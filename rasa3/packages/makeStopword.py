#######################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
# THIS FUNCTIONS RETURN A DICTIONARY WITH ALL THE STOPWORD-RESULTS FOR RASA-BACKEND HARDCODED.

def getStopwordsDict():

    stopword_dict = {
        "god" : ['https://en.wikipedia.org/wiki/God' , 'In monotheistic thought, God is usually conceived of as the supreme being, creator, and principal object of faith.[1] God is usually conceived of as being omnipotent, omniscient, omnipresent and omnibenevolent as well as having an eternal and necessary existence.'] , 
        "jesus" : ["https://en.wikipedia.org/wiki/Jesus" , "Jesus, also referred to as Jesus of Nazareth or Jesus Christ, was a first-century Jewish preacher and religious leader. He is the central figure of Christianity, the world's largest religion. Most Christians believe he is the incarnation of God the Son and the awaited messiah (the Christ), prophesied in the Hebrew Bible."] ,
        "lord" : ["https://en.wikipedia.org/wiki/Lord" , "Lord is an appellation for a person or deity who has authority, control, or power over others, acting as a master, a chief, or a ruler. The appellation can also denote certain persons who hold a title of the peerage in the United Kingdom, or are entitled to courtesy titles."] ,
        "evil" : ["https://en.wikipedia.org/wiki/Evil" , "Evil, in a general sense, is defined by what it is not—the opposite or absence of good. It can be an extremely broad concept, although in everyday usage it is often more narrowly used to talk about profound wickedness."] ,
        "devil" : ["https://en.wikipedia.org/wiki/Devil" , "A devil is the personification of evil as it is conceived in various cultures and religious traditions. It is seen as the objectification of a hostile and destructive force."] ,
        "man" : ["https://en.wikipedia.org/wiki/Man" , "A man is an adult male human. Prior to adulthood, a male human is referred to as a boy (a male child or adolescent)."] ,
        "men" : ["https://en.wikipedia.org/wiki/Man" , "A man is an adult male human. Prior to adulthood, a male human is referred to as a boy (a male child or adolescent)."] ,
        "son" : ["https://en.wikipedia.org/wiki/Son" , "A son is a male offspring; a boy or a man in relation to his parents. The female counterpart is a daughter. From a biological perspective, a son constitutes a first degree relative."] ,
        "child" : ["https://en.wikipedia.org/wiki/Child" , "Biologically, a child (plural children) is a human being between the stages of birth and puberty,[1][2] or between the developmental period of infancy and puberty."] ,
        "children" : ["https://en.wikipedia.org/wiki/Child" , "Biologically, a child (plural children) is a human being between the stages of birth and puberty,[1][2] or between the developmental period of infancy and puberty."] ,
        "earth" : ["https://en.wikipedia.org/wiki/Earth" , "Earth is the third planet from the Sun and the only astronomical object known to harbor life. While large amounts of water can be found throughout the Solar System, only Earth sustains liquid surface water."] ,
        "bible" : ["https://en.wikipedia.org/wiki/Bible" , "The Bible is a collection of religious texts or scriptures sacred in Christianity, Judaism, Samaritanism, and many other faiths. It appears in the form of an anthology, a compilation of texts of a variety of forms, originally written in Hebrew, Aramaic, and Koine Greek. These texts include theologically-focused narratives, hymns, prayers, proverbs, parables, didactic letters, admonitions, poetry, and prophecies."] ,
        "father" : ["https://en.wikipedia.org/wiki/Father" , "A father is the male parent of a child. Besides the paternal bonds of a father to his children, the father may have a parental, legal, and social relationship with the child that carries with it certain rights and obligations."] , 
        "romance"  : ["""https://www.mindbodygreen.com/articles/how-to-be-romantic""" , """Being romantic is about expressing love and dedication in a way that's intentional, unmistakable, and deeply affectionate. It often involves dramatic or passionate gestures, though smaller actions that indicate enduring affection can also be romantic."""]
    }

    return stopword_dict

############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
# WHENEVER WE SHIFT TO A NEW DATABASE, WHERE WE WOULD NEED TO HARDCODE ALL STOPWORDS-RESULTS, SO THIS FUNCTION
# CAN BE CALLED SO THAT WE CAN POPULATE SOME OF THESE ENTRIES PROGRAMMATICALLY.

def CreateStopwordEntryInDb():
    
    import os
    from dotenv import load_dotenv
    from pyArango.connection import Connection
    load_dotenv()

    arangodb_username = os.getenv("arangodb_username")
    arangodb_password = os.getenv('arangodb_password')
    database_name = os.getenv('database_name')
    stopwords_collection = os.getenv('stopwords_collection')
    arangoURL = os.getenv('arangoURL')

    conn = Connection(arangoURL=arangoURL, username=arangodb_username, password=arangodb_password)

    try:
        db = conn.createDatabase(name=database_name) #handles creation of db
    except:
        db = conn[database_name]         # handles opening of created db
    print(db)


    try:
        articles_Collection = db.createCollection(name=stopwords_collection) #creating a new collection on db = school
    except:
        articles_Collection = db[stopwords_collection] #connecting if already exists.

    aql = "FOR x IN StopWordsCollection RETURN x"
    queryResult = db.AQLQuery(aql, rawResults=True, batchSize=100)
    stopword_dict = getStopwordsDict()
    for word in stopword_dict.keys():
        for entry in queryResult:
            if word == entry.get('STOPWORD'):
                break

        doc = articles_Collection.createDocument()
        doc['STOPWORD'] = word
        doc['LINK'] = stopword_dict.get(word)[0]
        doc['PARA'] = stopword_dict.get(word)[1]
        doc._key = word
        try:
            doc.save()
        except: 
            pass

