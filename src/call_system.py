from twilio.rest import Client

ACCOUNT_SID = "your-twilio-sid"
AUTH_TOKEN = "your-twilio-auth-token"
FROM_NUMBER = "your-twilio-number"

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def make_call(to_number):
    """Makes a phone call and plays a message."""
    call = client.calls.create(
        twiml='<Response><Say>Hello, this is your assistant.</Say></Response>',
        to=to_number,
        from_=FROM_NUMBER
    )
    return call.sid