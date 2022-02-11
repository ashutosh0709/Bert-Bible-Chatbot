#### Please follow the BERT instructions and then RASA instructions:


####################################################################################
# BERT Instructions:
####################################################################################
1. From /home/ubuntu/ , cd into ->  vi 
2. run -> vi app.js, and edit the first line of the file with the new public IP of the BERT machine-instance. exit vi by ':wq' 
3. Now cd into- /home/ubuntu/bible_api_rasa/docker_version
3. build -> sudo docker build -t clientapi:v1 -f Dockerfile.capi .
2. run -> sudo docker run -p 8002:8002 clientapi:v1

















#####################################################################################
# RASA Instructions:
#####################################################################################
0. make change is rasa actions file.
---> cd into '/home/ubuntu/rasa_3/alexa_bible_skill/rasa3/actions'

vi actions.py
update url value(located just below the from and import statements) with the bert machine's api





1. Be in /home/ubuntu and run ->    source venv/bin/activate
2. Now change directory to - >  /home/ubuntu/rasa_3/alexa_bible_skill/rasa3    and run the following commands:
3. Open python prompt by typing->  python3
         *Now run the following commands:
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt') 

Now come out of python3 prompt by ctrl+z

3. run ->  rasa run actions
4. In another terminal(duplicate-session for rasa ec-2),
1. Be in /home/ubuntu and run ->    source venv/bin/activate
 Now change directory to ->  /home/ubuntu/rasa_3/alexa_bible_skill/rasa3 , and run  command -> rasa run --enable-api --cors="*" 


Now open another terminal(duplicate session for rasa-ec2),
Be in /home/ubuntu and run ->    source venv/bin/activate
 cd into :-> /home/ubuntu/rasa_3/alexa_bible_skill/ui , and run command :->
python3 web_app.py


:-> Now we can open the url :-> 'rasa-ip':8005 and the UI will open up as a button on the right bottom of the screen.



Now we can type our query as input like 'bible on [kings], what does christianity say about [kings], jesus on [kings], etc' where we can type in any of the 200 keywords inplace of [kings]. 
