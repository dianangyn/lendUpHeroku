from flask import Flask
import twilio.twiml

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def phoneFizz():
    """Respond to incoming requests."""
    resp = twilio.twiml.Response()
    resp.say("Hello. Let's play PhoneFizz. Enter a number then press star.")
    resp.gather(finishOnKey="*", action="/beginfizz", method="POST")
    print(resp)
    return str(resp)


@app.route("/beginfizz", methods=['POST'])
def beginfizz():
    """Handle key press from a user."""
    # Get the digit pressed by the user
    resp = twilio.twiml.Response()
    resp.say("beginning of the game")
    digit_pressed = request.form['Digits']  # returns a string
    '''
    try:
        digit_pressed = int(digit_pressed)
        resp.say("tried to create the create the input to an integer")
    except:
        resp.say("Sorry, that's not a real number.")
        return redirect("/")
    # catch non number responses
    '''
    if digit_pressed == "0":
        resp.say("Sorry, please enter a number within the range.")
        return redirect("/")
    else:
        for x in range(1, int(digit_pressed)):
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
