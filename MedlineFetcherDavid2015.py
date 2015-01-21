# ****************************
# *****  Medline Fetcher *****
# ****************************

# MEDLINE USER REQUIREMENT : Run retrieval scripts on weekends or between 9 pm and 5 am Eastern Time weekdays

import personalpath
import urllib
# from xml import xpath
import xml.dom.minidom
import os
import time
import libxml2

pubMedEutilsURL = 'http://www.ncbi.nlm.nih.gov/entrez/eutils'
pubMedDB = 'Pubmed'
reportType = 'medline'

from personalpath import PersonalPath
personalpath = PersonalPath('MedLine/')
personalpath.createDirectory()


def medlineEsearch(query):

    print ("MedlineFetcher::medlineFetcher :")

    "Get number of results for query 'query' in variable 'count'"
    "Get also 'queryKey' and 'webEnv', which are used by function 'medlineEfetch'"
    
    query = query.replace(' ', '%20')
        
    eSearch = '%s/esearch.fcgi?db=%s&retmax=1&usehistory=y&term=%s' %(pubMedEutilsURL, pubMedDB, query)
    eSearchResult = urllib.urlopen(eSearch)
    data = eSearchResult.read()

    doc = libxml2.parseDoc(data)

    count = doc.xpathEval('eSearchResult/Count/text()')[0]
    queryKey = doc.xpathEval('eSearchResult/QueryKey/text()')[0]
    webEnv = doc.xpathEval('eSearchResult/WebEnv/text()')[0]
    # print (count, queryKey, webEnv)
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
        eFetchResult = urllib.urlopen(eFetch)
        pubMedResultFile.write(eFetchResult.read())
        retstart += retmax

    pubMedResultFile.close()
    print ('Fetching for query ' , query , ' finished at ' , time.asctime(time.localtime()) )
    print (count , ' results written to file ' , pubMedResultFileName , '\n' )

def serialFetcher(yearsNumber,request):
    print ("MedlineFetcher::serialFetcher :")
    for i in range(yearsNumber):
        year = str(2015 - i)
        print ('YEAR ' + year)
        print ('---------\n')
        medlineEfetch(str(year) + '[dp] '+request , 20000)
    print ('Done !')
# regler les parametres de serialFetcher:



serialFetcher(1, 'microbiota')
# query = str(2014) + '[dp] '+'microbiota'
# print medlineEsearch( query )
