import random
import datetime

# function to generate a random string of length 6 with characters from a-zA-Z0-9
def get_random_string(length):  
    possible_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    random_url = "".join(random.choice(possible_characters) for i in range(length))
    return f"{random_url}"

def generate_otp():
    return random.randint(100000, 999999)

def send_email_with_otp(email, otp):
    # send email with otp using aws ses
    pass
    