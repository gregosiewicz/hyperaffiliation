import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from config import URL, SCOPUS_JOURNALS_XLSX


def download_scopus_journals_file():
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    link = soup.find('a', text='Download the Source title list')['href']
    response = requests.get(link)
    with open(SCOPUS_JOURNALS_XLSX, 'wb') as file:
        file.write(response.content)


def filter_and_save_active_journals():
    df = pd.read_excel(SCOPUS_JOURNALS_XLSX)
    active_df = df[df['Active or Inactive'] == 'Active']
    active_df = active_df[['Sourcerecord ID', 'Source Title']]
    active_df.to_csv(SCOPUS_JOURNALS_XLSX, index=False)


def main():
    if not os.path.exists(SCOPUS_JOURNALS_XLSX):
        download_scopus_journals_file()
    filter_and_save_active_journals()


if __name__ == '__main__':
    main()
