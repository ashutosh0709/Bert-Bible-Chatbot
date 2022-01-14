# ENVIROMENT SET-UP:
 - PYTHON 3.6.8
 
 
 # INSTALLATION:
 - python3 -m pip install --upgrade pip
 - pip install rasa_nlu
 - pip install spacy
 - python3 -m spacy download en_core_web_md
 - Now open python prompt (python3) -> then write:
        >>> import spacy
        >>> nlp=spacy.load('en_core_web_md)
   # ctrl-Z to come out of shell.
- pip install -U rasa_core
- pip install h5py==2.10.0
- pip install sklearn_crfsuite
- pip install tornado
- pip install responses


# RUNNING THE MODEL:

If  we run the program in interactive mode then 3 terminals need to be opened, in detached mode only one will do.
###################################################################################################################
#terminal-1: building and running the rasa model on port 5800

python3 nlu_training.py
python3 -m rasa_core.train -d domain.yml -s data/stories.md -o models/dialogue -c policy.yml
python3 -m rasa_core.run --enable_api -d models/dialogue -u models/nlu/default/current --cors "*" -o out.log --endpoints endpoints.yml --port 5800 --credentials credentials.yml

###################################################################################################################
#terminal-2: running the chat-app on port 8000

python3 web_app.py

###################################################################################################################
#terminal-3:running the actions server on port 5055

python3 -m rasa_core_sdk.endpoint --actions actions

###################################################################################################################
