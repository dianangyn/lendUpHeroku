from flask import Flask
import twilio.twiml

app = Flask(__name__)

@app.route('/')
def home():
    resp = twilio.twiml.Response()
    resp.say("Hello. Let's play PhoneFizz. Enter a number then press star.")
    return str(resp)


@app.route("/menu", methods=['POST'])
def menu():
    """Respond to incoming requests."""

    selected_option = request.form['Digits']
    option_actions = {'1': _give_instructions,
                      '2': _play_phonefizz}

    if option_actions.has_key(selected_option):
        response = twilio.twiml.Response()
        option_actions[selected_option](response)
        return twiml(response)
    return _redirect_menu()


@app.route("/beginfizz", methods=['POST'])
def beginfizz():
    """Handle key press from a user."""
    digit_pressed = request.form['Digits']
    resp = twilio.twiml.Response()
    resp.say("beginning of the game")
    if digit_pressed == "0":
        resp.say("Sorry, please enter a number within the range.")
        return redirect("/")
    else:
        return phonefizz(digit_pressed)
    return str(resp)

def _give_instructions(response):
    response.say("To play phonefizz, enter a number on your number pad." +
                 "Our game will return the phonefizz response for your number",
                 voice="alice", language="en-GB")

    response.say("Thank you for playing.")

    response.hangup()
    return response


def _play_phonefizz(reponse):
    with response.gather(action=url_for('beginfizz'), method="POST") as g:
        g.say("Please enter a number to play phonefizz ",
              voice="alice", language="en-GB", loop=2)
    return response

def _redirect_menu():
    response = twilio.twiml.Response()
    response.say("Returning to the main menu", voice="alice", language="en-GB")
    response.redirect(url_for('menu'))

    return twiml(response)


if __name__ == "__main__":
    app.run(debug=True)
