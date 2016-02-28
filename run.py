from flask import Flask
import twilio.twiml

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def phoneFizz():
    """Respond to incoming requests."""
    resp = twilio.twiml.Response()
    resp.say("Hello.")
    with resp.gather(finishOnKey="#", action="/beginfizz", method="POST") as g:
        g.say("Let's play PhoneFizz. Enter a number then press pound.")

    return str(resp)

@app.route("/beginfizz", methods=['GET', 'POST'])
def beginfizz():
    """Handle key press from a user."""
    # Get the digit pressed by the user
    digit_pressed = request.values.get('Digits', None) # returns a string
    resp = twilio.twiml.Response()
    resp.say(digit_pressed)

    try:
        digit_pressed = int(digit_pressed)
        resp.say("tried to create the create the input to an integer")
    except:
        resp.say("Sorry, that's not a real number.")
        return redirect("/")
    # catch non number responses
    if digit_pressed == 0:
        resp.say("Sorry, please enter a number within the range.")
        return redirect("/")

    for x in range(1,digit_pressed):
        playfizz(x)

    return str(resp)

def playfizz(currentNum):
    if currentNum % 3 == 0:
        resp.say("Fizz")
    elif currentNum % 5 == 0:
        resp.say("Buzz")
    else:
        resp.say(currentNum)

if __name__ == "__main__":
    app.run(debug=True)
