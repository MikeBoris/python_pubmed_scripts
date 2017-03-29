#! python2.7
"""
MTI_PubType_Program.py


"""
import re
import cx_Oracle
from Bio import Entrez
from sklearn.externals import joblib
import query as Q
import Pubmed_Desc_ID_Dict as PDID
import CIN_Desc_ID_Dict as CDID

# search pubmed for doi, return list of eligible pmids
def search(doi):
    Entrez.email = 'dclynch123@gmail.com'
    handle = Entrez.esearch(db='pubmed', retmode='xml', term=doi)
    results = Entrez.read(handle)
    return results

# search pubmed for pmid, return pubmed citation data in messy dict
def fetch_details(id_list):
    Entrez.email = 'dclynch123@gmail.com'
    handle = Entrez.efetch(db='pubmed', retmode='xml', id=id_list)
    results = Entrez.read(handle)
    return results

# make sure we're retrieving the right record given our input doi
def check(doi):
    results = search(doi)
    if 'ErrorList' in results:
        return None
    else:
        return results

# parse pubmed citation to extract pubtype data, if it exists
def find_pubtype(doi_result):
    try:
        results = check(doi_result)
        # pubtype data module
        id_list = results['IdList'][0]
        res = fetch_details(id_list)
        # if pub type exists append to pubtype list
        try:
            pub = res['PubmedArticle'][0]['MedlineCitation']['Article']['PublicationTypeList']
            uid = re.compile('[A-Z]\d{6}')
            pubIDs = uid.findall(str(pub))
            if pubIDs[0] == 'D016428' and len(pubIDs) == 1:
                print "Have to predict!"
            else:
                for item in pubIDs:
                    print "{} | {} | {}".format(result[0], PDID.PUB_DICT.get(item), "Pubmed")
        except:
            print "Nada"
    except:
        # add article_data to list object
        doc2pred = []
        # result[0] = AN, result[1] = DOI, result[2] = title, result[3] = abstract
        article_data = result[2] + str(result[3])
        doc2pred.append(article_data)
        predicted = clf.predict(doc2pred)
        pub = predicted[0]
        print "{} | {} | {}".format(result[0], CDID.PRED_DICT.get(pub), "Predicted")

if __name__ == '__main__':
    # load pickled model
    clf = joblib.load('PubClassifier.pkl')
    # set up db connection
    con = cx_Oracle.connect('query/ebsco@oramfs:1521/mfs.epnet.com')
    cur = con.cursor()
    cur.execute(Q.query)
    # print results in MTI-required format
    for result in cur:
        # result[0] = AN, result[1] = DOI
        find_pubtype(result[1])
    cur.close()
    con.close()
""" 
    # pubmed title + abstract data module

    # fetch title if is exists
    title = res['PubmedArticle'][0]['MedlineCitation']['Article']['ArticleTitle']
    # fetch abstract if it exists
    abstract = res['PubmedArticle'][0]['MedlineCitation']['Article']['Abstract']['AbstractText'][0]
    # add article_data to iterable list
    doc2pred = []
    article_data = title + abstract
    doc2pred.append(article_data)
    predicted = clf.predict(doc2pred)
    pub = predicted[0]
    print "Predicted pubs: "
    print "{}".format(CDID.PRED_DICT.get(pub))


TODO:
1. Clean up descriptor data for classifier (perhaps get better data on other descriptors from product);
2. train new model on all eligible descriptors;


4. Add function to include "Research" descriptor for specific pubtypes/predicted pubtypes

eg 'Systematic review' => 'Systematic review' + 'Research'
   'Randomized controlled trial' => 'Radomized controlled trial' + 'Research'
"""