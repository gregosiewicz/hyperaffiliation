import pandas as pd
from pybliometrics.scopus import ScopusSearch, config
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed
from config import ACTIVE_JOURNALS_CSV, YEARS, DOC_TYPES, COLUMNS


def list_of_active_journals(file_path):
    df = pd.read_csv(file_path)
    return df['Sourcerecord ID'].tolist()


def query_scopus(q, refresh=False):
    try:
        return ScopusSearch(q, refresh=refresh).results or []
    except (AttributeError, KeyError):
        return ScopusSearch(q, refresh=True).results or []


def get_papers(journal_id, doctype, year):
    query_str = f'(SOURCE-ID({journal_id}) AND DOCTYPE({doctype}) AND PUBYEAR={year})'
    results = query_scopus(query_str)
    return pd.DataFrame(results)


def count_affiliations(affiliation_str):
    return affiliation_str.count('-') + 1 if pd.notna(affiliation_str) and affiliation_str else 0


def process_papers(journal_ids, doctypes, years):
    papers = pd.DataFrame(columns=COLUMNS)
    for journal_id in journal_ids:
        for doctype in doctypes:
            for year in years:
                df = get_papers(journal_id, doctype, year)
                if df.empty:
                    continue
                df['year'] = year
                affiliations = df['author_afids'].str.split(';')
                df['max_multiaffiliations'] = affiliations.apply(
                    lambda x: max(count_affiliations(aid) for aid in x) if isinstance(x, list) else 0
                )
                papers = pd.concat([papers, df[COLUMNS]], ignore_index=True)
    return papers


def main():
    config.load()
    journal_ids = list_of_active_journals(ACTIVE_JOURNALS_CSV)
    all_papers = pd.DataFrame(columns=COLUMNS)

    with ProcessPoolExecutor(max_workers=6) as executor:
        future = executor.submit(process_papers, journal_ids, DOC_TYPES, YEARS)
        for result in tqdm(as_completed([future]), total=1, desc="Processing journals"):
            all_papers = pd.concat([all_papers, result.result()], ignore_index=True)

    all_papers['max_multiaffiliations'] = all_papers['max_multiaffiliations'].astype(int)
    timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    filename = f'results/papers_{timestamp}.csv'
    all_papers.to_csv(filename, index=False, sep=chr(30))



if __name__ == '__main__':
    main()
