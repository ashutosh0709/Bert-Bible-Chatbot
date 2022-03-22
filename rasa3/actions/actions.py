#############################################################################################################################################################################################
import os

import time 
time.sleep(50)

from dotenv import load_dotenv
load_dotenv()
ip = os.getenv("instance_ip")
###############################################################################################################################################
###############################################################################################################################################

url = "http://" + ip + ":8002/str" #endpoint where the bertmodel-api is placed.
mismatch_url = "http://" + ip + ":8004/kw" #endpoint where the bertmodel-based mismatch-keyword-replacement is placed.

link_url = ""
last_slot_value = ""
###############################################################################################################################################
##############################################################################################################################################################################################
from nltk.probability import FreqDist
import requests
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize
from nltk.corpus import wordnet
import os
from dotenv import load_dotenv
from pyArango.connection import Connection
from hashlib import new
from keyword import iskeyword
from typing import Any, Text, Dict, List
from urllib import response
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.events import SlotSet
import logging
from nltk.probability import FreqDist
import requests
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize
##############################################################################################################################################################################################################################################################################################################################################################################################################
###############################################################################################################################################################################################################################################################################################################################################################################################################
######################################################################################################################################################################################################################################################################################################################################################################################################
#logging.basicConfig(filename='rasa_actions.log', level=logging.DEBUG , format='%(asctime)s :: %(levelname)s :: %(message)s', force=True)
###################################################################################################################################################################################################
from packages import dac , action_functions
#################################################################################################################################################################################################################
lookup_dict = dac.getListOfAllKeywordsFromDb()
#######################################################################################################################################################
from packages import makeStopword
makeStopword.CreateStopwordEntryInDb()
stopword_dict = action_functions.getStopwordsDict()
##################################################################################################################################################

class one_keyword_api_call(Action):

    def name(self):
        return "action_one_keyword"  

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        global last_slot_value
        global link_url
        slot_value = tracker.get_slot('keyword')                                             # 1

 #       logging.info("---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        print(slot_value)                                                                    # 2


        if slot_value != last_slot_value:                                                     # 4
            last_slot_value = slot_value
            print(slot_value)
            
            if dac.isStopword(slot_value) == True:                                        # 5
                link_url , para = dac.getDataOfStopword(slot_value)
  #              logging.info("The para returned by rasa-actions for " +  slot_value  +  " is : " + para)
                dispatcher.utter_message(para)
                return []
            
            if dac.isKeyword(slot_value) == False:                                     
                if slot_value in lookup_dict:
                    slot_value = lookup_dict.get(slot_value)
                else:
                    dac.write_words_to_db(slot_value)                                              # 7
                    slot_value = action_functions.mismatchFunc(slot_value , mismatch_url)
                    if slot_value == "failed to retrive the bert-assigned keyword for the entered mismatched keyword":
                        dispatcher.utter_message(slot_value)
                        return []
                    if slot_value == "":                                                      
                        dispatcher.utter_message("Please check the spelling!")
                        return []
                print(slot_value)
   
            article , link_url = action_functions.apiFunc(slot_value ,url)    
            if(article == 'NOTHING TO SHOW'):
                link_url = ""    
                return []
            para = action_functions.bestParaExtractor(article , str(slot_value))                                # 9
   #         logging.info("The para returned by rasa-actions for " +  str(slot_value)  +  " is : " + str(para))
            dispatcher.utter_message(para)
        else:
            link_url = ""    
    #        logging.info("The para returned by rasa-actions for " + slot_value + " is : " + "Slot-value not picked up")
            dispatcher.utter_message("Slot-value not picked up")
        return []


########################################################################################################################################

class DisplayLink(Action):
    def name(self):
            return "action_display_link"  

    def run(self,dispatcher,tracker,domain):
        if link_url != "": 
            try:
     #           logging.info("The article-URL returned by rasa-actions is " + str(link_url)) 
                dispatcher.utter_message("Article-Link : " + str(link_url))
            except:
                pass  
        else:
      #      logging.info("The message returned by rasa-actions is " + "Please try again!") 
            dispatcher.utter_message("Please try again!")
        return []    


###################################################################################################################################################################################################
