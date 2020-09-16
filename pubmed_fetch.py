import Bio
import time
from Bio import Entrez
from Bio import Medline
import pandas as pd
import ssl

Entrez.email = 'awesomedeesudar123@gmail.com'
db = 'pubmed'
ssl._create_default_https_context = ssl._create_unverified_context

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
    all_metadata = []
    for i in pmid_list:
        time.sleep(1)
        print("fetching")
        efetch = Entrez.efetch(db, id=i, rettype="medline", retmode="text")
        records = Medline.read(efetch)
        metadata = [i]
        metadata = getdata(records, metadata, search)
        all_metadata.append(metadata)

    print(all_metadata)
    return all_metadata


lala = ['32868408', '32847614', '32839564', '32853550', '32817010', '32807987', '32328653', '32799889', '32823814',
        '32795400', '32795399', '32791514', '32787960', '32772418', '32769180', '32768438', '32755546', '32753598',
        '32747814', '32831705', '32823310', '32781932', '32555415', '32428240', '32631635', '32609955', '32366968',
        '32366680']


def fetchMetadata2(lala, search):
    pmid_string = ",".join(lala)
    print(pmid_string)
    records = []
    efetch = Entrez.efetch(db, id=pmid_string, rettype="medline", retmode="text")
    for i in range(len(lala)):
        record = Medline.read(efetch)
        records.append(record)
        print("receiving data")
    print("This is records", records)
    alldata = getdata1(records, search)
    return alldata

def getdata1(records, search):
    alldata = []
    for i in records:
        print("getting data")
        data = [i['PMID'], i['TI'], i['AU'], i['AU'][0], i['SO'], i['TA'], i['DP'], i['CRDT']]
        try:
            data.append(i['PMC'])
        except:
            data.append("No PMC")
        added = 0
        for j in i['AID']:
            if '[doi]' in j:
                data.append(j)
                added = 1
                break
        if added == 0:
            data.append("No DOI")

        print(i["PMID"])
        data.append(search)
        data.append("")
        alldata.append(data)
    return alldata