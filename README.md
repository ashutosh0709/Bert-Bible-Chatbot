# With Docker Instructions:
###########################################################################################################

# BERT Instructions: Run the following commands:-> Open BERT-API EC2 instance:->
#####################################################################################
* sudo su  
* docker run -d -p 8002:8002 clientapi:v1

##################################################################################
# RASA Instructions:
##################################################################################

* docker rm /actionserver -> we need to remove it since the container ran last time.
* docker run -d -p 5055:5055 --net networkaction --name actionserver actionimage 
* cd /home/ubuntu/rasa_3/alexa_bible_skill/rasa3
* docker run --user 1000 -d -v $(pwd):/app -p 5005:5005 --net networkaction rasa/rasa:3.0.4-full run --enable-api --cors="*"
* docker run -d -p 8005:8005 rasaui:v1

:-> Now we can open the url :-> 'rasa-ip':8005 , and the UI will open up as a button on the right bottom of the screen.
:-> To connect on whatsapp, save a new contact in your phone for the number : '+1 415 523 8886', and send the message 'join letter-wood'(without quotes). Now you are connected for 3 days. After 3 days, you will have to reconnect in the same way.

###########################################################################################################
