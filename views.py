from flask import Flask, request, redirect, render_template
import twilio.twiml
from forms import webFizzForm

app = Flask(__name__)


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
    return render_template('/webfizz.html', form=webFizzForm)


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


"""@app.route('/dial', methods=['GET', 'POST'])
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
                resp.say("Sorry, that is an invalid number.")

    return str(resp)"""


if __name__ == "__main__":
    app.run(debug=True)