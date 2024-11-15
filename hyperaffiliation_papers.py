import pandas as pd
from config import PAPERS_FILE, RESULT_SIZE


if __name__ == '__main__':
    df = pd.read_csv(PAPERS_FILE, sep=chr(30))

    top = df.nlargest(RESULT_SIZE, 'max_multiaffiliations')
    top['eid'] = top['eid'].apply(
        lambda x: f'=HYPERLINK("https://www.scopus.com/record/display.uri?eid={x}&origin=resultslist"; "scopus")'
    )
    top['doi'] = top['doi'].apply(lambda x: f'=HYPERLINK("https://doi.org/{x}"; "doi")')
    
    top.rename(
        columns={
            'source_id': 'Journal ID',
            'eid': 'Scopus link',
            'doi': 'DOI link',
            'max_multiaffiliations': 'Max affiliation',
            'publicationName': 'Journal',
            'year': 'Year',
            'title': 'Title',
        },
        inplace=True
    )

    now = pd.Timestamp.now()
    top.to_csv(f'results/papers_largest_{now.strftime('%Y%m%d_%H%M%S')}.csv', index=False, sep=chr(30))
