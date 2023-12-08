import os
from dotenv import load_dotenv

load_dotenv()

# email

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# postgresql

NAME_DATABASE = os.getenv('NAME_DATABASE')
USER_DATABASE = os.getenv('USER_DATABASE')
PASSWORD_DATABASE = os.getenv('PASSWORD_DATABASE')
HOST_DATABASE = os.getenv('HOST_DATABASE')