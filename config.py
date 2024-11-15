SCOPUS_JOURNALS_XLSX = 'data/scopus_journals.xlsx'
ACTIVE_JOURNALS_CSV = 'data/active_scopus_journals.csv'
PAPERS_FILE = 'results/papers_YYYYMMDD_HHMMSS.csv'
URL = 'https://www.elsevier.com/products/scopus/content'
START_YEAR = 2020
END_YEAR = 2024
YEARS = range(START_YEAR, END_YEAR + 1)
DOC_TYPES = ['ar', 'no', 'cp', 'sh', 're', 'er']
COLUMNS = [
    'source_id',
    'eid',
    'doi',
    'max_multiaffiliations',
    'title',
    'publicationName',
    'year',
]
RESULT_SIZE = 1000
