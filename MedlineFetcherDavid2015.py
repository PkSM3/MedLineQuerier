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

    print ("MedlineFetcher::medlineEsearch :")

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
    values = { "count": int(str(count)), "queryKey": queryKey , "webEnv":webEnv }
    return values

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


# RETMAX:
# Total number of UIDs from the retrieved set to be shown in the XML output (default=20)
# maximum of 100,000 records
def medlineEfetchRAW( fullquery):
    

    query = fullquery["string"]
    retmax = fullquery["retmax"]
    count = fullquery["count"]
    queryKey = fullquery["queryKey"]
    webEnv = fullquery["webEnv"]

    print ("MedlineFetcher::medlineEfetchRAW :")

    "Fetch medline result for query 'query', saving results to file every 'retmax' articles"

    queryNoSpace = query.replace(' ', '') # No space in directory and file names, avoids stupid errors
    

    # pubmedqueryfolder = personalpath.pubMedAbstractsPath + 'Pubmed_' + queryNoSpace
    # if not os.path.isdir(pubmedqueryfolder):
    #     os.makedirs(pubmedqueryfolder)

    pubMedResultFileName = personalpath.mainPath + 'Pubmed_' + queryNoSpace + '.xml'
    pubMedResultFile = open(pubMedResultFileName, 'w')
    

    print ('Query "' , query , '"\t:\t' , count , ' results')
    print ('Starting fetching at ' , time.asctime(time.localtime()) )

    retstart = 0
    while(retstart < count):
        eFetch = '%s/efetch.fcgi?email=youremail@example.org&rettype=%s&retmode=xml&retstart=%s&retmax=%s&db=%s&query_key=%s&WebEnv=%s' %(pubMedEutilsURL, reportType, retstart, retmax, pubMedDB, queryKey, webEnv)                
        eFetchResult = urlopen(eFetch)
        if sys.version_info >= (3, 0): pubMedResultFile.write(eFetchResult.read().decode('utf-8'))
        else: pubMedResultFile.write(eFetchResult.read())
        retstart += retmax
        break # you shall not pass !!

    pubMedResultFile.close()
    print ('Fetching for query ' , query , ' finished at ' , time.asctime(time.localtime()) )
    print (retmax , ' results written to file ' , pubMedResultFileName , '\n' )
    print("------------------------------------------")






# GLOBALLIMIT:
# I will retrieve this exact amount of publications.
# The publications per year i'll retrieve per year will be = (k/N)*GlobalLimit <- i'll use this as RETMAX
# - k : Number of publications of x year (according to pubmed)
# - N : Sum of every k belonging to {X} (total number of pubs according to pubmed)
# - GlobalLimit : Number of publications i want.
def serialFetcher(yearsNumber,query, globalLimit):

    N = 0

    print ("MedlineFetcher::serialFetcher :")
    thequeries = []
    for i in range(yearsNumber):
        year = str(2015 - i)
        print ('YEAR ' + year)
        print ('---------\n')
        # medlineEfetch(str(year) + '[dp] '+query , 20000)
        # medlineEfetchRAW(str(year) + '[dp] '+query , retmax=300)
        pubmedquery = str(year) + '[dp] '+query
        globalresults = medlineEsearch(pubmedquery)
        N+=globalresults["count"]
        querymetadata = { 
            "string": pubmedquery , 
            "count": globalresults["count"] , 
            "queryKey":globalresults["queryKey"] , 
            "webEnv":globalresults["webEnv"] , 
            "retmax":0 
        }
        thequeries.append ( querymetadata )

    print("Total Number:", N,"publications")
    print("And i want just:",globalLimit,"publications")
    print("---------------------------------------\n")

    for query in thequeries:
        k = query["count"]
        percentage = k/float(N)
        retmax_forthisyear = int(round(globalLimit*percentage))
        query["retmax"] = retmax_forthisyear
        # print(query)
        medlineEfetchRAW( query )

    print ('Done !')
# regler les parametres de serialFetcher:


# serialFetcher(yearsNumber=3, 'microbiota' , globalLimit=100 )
serialFetcher( 3, 'microbiota' , 300 )
# query = str(2015)+ '[dp] '+'microbiota'
# medlineEsearch( query )
