from django.shortcuts import render
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
    phone_number1 = request.POST['number1']
    phone_number2 = request.POST['number2']
    phone_number3 = request.POST['number3']

    if (len(phone_number1)<10):
        return render(request, 'sendmessage/index.html', {
            'error_message': 'You didn\'t enter a phone number.',
        })
    else:
        token = request.POST['stripeToken']
         #Create the charge on Stripe's servers - this will charge the user's card
        try:
          charge = stripe.Charge.create(
             amount=100, # amount in cents, again
             currency="usd",
             source=token,
             description="Just keeping it loopy"
        )
        except stripe.error.CardError, e:
            pass

        try:
            call = client.calls.create(to=phone_number1,
                from_="+15103533372",
                url="http://twimlbin.com/external/5efadf9718cccc0aebb0ea18dd2ad717")
            print call.sid
        except Exception, e:
            print str(e)

        try:
            call = client.calls.create(to=phone_number2,
                from_="+15103533372",
                url="http://twimlbin.com/external/5efadf9718cccc0aebb0ea18dd2ad717")
            print call.sid
        except Exception, e:
            print str(e)

        try:
            call = client.calls.create(to=phone_number3,
                from_="+15103533372",
                url="http://twimlbin.com/external/5efadf9718cccc0aebb0ea18dd2ad717")
            print call.sid
        except Exception, e:
            print str(e)
        return render(request, 'sendmessage/done.html')
