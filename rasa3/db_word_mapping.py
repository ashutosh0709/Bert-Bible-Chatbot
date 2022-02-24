
dict = {'astound' : 'fear' , 'happily' : 'happiness'} 






def write_lookup_entries_to_db(word1 , word2):

    import os
    from dotenv import load_dotenv
    from pyArango.connection import Connection

    load_dotenv()
    arangodb_username = os.getenv("arangodb_username")
    arangodb_password = os.getenv('arangodb_password')
    database_name = os.getenv('database_name')
    article_keywords_collection = os.getenv('article_keywords_collection')
    arangoURL = os.getenv('arangoURL')

    #arangodb_username = 
    #arangodb_password = 
    #database_name = 
    #article_keywords_collection = 
    #arangoURL = 
    

    conn = Connection(arangoURL=arangoURL, username=arangodb_username, password=arangodb_password)

    try:
        db = conn.createDatabase(name=database_name) #handles creation of db
    except:
        db = conn[database_name]         # handles opening of created db
    print(db)


    try:
        articles_Collection = db.createCollection(name=article_keywords_collection) #creating a new collection on db = school
    except:
        articles_Collection = db[article_keywords_collection] #connecting if already exists.
    #################################################################################################

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

def add_word_mappings_to_db(dict):
    for word1 in dict:
        word2 = dict.get(word1)
        db , articles_collection = write_lookup_entries_to_db(word1 , word2)

       
add_word_mappings_to_db(dict)