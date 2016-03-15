from flask import Flask, request, redirect, url_for, render_template
import twilio.twiml
from .forms import webFizzForm

app = Flask(__name__)

"""
from twilio.rest import TwilioRestClient

# Get these credentials from http://twilio.com/user/account
account_sid = "ACd31f04c5fd89bf0fd1a52a36bcb9b50c"
auth_token = "575f13c3c92ec55501ed32e1776c5184"
client = TwilioRestClient(account_sid, auth_token)"""


@app.route("/", methods=['GET', 'POST'])
def home():
    """Respond to incoming requests."""
    form = webFizzForm()
    resp = twilio.twiml.Response()
    resp.say("Hello. Let's play PhoneFizz.")
    with resp.gather(finishOnKey="#", action="/beginfizz") as g:
        g.say("Please enter a number to play phonefizz then pressed pound.")
    return render_template('webfizz.html', form = form, reponse=str(resp))

"""
@app.route("/", methods =['GET'])
def home():
    return
"""

@app.route("/beginfizz", methods=['GET', 'POST'])
def beginfizz():
    """Handle key press from a user."""
    digit_pressed = request.form['Digits'] # returns a string
    resp = twilio.twiml.Response()
    if digit_pressed == "0":
        resp.say("Sorry, please enter a number within the range.")
        return redirect("/")
    else:
        resp.say(phoneFizz(int(digit_pressed)))
    return str(resp)


def phoneFizz(input):
    output = ""
    for x in range(1, input+1):
        if x % 5 == 0 and x % 3 == 0:
            output += ("fizzbuzz ")
        elif x % 5 == 0:
            output += ("fizz ")
        elif x % 3 == 0:
            output += ("buzz ")
        else:
            output += str(x)+" "
    return output


def _play_phonefizz(response):
    with response.gather(action=url_for('beginfizz'), method="POST") as g:
        g.say("Please enter a number to play phonefizz ",
              voice="alice", language="en-GB", loop=2)
    return response


@app.route("/webfizz", methods=['GET', 'POST'])
def webfizz():
    to_call = request.form['phonenumber']
    resp = twilio.twiml.Response()
    if to_call == "":
        resp.say("Sorry, please enter a phone number.")
        return redirect("/")
    else:
        call = client.calls.create(to=to_call,
                           from_="+17606426823",
                           url="/beginfizz")
    return str(resp)

# Make the call

print call.sid

if __name__ == "__main__":
    app.run(debug=True)