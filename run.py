from flask import Flask
import twilio.twiml

app = Flask(__name__)

@app.route("/", methods=['POST'])
def menu():
    """Respond to incoming requests."""
    resp = twilio.twiml.Response()
    resp.say("Hello. Let's play PhoneFizz.")
    with resp.gather(numDigits=1, action="/hello") as g:
        g.say("Please enter a number to play phonefizz then pressed pound.")
    return str(resp)

@app.route("/hello", methods=['GET', 'POST'])
def handle_key():
    """Handle key press from a user."""
    # Get the digit pressed by the user
    digit_pressed = request.form['Digits'] # returns a string
    if digit_pressed == "1":
        resp = twilio.twiml.Response()
        resp.say("Thank you for pressing 1. Goodbye.")
        return str(resp)
    # If the caller pressed anything but 1, redirect them to the homepage.
    else:
        return redirect("/")



@app.route("/beginfizz", methods=['GET', 'POST'])
def beginfizz():
    """Handle key press from a user."""
    digit_pressed = request.values.get('Digits', None)
    resp = twilio.twiml.Response()
    resp.say("beginning of the game")
    if digit_pressed == "0":
        resp.say("Sorry, please enter a number within the range.")
        return redirect("/")
    else:
        return phoneFizz(digit_pressed)
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


def _play_phonefizz(reponse):
    with response.gather(action=url_for('beginfizz'), method="POST") as g:
        g.say("Please enter a number to play phonefizz ",
              voice="alice", language="en-GB", loop=2)
    return response

if __name__ == "__main__":
    app.run(debug=True)
