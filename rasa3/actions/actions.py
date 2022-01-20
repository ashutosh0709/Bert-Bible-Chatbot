# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


###########################################################################
from nltk.probability import FreqDist
import requests
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize
############################################################################
url = "http://localhost:8002/str" #endpoint where the bertmodel-api is placed.
link_url = ""

############################################################################
def apiFunc(text):
    global link_url
    link_url = ""
    data = {'text':text}
    r = requests.get(url=url , data=data)
    if r.status_code == 400:
        article = "Sorry, I did not understand."
    else:    
        rv = r.json()
        article = rv['para']
        link_url = rv['url'][0] # url is only in 0th idx of the list returned, it also includes frequency and closest_dist , etc
        article = article.replace("\"", "'")
    return article
############################################################################
def bestParaExtractor(article , keyword):
    keyword = str(keyword)
    text = sent_tokenize(article) #text is now alist containing sentences.
    # print(len(text))
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
        #print("frequency of keyword : " + keyword + " : " + str(max_freq_range[0]))
        if max_freq_range[0] == 0:
            rv_text = "Here is something i found for you :" 
        else:
            lo = max_freq_range[1]
            hi = max_freq_range[2]
            rv_text = text[lo] + text[lo + 1] + text[lo + 2] + text[lo + 3] 
        return rv_text


def freqKeyWord(list_of_4_sentences , keyword):
    freq = 0
    #print("keyword : " + str(keyword))
    for sentence in list_of_4_sentences:
        tokens = word_tokenize(sentence)
        for idx in range(len(tokens)):
            tokens[idx] = tokens[idx].lower()
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = []
        for word in tokens:
            lemmatized_tokens.append(lemmatizer.lemmatize(word))
        # print("#########################################################################################################################")
        # print(lemmatized_tokens)
        # print("#######################################################################################################################")    
        freq = freq + tokens.count(keyword)    
        # print(tokens.count(keyword)) 
        # print("short freq : " , freq)
        # print(type(keyword))
        # print(type(tokens[2])) # erro here for now, remove it!
    return freq   
############################################################################







class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []


#######################################################################################################################################
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


class one_keyword_api_call(Action):

    def name(self):
        return "action_one_keyword"  

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        #SlotSet("keyword", "defalt_fallback_value")
        #slot_value = tracker.get_slot('kings_slot')
        slot_value =  tracker.latest_message['intent'].get('name')
        print("this is the obj of slot value -> " , type(slot_value) , "thi is slot value -> " , slot_value)
        print(slot_value[-6:]) #to check if the last 6 letters of the intent name is "intent" - for verifying inen validation before api-call. Not yet implemented!
        print(slot_value[ : -7]) #will remove the last "_intent" from intent name and we will get the keyword.
        slot_value = slot_value[ : -7]
        
        if slot_value != None:
            print(slot_value)
            article = apiFunc(slot_value)
            para = bestParaExtractor(article , str(slot_value))
            dispatcher.utter_message(para)
        else:
            global link_url
            link_url = ""    
        #return[SlotSet("kings_slot", None)]
        return []  




#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
########################################################################################################################################

class DisplayLink(Action):
    def name(self):
            return "action_display_link"  

    def run(self,dispatcher,tracker,domain):
        if link_url != "": 
            try:
                dispatcher.utter_message("Article-Link : " + str(link_url))
            except:
                pass  
        else:
            dispatcher.utter_message("Sorry, I did not get you.")
        return []    


