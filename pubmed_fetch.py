import Bio
from Bio import Entrez
from Bio import Medline
import pandas as pd

Entrez.email = 'kgdhatchi@gmail.com'
db = 'pubmed'

categories = ['TI', 'AU', 'SO', 'TA', 'DP', 'CRDT', 'PMC', 'AID']
search_list = ['CC Members', 'Cancer', 'CCSG']
all_metadata = []


def getdata(records, metadata, search):
    for i in categories:
        if i == 'PMC':
            if 'PMC' in records:
                metadata.append(records['PMC'])
                continue
            else:
                metadata.append("No PMCID")
                continue
        if i == 'AU':
            metadata.append(records['AU'])
            metadata.append(records['AU'][0])
            continue
        if i == 'AID':
            added = 0
            for j in records['AID']:
                if '[doi]' in j:
                    metadata.append(j)
                    added = 1
                    break
            if added == 0:
                metadata.append("No DOI")
            continue
        try:
            metadata.append(records[i])
            continue
        except:
            metadata.append('None')
            continue
    metadata.append(search)
    metadata.append("")
    return metadata


def fetchMetadata(pmid_list, search):
    for i in pmid_list:
        efetch = Entrez.efetch(db, id=i, rettype="medline", retmode="text")
        records = Medline.read(efetch)
        metadata = []
        metadata.append(i)
        metadata = getdata(records, metadata, search)
        all_metadata.append(metadata)
    return all_metadata
