# (A) SETUP INSTRUCTIONS:

* in -> '/home/ubuntu/' directory on AWS-EC2, git pull  https://github.com/ashutosh0709/alexa_bible_skill.git 


###########################################################################################

# (B) RUNNING INSTRUCTIONS:
## (B.1) BERT Instructions, to start the BERT-APIS : 
* FOLLOW THE '(C) RUNNING INSTRUCTIONS' OF BERT-CODE.
* cd /home/ubuntu/alexa_bible_skill/rasa3
* docker run --user 0 -v $(pwd):/app rasa/rasa:3.0.4-full train





## (B.2) RASA Instructions:
* sudo su
* cd /home/ubuntu/alexa_bible_skill/rasa3/actions
* vi .env  :-> Now create the .env file using 'env_creation_file.txt' -> present in the repo itself. Now update EC2-INSTANCE-IP-OF-BERT-MACHINE in the first line.   ('wq' for saving and exiting vi).
* cd /home/ubuntu/alexa_bible_skill/rasa3
* docker build -t actionimage -f Dockerfile.actions .
* docker network create networkaction
* docker rm /actionserver -> we need to remove it since the container ran last time.
* cd /home/ubuntu/alexa_bible_skill/rasa3
* docker run -d -p 5055:5055 --net networkaction --name actionserver actionimage 
* cd /home/ubuntu/alexa_bible_skill/rasa3
* docker run --user 1000 -d -v $(pwd):/app -p 5005:5005 --net networkaction rasa/rasa:3.0.4-full run --enable-api --cors="*"
* cd /home/ubuntu/alexa_bible_skill/ui/templates
* vi index.html :-> Goto the 4th line from BOTTOM and change the IP in 'host=' to rasa-instance's-ip.
* cd /home/ubuntu/alexa_bible_skill/ui
* docker build -t rasaui:v1 .
* docker run -d -p 8005:8005 rasaui:v1

:-> Now we can open the url :-> 'rasa-ip':8005 , and the UI will open up as a button on the right bottom of the screen.













