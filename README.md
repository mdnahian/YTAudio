# YTAudio

YouTube Audio Player Alexa Skill

## Installation & Setup

1. `pip install -r requirements.txt`
2. `pip install youtube-dl --upgrade`
3. `python app.py`

## Skill Setup

### Skill Information

1. Set Invocation name to `youtube audio`
2. In Global Fields, set Audio Player to Yes

### Interaction Model

Copy-paste intents.json into Intent Schema and utterances.txt into Sample Utterances.

### Configuration

1. Set Endpoint to HTTPS and set url endpoint
2. Set Account Linking to No

### SSL Certificate

If using ngrok, set NA Endpoint to "My development endpoint is a sub-domain of a domain that has a wildcard certificate from a certificate authority".


### Test

Test the Alexa skill on your Amazon Echo by saying "ask youtube audio to search for _____"