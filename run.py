from flask import Flask, request, redirect, render_template, url_for, jsonify
import twilio.twiml
from forms import PhoneForm
from twilio.rest import TwilioRestClient


app = Flask(__name__)
WTF_CSRF_ENABLED = True
app.config.from_pyfile('config.py')


@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    """Respond to incoming requests."""
    resp = twilio.twiml.Response()
    resp.say("Hello. Let's play PhoneFizz.")
    with resp.gather(finishOnKey="#", action="/beginfizz") as g:
        g.say("Please enter a number to play phonefizz then press pound.")
    return str(resp)

"""
@app.route("/play", methods=['GET','POST'])
def play():
    resp = twilio.twiml.Response()
    with resp.gather(finishOnKey="#", action="/beginfizz") as g:
        g.say("Please enter a number to play phonefizz then press pound.")
    return str(resp)
"""


@app.route("/beginfizz", methods=['GET', 'POST'])
def beginfizz():
    """Handle key press from a user."""
    digit_pressed = request.form['Digits']  # returns a string
    resp = twilio.twiml.Response()
    if digit_pressed == "0":
        resp.say("Sorry, please enter a number within the range.")
        return redirect("/")
    else:
        resp.say(phonefizz(int(digit_pressed)))
    return str(resp)


@app.route("/webfizz", methods=['GET', 'POST'])
def webfizz():
    return render_template('/web.html', form=PhoneForm)


def phonefizz(inp):
    output = ""
    for x in range(1, inp+1):
        if x % 5 == 0 and x % 3 == 0:
            output += "fizzbuzz "
        elif x % 5 == 0:
            output += "fizz "
        elif x % 3 == 0:
            output += "buzz "
        else:
            output += str(x)+" "
    return output


@app.route('/dial', methods=['POST'])
def web_dial():
    phone_number = '+18586108538'
    print phone_number
    try:
        twilio_client = TwilioRestClient(app.config['TWILIO_ACCOUNT_SID'],
                                         app.config['TWILIO_AUTH_TOKEN'])
    except Exception as e:
        msg = 'Missing configuration variable: {0}'.format(e)
        return jsonify({'error': msg})
    try:
        call = twilio_client.calls.create(from_=app.config['TWILIO_CALLER_ID'],
                                   to=phone_number,
                                   url=url_for('.home', _external=True))
    except Exception as e:
        app.logger.error(e)
        return jsonify({'error': str(e)})

    return jsonify({'message': 'Call incoming!', 'sid': call.sid})


if __name__ == "__main__":
    app.run(debug=True)