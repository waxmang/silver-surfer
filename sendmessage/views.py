from django.shortcuts import render, redirect
from django.http import HttpResponse
from django_twilio.decorators import twilio_view
from django.conf import settings

from twilio.twiml import Response
from twilio.rest import TwilioRestClient

import stripe

client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

# Create your views here.
def index(request):
    return render(request, 'sendmessage/index.html', {})

def send(request):
    phone_number = request.POST['number']
    if (len(phone_number)<5):
        return render(request, 'sendmessage/index.html', {
            'error_message': 'You entered an invalid phone number.',
        })
    else:
        try:
            call = client.calls.create(to=phone_number,
                from_="+15103533372",
                url="http://twimlbin.com/external/5efadf9718cccc0aebb0ea18dd2ad717")
            print call.sid
        except Exception, e:
            print str(e)
        return render(request, 'sendmessage/done.html')

def donate(request):
    token = request.POST['stripeToken']
     # Create the charge on Stripe's servers - this will charge the user's card
    try:
      charge = stripe.Charge.create(
        amount=500, # amount in cents, again
        currency="usd",
        source=token,
        description="Just keeping it loopy"
    )
    except stripe.error.CardError, e:
      # The card has been declined
        pass

    return render(request, 'sendmessage/done.html')
