"""
Given input article DOI, outputs article metadata (Publication type & MeSH headings)

Usage:
include doi as argument
eg
[13:10:43][sandbox|60]# python efetch.py 10.1007/s10916-009-9293-6

Publication types:

10.1007/s10916-009-9293-6 | D016430
10.1007/s10916-009-9293-6 | D016428
10.1007/s10916-009-9293-6 | D013485

MeSH Headings:

10.1007/s10916-009-9293-6 | ['Q000517', 'D000058'] | ["'Y'", "'N'"]
10.1007/s10916-009-9293-6 | ['D000328'] | ["'N'"]
10.1007/s10916-009-9293-6 | ['D000465'] | ["'N'"]
10.1007/s10916-009-9293-6 | ['D000843'] | ["'N'"]
10.1007/s10916-009-9293-6 | ['D001696'] | ["'N'"]
10.1007/s10916-009-9293-6 | ['D056228'] | ["'Y'"]
10.1007/s10916-009-9293-6 | ['D005260'] | ["'N'"]
10.1007/s10916-009-9293-6 | ['D005684'] | ["'Y'"]
10.1007/s10916-009-9293-6 | ['D006801'] | ["'N'"]
10.1007/s10916-009-9293-6 | ['D008297'] | ["'N'"]
10.1007/s10916-009-9293-6 | ['D018482'] | ["'N'"]
10.1007/s10916-009-9293-6 | ['D004856'] | ["'Y'"]
10.1007/s10916-009-9293-6 | ['D014732'] | ["'Y'"]

more info:
bio entrez docs:
http://biopython.org/DIST/docs/api/Bio.Entrez-module.html
"""
import re
from sys import argv
from Bio import Entrez


query = argv[1]

def search(doi):
    Entrez.email = 'abc@example.com' # insert your email
    handle = Entrez.esearch(db='pubmed', retmode='xml', term=doi)
    results = Entrez.read(handle)
    return results

def fetch_details(id_list):
    Entrez.email = 'abc@example.com' # insert your email
    handle = Entrez.efetch(db='pubmed', retmode='xml', id=id_list)
    results = Entrez.read(handle)
    return results

if __name__ == '__main__':
    results = search(query)
    id_list = results['IdList'][0]
    res = fetch_details(id_list)

    # if pub exists, assign pub type data to second sheet
    print ""
    print "Publication types:"
    pub = res['PubmedArticle'][0]['MedlineCitation']['Article']['PublicationTypeList']
    print ""

    uid = re.compile('[A-Z]\d{6}')
    pubIDs = uid.findall(str(pub))

    for item in pubIDs:
        print "{} | {} ".format(query, item)

    print ""

    # if mesh exists, assign mesh data to first sheet, each mesh heading
    major = re.compile(r"\'[A-Z]\'")

    if (res['PubmedArticle'][0]['MedlineCitation']['MeshHeadingList']):
    	print "MeSH Headings:"
    	myList = res['PubmedArticle'][0]['MedlineCitation']['MeshHeadingList']
        me = re.compile(r"\'(.+?)\'")

        print ""    
    	for value in enumerate(myList):
    		print "{} | {} | {}".format(query, uid.findall(str(value)), major.findall(str(value)))
    	print ""
    else:
    	print "No MeSH available"






