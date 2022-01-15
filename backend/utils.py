import random
import datetime


def get_random_url():
    # generate a random string of length 6 with characters from a-zA-Z0-9
    possible_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    random_url = "".join(random.choice(possible_characters) for i in range(6))
    return "atm.io/" + random_url


def convert_to_python_datetime(date_in):
  date_processing = date_in.replace('T', '-').replace(':', '-').split('-')
  date_processing = [int(v) for v in date_processing]
  date_out = datetime.datetime(*date_processing)
  return date_out