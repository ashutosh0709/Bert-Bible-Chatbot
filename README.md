# Please follow the BERT instructions and then RASA instructions:


############################################################################################
# BERT Instructions: Run the following commands:-> Open BERT-API EC2 instance:->
############################################################################################
* sudo su  
* cd /home/ubuntu/bible_api_rasa/docker_version/ui/static/javascript
* vi app.js :-> Edit the first line of the file with the new public IP of the BERT machine-instance(command in vi is 'i' for insert). Exit vi by pressing escape and then ':wq' 
* cd /home/ubuntu/bible_api_rasa/docker_version
* docker build -t clientapi:v1 -f Dockerfile.capi .
* docker run -p 8002:8002 clientapi:v1


############################################################################################
# RASA Instructions: Will have 3 terminals.(3 duplicate sessions, or -d will also work)
############################################################################################
################################################
## TERMINAL-1: Run the following commands:
################################################
* sudo su
* cd /home/ubuntu/rasa_3/alexa_bible_skill  
* If needed, then only run(No need to run currently) :-> git pull  https://github.com/ashutosh0709/alexa_bible_skill.git
* cd /home/ubuntu/rasa_3/alexa_bible_skill/rasa3/actions
* vi actions.py  :-> Now update url(located just below the 'from' and 'import' statements) with the bert machine's IP ('wq' for saving and exiting vi).
* cd /home/ubuntu 
* source venv/bin/activate
* cd /home/ubuntu/rasa_3/alexa_bible_skill/rasa3 
* rasa run actions


###############################################
## TERMINAL-2: Run the following commands:
###############################################
* sudo su
* source venv/bin/activate
* cd /home/ubuntu/rasa_3/alexa_bible_skill/rasa3 
* rasa run --enable-api --cors="*" 


###############################################
## TERMINAL-3: Run the following commands:
###############################################
* sudo su
* source venv/bin/activate
* cd /home/ubuntu/rasa_3/alexa_bible_skill/ui/templates  
* vi index.html  :-> Goto the 4th line from BOTTOM and change the IP in 'host=' to rasa-ip.
* cd /home/ubuntu/rasa_3/alexa_bible_skill/ui 
* python3 web_app.py


#######################################################################################

:-> Now we can open the url :-> 'rasa-ip':8005 ,  and the UI will open up as a button on the right bottom of the screen.

#######################################################################################
Some working Query Examples: 

01. bible on [kings]
02. what does christianity say about [kings]
03. what jesus said about [kings]
04. what does the bible say about [kings]
05. what does the bible have to say on [kings]
06. what does the bible say on [kings]
07. bible on [kings]
08. what does christianity say about [kings]
09. what does christianity have to say on [kings]
10. what jesus said about [kings]
11. how is [kings] explained in christianity?
12. what jesus spoke about [kings]
13. what christianity says on [kings]
14. christianity on [kings]
15. jesus on [kings]
16. [kings] in bible
17. [kings] as explained by bible
18. [kings] as said by jesus

########################################################################################
- The updated list of keywords currently embedded into the model is in '200_keywords_list.txt' in the root directory of the project.
