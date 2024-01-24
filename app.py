from flask import Flask, request, redirect, session, render_template
from requests_oauthlib import OAuth2Session
import os, logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# This secret key is used for securely signing the session
app.secret_key = os.urandom(24)

# Your Fitbit OAuth credentials
CLIENT_ID = '23RTSX'
CLIENT_SECRET = 'b058974f738bed3682a083633aac9795'
REDIRECT_URI = 'http://localhost:8080/redirect'

# Disable SSL requirement for local testing
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Fitbit OAuth endpoints
AUTHORIZATION_BASE_URL = 'https://www.fitbit.com/oauth2/authorize'
TOKEN_URL = 'https://api.fitbit.com/oauth2/token'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/redirect')
def redirect_page():
    """ Handle the response from Fitbit """
    fitbit = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
    token = fitbit.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET,
                               authorization_response=request.url)
    session['oauth_token'] = token
    logging.debug("Fetched and stored token: %s", token)
    return 'You are successfully logged in with Fitbit!'

@app.route('/fetch-steps')
def fetch_steps():
    logging.debug("Fetching steps data with token: %s", session.get('oauth_token'))
    fitbit = OAuth2Session(CLIENT_ID, token=session.get('oauth_token'))
    response = fitbit.get('https://api.fitbit.com/1/user/-/activities/steps/date/today/1w.json')
    return response.json()

@app.route('/fetch-heart-rate')
def fetch_heart_rate():
    logging.debug("Fetching heart rate data with token: %s", session.get('oauth_token'))
    fitbit = OAuth2Session(CLIENT_ID, token=session.get('oauth_token'))
    response = fitbit.get('https://api.fitbit.com/1/user/-/activities/heart/date/today/1w.json')
    return response.json()

@app.route('/fetch-sleep')
def fetch_sleep():
    logging.debug("Fetching sleep data with token: %s", session.get('oauth_token'))
    fitbit = OAuth2Session(CLIENT_ID, token=session.get('oauth_token'))
    response = fitbit.get('https://api.fitbit.com/1.2/user/-/sleep/date/today/1w.json')
    return response.json()

if __name__ == '__main__':
    app.run(debug=True, port=8080)
