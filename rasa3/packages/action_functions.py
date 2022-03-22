from nltk.probability import FreqDist
import requests
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize
from nltk.corpus import wordnet


###############################################################################################################################################################################################################################################################################################################################################################################################
# RETURNS A DICTIONARY CONTAINING HARDCODED DATA(LINK , URL) FOR STOPWORDS. USED BY ACTIONS PIPELINE.

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
###############################################################################################################################################################################################################################################################################################################################################################################################
# (FUNCTION DEPRECIATED FROM PIPELINE) Finding the best meaning keyword for the given inputted word, by checking similarity through the NLTK module.
# we currently are'nt using this, but have been kept here just in case.

def bestMeaningWord(word1 , lis):

    bestword = ''
    prevmax = -10

    for word2 in lis:
        syn1 = wordnet.synsets(word1)[0]
        syn2dummy = wordnet.synsets(word2)
        if len(syn2dummy) == 0 :
            continue
        syn2 = syn2dummy[0]
      #  print ("hello name :  ", syn1.name())
      #  print ("selling name :  ", syn2.name())

        if syn1.wup_similarity(syn2) > prevmax:
            prevmax = syn1.wup_similarity(syn2)
            bestword = word2
    
    return bestword

###############################################################################################################################################################################################################################################################################################################################################################################################
# takes in a word as input and returns the best synonym-keyword associated with it(BERT), by making a call to the synonym-api.

def mismatchFunc(text , mismatch_url):
    data = {'text':text}
    r = requests.get(url=mismatch_url , data=data)
    if r.status_code == 400:
        rv = "failed to retrive the bert-assigned keyword for the entered mismatched keyword"
    else:    
        r = r.json()
        rv = r['keyword']
    return rv


###############################################################################################################################################################################################################################################################################################################################################################################################
# takes a keyword as input and makes the call to api, and gets the best url and article for that keyword, and returns the url and best para for that keyword eventually.

def apiFunc(text ,url):
    print(url)
    link_url = ""
    data = {'text':text}
    r = requests.get(url=url , data=data)
    if r.status_code == 400:
        article = "Sorry, I did not understand."
    else:    
        rv = r.json()
        article = rv['para']
        print(article) #################### delete this prompt 
        link_url = rv['url'][0] # url is only in 0th idx of the list returned, it also includes frequency and closest_dist , etc
        article = article.replace("\"", "'")
    return article , link_url


###############################################################################################################################################################################################################################################################################################################################################################################################
# takes an article and keyword and returns the best para in that article.

def bestParaExtractor(article , keyword):
    keyword = str(keyword)
    text = sent_tokenize(article) #text is now alist containing sentences.
    if len(text) < 5:
        return text
    else:
        lo = 0 
        hi = 3
        max_freq_range = [-1 , -1 , -1] #will contain a list of 3 items : ['freq_maximum' , lo , hi]
        while hi < len(text) :
            freq = freqKeyWord(text[lo : hi + 1] , keyword)
            #print(freq)
            if freq >= max_freq_range[0]:
                max_freq_range = [freq , lo , hi]
            lo = lo + 1
            hi = hi + 1
        if max_freq_range[0] == 0:
            rv_text = "Here is something i found for you :" 
        else:
            lo = max_freq_range[1]
            hi = max_freq_range[2]
            rv_text = str(text[lo]) + str(text[lo + 1]) + str(text[lo + 2]) + str(text[lo + 3]) 
        return rv_text

###############################################################################################################################################################################################################################################################################################################################################################################################
# takes a list of paragraphs, and returns the list of frequency of the keyword associated with the corresponding paragraph.

def freqKeyWord(list_of_4_sentences , keyword):
    freq = 0
    for sentence in list_of_4_sentences:
        tokens = word_tokenize(sentence)
        for idx in range(len(tokens)):
            tokens[idx] = tokens[idx].lower()
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = []
        for word in tokens:
            lemmatized_tokens.append(lemmatizer.lemmatize(word))  
        freq = freq + tokens.count(keyword)    
    return freq   

###############################################################################################################################################################################################################################################################################################################################################################################################
