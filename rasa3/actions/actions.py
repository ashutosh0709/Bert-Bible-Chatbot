# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from urllib import response

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.events import SlotSet


##########################################################################
from nltk.probability import FreqDist
import requests
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize

import logging
logging.basicConfig(filename='rasa_actions.log', level=logging.DEBUG , format='%(asctime)s :: %(levelname)s :: %(message)s', force=True)


###########################################################################
url = "http://44.197.194.109:8002/str" #endpoint where the bertmodel-api is placed.
link_url = ""

last_slot_value = ""
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





class one_keyword_api_call(Action):

    def name(self):
        return "action_one_keyword"  

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        global last_slot_value
        global link_url
        #SlotSet("keyword", "defalt_fallback_value")
        slot_value = tracker.get_slot('keyword')
       # slot_value =  tracker.latest_message['intent'].get('name')
       # print("this is the obj of slot value -> " , type(slot_value) , "thi is slot value -> " , slot_value)
      #  print(slot_value[-6:]) #to check if the last 6 letters of the intent name is "intent" - for verifying inen validation before api-call. Not yet implemented!
      #  print(slot_value[ : -7]) #will remove the last "_intent" from intent name and we will get the keyword.
        print(slot_value)
        # if slot_value[-6:] != "intent":
        #     dispatcher.utter_message("Sorry, I did not get you")
        #     global link_url
        #     link_url = ""   
        #     return []


       # slot_value = slot_value[ : -7]
       
        logging.info("---------------------------------------------------------------------------------------------------------------------------------------")
        logging.info("The slot-keyword picked up by NLU is : " + slot_value)

        if slot_value != last_slot_value:
            last_slot_value = slot_value
            print(slot_value)
            article = apiFunc(slot_value)
            print("type - > " , type(article))
            print(article)
            if(article == 'NOTHING TO SHOW'):
                link_url = ""    
                return []
            para = bestParaExtractor(article , str(slot_value))
            logging.info("The para returned by rasa-actions for " +  slot_value  +  " is : " + para)

            print(para)
            dispatcher.utter_message(para)
        else:
            link_url = ""    
            logging.info("The para returned by rasa-actions for " + slot_value + " is : " + "Slot-value not picked up")
            dispatcher.utter_message("Slot-value not picked up")
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
                logging.info("The article-URL returned by rasa-actions is " + str(link_url))
                dispatcher.utter_message("Article-Link : " + str(link_url))
            except:
                pass  
        else:
            logging.info("The message returned by rasa-actions is " + "Please try again!")
            dispatcher.utter_message("Please try again!")
        return []    


###################################################################################################################################################################################
# class test_function_actions_file(Action):

#     def name(self):
#         return "action_display"  

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         slot_value =  tracker.latest_message['intent'].get('name')
#         print("this is slot value -> " , slot_value)
#         print(slot_value[-6:]) #to check if the last 6 letters of the intent name is "intent" - for verifying inen validation before api-call. Not yet implemented!
#         print(slot_value[ : -7]) #will remove the last "_intent" from intent name and we will get the keyword.
#         if slot_value[-6:] != "intent":
#             dispatcher.utter_message("Sorry, I did not get you")
#             return []

#         slot_value = slot_value[ : -7]
        
#         if slot_value != None:
#             print(slot_value)
#             dispatcher.utter_message(slot_value)
#         else:
#             dispatcher.utter_message("None came as the intent value!")
#         return []  














































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
        return[]   


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




















