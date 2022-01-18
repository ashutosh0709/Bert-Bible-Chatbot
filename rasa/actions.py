from os import link
from typing import Dict, Text, Any, List, Union, Optional

from rasa_core_sdk import Tracker
from rasa_core_sdk.executor import CollectingDispatcher
#from rasa_core.actions.action import Action
from rasa_core_sdk import Action
from rasa_core_sdk.forms import FormAction
from rasa_core_sdk.events import SlotSet


###########################################################################
from nltk.probability import FreqDist
import requests
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize
############################################################################
url = "http://44.193.196.134:8002/str" #endpoint where the bertmodel-api is placed.
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





class apisearch(Action):

    def name(self):
        return "action_question_two"  

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        #SlotSet("keyword", "defalt_fallback_value")
        slot_value = tracker.get_slot('keyword')
        
        if slot_value != None:
            print(slot_value)
            article = apiFunc(slot_value)
            para = bestParaExtractor(article , str(slot_value))
            dispatcher.utter_message(para)
        else:
            global link_url
            link_url = ""    
        return[SlotSet("keyword", None)]   


class DisplayLink(Action):
    def name(self):
            """name of the custom action"""
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































########################################################################################################################################

class expressionssearch(Action):

    def name(self):
        return "action_expressions_intent"  

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        slot_value = tracker.get_slot('expressions_slot')
        print(slot_value)
        
        article = apiFunc(slot_value)
        para = bestParaExtractor(article , str(slot_value))

        dispatcher.utter_message(para)
        return []    



class ResetSlot(Action):

    def name(self):
        return "action_reset_slot"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("keyword", None)]
