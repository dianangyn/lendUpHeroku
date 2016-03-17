from flask import Flask, request, redirect, render_template
import twilio.twiml
from forms import webFizzForm

app = Flask(__name__)


@app.route("/", methods=['GET','POST'])
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


if __name__ == "__main__":
    app.run(debug=True)