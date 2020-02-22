# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'ACcee7a1027e6128667c2460db074b3875'
auth_token = '07b86398710cd17e802789588f7fae9a'
client = Client(account_sid, auth_token)

message = client.messages.create(
    body='Testing From Console!',
    from_='+13475543716',
    to='+12562428080'
)

print(message.sid)
