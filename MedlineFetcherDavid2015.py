# ****************************
# *****  Medline Fetcher *****
# ****************************

# MEDLINE USER REQUIREMENT : Run retrieval scripts on weekends or between 9 pm and 5 am Eastern Time weekdays

import personalpath

import sys
if sys.version_info >= (3, 0): from urllib.request import urlopen
else: from urllib import urlopen

# from xml import xpath
import xml.dom.minidom
import os
import time
# import libxml2
from lxml import etree

pubMedEutilsURL = 'http://www.ncbi.nlm.nih.gov/entrez/eutils'
pubMedDB = 'Pubmed'
reportType = 'medline'

from personalpath import PersonalPath
personalpath = PersonalPath('MedLine/')
personalpath.createDirectory()




# Return the:
# - count = 
# - queryKey = 
# - webEnv = 
def medlineEsearch(query):

    print ("MedlineFetcher::medlineFetcher :")

    "Get number of results for query 'query' in variable 'count'"
    "Get also 'queryKey' and 'webEnv', which are used by function 'medlineEfetch'"
    
    query = query.replace(' ', '%20')
        
    eSearch = '%s/esearch.fcgi?db=%s&retmax=1&usehistory=y&term=%s' %(pubMedEutilsURL, pubMedDB, query)
    eSearchResult = urlopen(eSearch)
    data = eSearchResult.read()

    root = etree.XML(data)

    findcount = etree.XPath("/eSearchResult/Count/text()")
    count = findcount(root)[0]
    
    findquerykey = etree.XPath("/eSearchResult/QueryKey/text()")
    queryKey = findquerykey(root)[0]

    findwebenv = etree.XPath("/eSearchResult/WebEnv/text()")
    webEnv = findwebenv(root)[0]

    # doc = libxml2.parseDoc(data)
    # count = doc.xpathEval('eSearchResult/Count/text()')[0]
    # queryKey = doc.xpathEval('eSearchResult/QueryKey/text()')[0]
    # webEnv = doc.xpathEval('eSearchResult/WebEnv/text()')[0]
    # print count, queryKey, webEnv
    return str(count), queryKey, webEnv

def medlineEfetch(query, retmax):
    
    print ("MedlineFetcher::medlineEfetch :")

    "Fetch medline result for query 'query', saving results to file every 'retmax' articles"

    queryNoSpace = query.replace(' ', '') # No space in directory and file names, avoids stupid errors
    

    pubmedqueryfolder = personalpath.pubMedAbstractsPath + 'Pubmed_' + queryNoSpace
    if not os.path.isdir(pubmedqueryfolder):
        os.makedirs(pubmedqueryfolder)

    pubMedResultFileName = pubmedqueryfolder + '/Pubmed_' + queryNoSpace + '.txt'
    pubMedResultFile = open(pubMedResultFileName, 'w')
    
    count1, queryKey, webEnv = medlineEsearch(query)

    print ('Submitted query ' , query , ' gives ' , count1 , ' results')
    print ('Starting fetching at ' , time.asctime(time.localtime()) , '\n')
    
   #  Fetch results...

    count = int(count1)  
    retstart = 0

    while(retstart < count):
        print (str(retstart) )
        eFetch = '%s/efetch.fcgi?email=youremail@example.org&rettype=%s&retmode=text&retstart=%s&retmax=%s&db=%s&query_key=%s&WebEnv=%s' %(pubMedEutilsURL, reportType, retstart, retmax, pubMedDB, queryKey, webEnv)                
        eFetchResult = urlopen(eFetch)
        if sys.version_info >= (3, 0): pubMedResultFile.write(eFetchResult.read().decode('utf-8'))
        else: pubMedResultFile.write(eFetchResult.read())
        retstart += retmax

    pubMedResultFile.close()
    print ('Fetching for query ' , query , ' finished at ' , time.asctime(time.localtime()) )
    print (count , ' results written to file ' , pubMedResultFileName , '\n' )




def medlineEfetchRAW(query, retmax , limit):
    
    print ("MedlineFetcher::medlineEfetch :")

    "Fetch medline result for query 'query', saving results to file every 'retmax' articles"

    queryNoSpace = query.replace(' ', '') # No space in directory and file names, avoids stupid errors
    

    pubmedqueryfolder = personalpath.pubMedAbstractsPath + 'Pubmed_' + queryNoSpace
    if not os.path.isdir(pubmedqueryfolder):
        os.makedirs(pubmedqueryfolder)

    pubMedResultFileName = pubmedqueryfolder + '/Pubmed_' + queryNoSpace + '.xml'
    pubMedResultFile = open(pubMedResultFileName, 'w')
    
    count1, queryKey, webEnv = medlineEsearch(query)

    print ('Submitted query ' , query , ' gives ' , count1 , ' results')
    print ('Starting fetching at ' , time.asctime(time.localtime()) , '\n')
    
   #  Fetch results...


    count = int(count1)
    count = limit  
    retstart = 0

    while(retstart < count):
        print (str(retstart) )
        eFetch = '%s/efetch.fcgi?email=youremail@example.org&rettype=%s&retmode=xml&retstart=%s&retmax=%s&db=%s&query_key=%s&WebEnv=%s' %(pubMedEutilsURL, reportType, retstart, retmax, pubMedDB, queryKey, webEnv)                
        eFetchResult = urlopen(eFetch)
        if sys.version_info >= (3, 0): pubMedResultFile.write(eFetchResult.read().decode('utf-8'))
        else: pubMedResultFile.write(eFetchResult.read())
        retstart += retmax
        # if retstart>limit: break

    pubMedResultFile.close()
    print ('Fetching for query ' , query , ' finished at ' , time.asctime(time.localtime()) )
    print (count , ' results written to file ' , pubMedResultFileName , '\n' )






def serialFetcher(yearsNumber,query):
    print ("MedlineFetcher::serialFetcher :")
    for i in range(yearsNumber):
        year = str(2015 - i)
        print ('YEAR ' + year)
        print ('---------\n')
        # medlineEfetch(str(year) + '[dp] '+query , 20000)
        medlineEfetchRAW(str(year) + '[dp] '+query , retmax=20000, limit=100)
    print ('Done !')
# regler les parametres de serialFetcher:



serialFetcher(1, 'microbiota')
# query = str(2015)+ '[dp] '+'microbiota'
# medlineEsearch( query )
