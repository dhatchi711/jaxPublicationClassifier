import search_terms
import pubmed_fetch
from bs4 import BeautifulSoup
import urllib
from urllib import parse
import urllib.request as ur
import ssl
import Bio
from Bio import Entrez
from Bio import Medline
import pandas as pd

ssl._create_default_https_context = ssl._create_unverified_context

# Search Variables
author_search = search_terms.default_cc_search
cancer_search = search_terms.default_cancer_term_search
ccsg_search = search_terms.default_ccsg_search
ccSearch = 'CC Members'
cancerSearch = 'Cancer'
ccsg = 'CCSG'


def getNumberOfPages(num_of_results):
    num_pages = 0
    if num_of_results > 200:
        num_pages = int(num_of_results / 200)
        if num_of_results % 200 != 0:
            num_pages = num_pages + 1
    else:
        num_pages = 1
    return num_pages


def retrievePMIDs(searchLink):
    pmids = ''
    pmids_list = []
    first_time = 1
    for i in searchLink:
        if first_time == 1:
            page = ur.urlopen(i)
            soup = BeautifulSoup(page, "html.parser")
            pmids = soup.find('meta', attrs={"name": "log_displayeduids"}).get("content")
            pmids_list = pmids.split(",")
            first_time -= 1
        else:
            page = ur.urlopen(i)
            soup = BeautifulSoup(page, "html.parser")
            pmids = soup.find('meta', attrs={"name": "log_displayeduids"}).get("content")
            pmids_list = pmids_list + (pmids.split(","))
    return pmids_list


def constructSearchURL(searchTerm, startDate, endDate):
    search = searchTerm
    date_range = "(" + '"' + startDate + '"' + "[Date - Publication] : " + '"' + endDate + '"' + "[Date - Publication])"
    date_range_URL = urllib.parse.quote_plus(date_range)
    search_term_URL = urllib.parse.quote_plus(search)
    search_URL = search_terms.default_search_url
    page_count = search_terms.page_count
    num_of_returns = search_terms.page_returns
    full_Search_URL = search_URL + search_term_URL + date_range_URL + num_of_returns
    page = ur.urlopen(full_Search_URL)
    soup = BeautifulSoup(page, "html.parser")
    try:
        total_num_of_results = int(soup.find('meta', attrs={"name": "log_resultcount"}).get("content"))
        pages = getNumberOfPages(total_num_of_results)
        search_pages = []
        while pages >= 1:
            page_str = str(pages)
            full_Search_URL = search_URL + search_term_URL + date_range_URL + num_of_returns + page_count + page_str
            search_pages.append(full_Search_URL)
            pages -= 1
        pmid_list = retrievePMIDs(search_pages)
    except:
        pmid_list = []
        pmid_list.append(soup.find('meta', attrs={"name": "citation_pmid"}).get("content"))

    return pmid_list


def add_to_df(cclist):
    columns = ['PMID', 'Title', 'Authors', 'FirstAuthor', 'Citation', 'Journal', 'PublicationDate', 'CreateDate',
               'PMCID',
               'DOI', 'SearchString', 'CCSGSearch']
    df = pd.DataFrame(cclist, columns=columns)
    return df
    # df.to_excel("list.xlsx")


def main(start, end):
    start = start.replace("-", "/")
    end = end.replace("-", "/")
    print(start)
    print(end)
    cc_pmids = constructSearchURL(author_search, start, end)
    print(cc_pmids)
    cc_results = pubmed_fetch.fetchMetadata2(cc_pmids, ccSearch)
    print(cc_results)
    cancer_pmids = constructSearchURL(cancer_search, start, end)
    for i in range(len(cc_results)):
        if cc_results[i][0] in cancer_pmids:
            cc_results[i][10] = 'Cancer'
    ccsg_pmids = constructSearchURL(ccsg_search, start, end)
    for i in range(len(cc_results)):
        if cc_results[i][0] not in ccsg_pmids:
            cc_results[i][11] = 'No'
        else:
            cc_results[i][11] = 'Yes'

    df = add_to_df(cc_results)
    return df
