
import random
import requests

# Function to generate a random 4-digit OTP code
def generate():
    return str(random.randint(1000, 9999))

# Function to send a custom SMS with OTP
def send(code,phone):
    print('here')
    try:
        print(phone.data)
        
        to_phone = phone.data['phoneNumber']
        # Call an api and send parameter to it
        r = requests.get(
            "http://api.sparrowsms.com/v2/sms/",
            params={'token' : 'v2_Rri05e6U3XkCcnmjeOnfxdDzAqz.dY9a',
                  'from'  : 'TheAlert',
                  'to'    : to_phone,
                  'text'  : f'Dear User,Please use OTP {code} for the verification.'})

        status_code = r.status_code
        response = r.text
        response_json = r.json()
        print(response)
        
        

        print(f"OTP sent successfully to {to_phone}: {code}")

        
    except Exception as e:
        print(f"Error sending OTP: {str(e)}")



