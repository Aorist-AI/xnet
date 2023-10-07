from django.http import HttpResponse, JsonResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from .mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
from django.views.decorators.csrf import csrf_exempt
from .models import MpesaPayment
from useraccess.models import Packages
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import ListView
from django.shortcuts import render
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from useraccess.views import check_user_status_before_insert


def getAccessToken(request):
    consumer_key = 'WKtrYFr35GVoI2fBWngoet2fs7T0KLa9'
    consumer_secret = 'oUZYG6fQFVq4YO9z'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL,
                     auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return HttpResponse(validated_mpesa_access_token)


def lipa_na_mpesa_online(request):
    data = {
        "username": cache.get("username"),
        "phone_number": cache.get("phonenumber"),
        "amount": request.GET.get("price"),
        "access_period": request.GET.get("access_period"),
        "bundle": request.GET.get("bundle"),
        "speed": request.GET.get("speed"),
        "bundle_id": request.GET.get("bundle_id")
    }
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        # "META": request.META,
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": data["amount"],
        "PartyA": 254797584194,  # replace with your phone number to get cash
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber":
        254700011464,  # replace with your phone number to get stk push
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "PaulWababu",
        "TransactionDesc": "Donate to PaulWababu!"
    }
    response = requests.post(api_url, json=request, headers=headers)
    check_user_status_before_insert(data)
    return HttpResponseRedirect("/profile")


@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {
        "ShortCode": LipanaMpesaPpassword.Test_c2b_shortcode,
        "ResponseType": "Completed",
        "ConfirmationURL": "https://fa37b283.ngrok.io/api/v1/c2b/confirmation",
        "ValidationURL": "https://fa37b283.ngrok.io/api/v1/c2b/validation"
    }
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)


@csrf_exempt
def call_back(request):
    pass


@csrf_exempt
def validation(request):
    context = {"ResultCode": 0, "ResultDesc": "Accepted"}
    return JsonResponse(dict(context))


@csrf_exempt
def confirmation(request):
    mpesa_body = request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    payment = MpesaPayment(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['LastName'],
        middle_name=mpesa_payment['MiddleName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        organization_balance=mpesa_payment['OrgAccountBalance'],
        type=mpesa_payment['TransactionType'],
    )
    payment.save()
    context = {"ResultCode": 0, "ResultDesc": "Accepted"}
    return JsonResponse(dict(context))
