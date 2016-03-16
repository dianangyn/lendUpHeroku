from flask import Flask, request, redirect, url_for, render_template
import twilio.twiml
import re
from twilio.util import TwilioCapability
from twilio.rest import TwilioRestClient
from forms import webFizzForm

app = Flask(__name__)

default_client = "friend"
caller_id = "+17606426823"


@app.route("/", methods=['POST'])
def home():
    """Respond to incoming requests."""
    resp = twilio.twiml.Response()
    resp.say("Hello. Let's play PhoneFizz.")
    with resp.gather(finishOnKey="#", action="/beginfizz") as g:
        g.say("Please enter a number to play phonefizz then pressed pound.")
    return str(resp)


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


@app.route("/webfizz", methods=['GET', 'POST'])
def webfizz():
    account_sid = "ACd31f04c5fd89bf0fd1a52a36bcb9b50c"
    auth_token = "575f13c3c92ec55501ed32e1776c5184"
    capability = TwilioCapability(account_sid, auth_token)
    application_sid = "AP9087308355771954b1a49f4e9c9636ca"

    capability.allow_client_outgoing(application_sid)
    capability.allow_client_incoming("friend")
    token = capability.generate()

    return render_template('webfizz.html', token=token, form=webFizzForm)


@app.route('/dial', methods=['GET', 'POST'])
def dial():
    dest_number = request.form['phonenumber']
    resp = twilio.twiml.Response()
    if dest_number == "":
        resp.say("Sorry, please enter a phone number.")
        return redirect("/")
    else:
        with resp.dial(callerId=caller_id) as r:
            # If we have a number, and it looks like a phone number:
            if dest_number and re.search('^[\d\(\)\- \+]+$', dest_number):
                r.number(dest_number)
            else:
                r.client(dest_number)

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)

"""
"""