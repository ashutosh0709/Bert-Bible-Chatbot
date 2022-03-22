import os
from dotenv import load_dotenv
from pyArango.connection import Connection

###############################################################################################################################################################################################################################################################################################################################################################################################################

# THIS FUNC WRITES MAPPED LOOKUP ENTRES TO DB, WHICH RASA-ACTIONS USE TO PROVIDE RESULTS FOR MISMATCHED 
# KEYWORD, IF A MAPPING IS PRESENT IN OUR DATABASE FOR THE ENTERED WORD.

def write_lookup_entries_to_db(word1 , word2):

    load_dotenv()

    arangodb_username = os.getenv("arangodb_username")
    arangodb_password = os.getenv('arangodb_password')
    database_name = os.getenv('database_name')
    lookup_collection = os.getenv('lookup_collection')
    arangoURL = os.getenv('arangoURL')

    conn = Connection(username=arangodb_username, password=arangodb_password)

    try:
        db = conn.createDatabase(name=database_name) #handles creation of db
    except:
        db = conn[database_name]         # handles opening of created db
    print(db)


    try:
        articles_Collection = db.createCollection(name=lookup_collection) #creating a new collection on db = school
    except:
        articles_Collection = db[lookup_collection] #connecting if already exists.
    ############################################################

    doc = articles_Collection.createDocument()

    doc['MAPPED_WORD'] = word1
    doc['KEYWORD'] = word2
    doc._key = ''.join(word1) 
    print(''.join(word1))
    try:
       doc.save()
    except:
       pass

    return db , articles_Collection


##############################################################################################################################################################################################################################################################################################################################################################################################################

# this function writes a word to the collection specifying it to be mapped later on to a keyword, used by 
# actions server to find user-specified mappings for some words to some keywords.

def write_words_to_db(word1):

    load_dotenv()

    arangodb_username = os.getenv("arangodb_username")
    arangodb_password = os.getenv('arangodb_password')
    database_name = os.getenv('database_name')
    words_not_mapped_collection = os.getenv('words_not_mapped')
    arangoURL = os.getenv('arangoURL')


    conn = Connection(arangoURL=arangoURL, username=arangodb_username, password=arangodb_password)

    try:
        db = conn.createDatabase(name=database_name) 
    except:
        db = conn[database_name]        
    print(db)


    try:
        articles_Collection = db.createCollection(name=words_not_mapped_collection) 
    except:
        articles_Collection = db[words_not_mapped_collection]
    doc = articles_Collection.createDocument()
    doc['WORD'] = word1
    doc._key = ''.join(word1) 
    print(''.join(word1))
    try:
       doc.save()
    except: 
       pass


###############################################################################################################################################################################################################################################################################################################################################################################################################

# Get a dictionary of {mapped_word : keyword} for using in the actions-pipeline.

def map_keywords_to_urls_in_db(articles_Collection , db):
    word_map_dictionary = {}

    for doc in articles_Collection.fetchAll():
        word1 =  doc['MAPPED_WORD']
        word2 = doc['KEYWORD']
        
        word_map_dictionary.update({word1 : word2})

    return word_map_dictionary    

###############################################################################################################################################################################################################################################################################################################################################################################################################

# get list of all the valid keywords that we have at this point, extracted from database.

def getListOfAllKeywordsFromDb():

    load_dotenv()
    arangodb_username = os.getenv("arangodb_username")
    arangodb_password = os.getenv('arangodb_password')
    database_name = os.getenv('database_name')
    article_keywords_collection = os.getenv('article_keywords_collection')
    keyword_to_url_collection = os.getenv('keyword_url_collection')
    arangoURL = os.getenv('arangoURL')


    db , articles_collection = write_lookup_entries_to_db(' ' , ' ')
    lookup_dict = map_keywords_to_urls_in_db(articles_collection , db)   


    # conn = Connection(username=arangodb_username, password=arangodb_password)
    # db = conn[database_name]   
    # articles_Collection = db[keyword_to_url_collection]


    # list_of_all_keywords  = []
    # aql = "FOR x IN keyword_to_url_collection RETURN x"
    # queryResult = db.AQLQuery(aql, rawResults=True, batchSize=100)
    # for entry in queryResult:
    #     list_of_all_keywords.append(entry.get('KEYWORD'))
    # list_of_all_keywords , db , articles_collection , 
    
    return lookup_dict

#############################################################################################################################################################################################################################################################################################################################################################
# WILL RETURN TRUE IF THE ENTERED WORD IS A VALID KEYWORD FETCHED FROM DATABASE, ELSE WILL RETURN FALSE.

def isKeyword(word):
    load_dotenv()

    arangodb_username = os.getenv("arangodb_username")
    arangodb_password = os.getenv('arangodb_password')
    database_name = os.getenv('database_name')
    lookup_collection = os.getenv('keyword_url_collection')
    arangoURL = os.getenv('arangoURL')

    conn = Connection(username=arangodb_username, password=arangodb_password)

    try:
        db = conn.createDatabase(name=database_name) #handles creation of db
    except:
        db = conn[database_name]         # handles opening of created db
    print(db)


    try:
        articles_Collection = db.createCollection(name=lookup_collection) #creating a new collection on db = school
    except:
        articles_Collection = db[lookup_collection] #connecting if already exists.
    #############################################################
    aql = "FOR x IN keyword_to_url_collection RETURN x"
    queryResult = db.AQLQuery(aql, rawResults=True, batchSize=100)
    for entry in queryResult:
        if word == entry.get('KEYWORD'):
            return True
    
    return False


#############################################################################################################################################################################################################################################################################################################################################################
# WILL RETURN TRUE IF THE ENTERED WORD IS A STOPWORD ACCORDING TO THE DATABASE COLLECTION. ELSE WILL RETURN FALSE.
def isStopword(word):
    load_dotenv()

    arangodb_username = os.getenv("arangodb_username")
    arangodb_password = os.getenv('arangodb_password')
    database_name = os.getenv('database_name')
    stopwords_collection = os.getenv('stopwords_collection')
    arangoURL = os.getenv('arangoURL')

    conn = Connection(username=arangodb_username, password=arangodb_password)

    try:
        db = conn.createDatabase(name=database_name) #handles creation of db
    except:
        db = conn[database_name]         # handles opening of created db
    print(db)


    try:
        articles_Collection = db.createCollection(name=stopwords_collection) #creating a new collection on db = school
    except:
        articles_Collection = db[stopwords_collection] #connecting if already exists.

    ###
    aql = "FOR x IN StopWordsCollection RETURN x"
    queryResult = db.AQLQuery(aql, rawResults=True, batchSize=100)
    for entry in queryResult:
        if word == entry.get('STOPWORD'):
            return True
    
    return False

############################################################################################################################################################################################################################################################################################################
# THIS FUNCTION RETURNS THE DATA(LINK , PARA) FOR A STOPWORD AS PER THE DATABASE-ENTRY FOR THAT STOPWORD.

def getDataOfStopword(stopword):
    import os
    from dotenv import load_dotenv
    from pyArango.connection import Connection
    load_dotenv()

    arangodb_username = os.getenv("arangodb_username")
    arangodb_password = os.getenv('arangodb_password')
    database_name = os.getenv('database_name')
    stopwords_collection = os.getenv('stopwords_collection')
    arangoURL = os.getenv('arangoURL')

    conn = Connection(username=arangodb_username, password=arangodb_password)

    try:
        db = conn.createDatabase(name=database_name) #handles creation of db
    except:
        db = conn[database_name]         # handles opening of created db
    print(db)


    try:
        articles_Collection = db.createCollection(name=stopwords_collection) #creating a new collection on db = school
    except:
        articles_Collection = db[stopwords_collection] #connecting if already exists.

    try:
        doc = articles_Collection[stopword]
        link = doc['LINK']
        para = doc['PARA']
    except:
        link = "Not Getting Link from stopword"
        para = "Not Getting Para from stopword"

    return link , para



