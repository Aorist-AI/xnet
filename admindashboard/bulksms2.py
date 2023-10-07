import africastalking

#initialize the sdk
username = "PaulSaul"
api_key = "daa4635872bc8bbae5549811411fd506224c991f37a3f311a31cad867d77864c"
africastalking.initialize(username, api_key)


def init_sms():
    #initialize the service, in our case, SMS
    sms = africastalking.SMS
    return sms


#USE THE SERVICE
def on_finish(error, response):
    if error is not None:
        raise error
    print(response)


#sms.send("Bulk SMS sending, testing phase 2. From PaulWababu", recipients, callback=on_finish)
def process_sms(message, phonenumbers):
    recipients = phonenumbers
    message = message

    return init_sms().send(message, recipients, callback=on_finish)


if __name__ == '__main__':

    process_sms(message, recipients)