import os

base = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.environ['CHECKEPISODE_SECRET_KEY']

SQLALCHEMY_DATABASE_URI = os.environ['CHECKEPISODE_DATABASE_URI']

HOST = '0.0.0.0'
PORT = 5000

RECAPTCHA_USE_SSL = False
RECAPTCHA_PUBLIC_KEY = os.environ['CHECKEPISODE_RECAPTCHA_PUBLIC_KEY']
RECAPTCHA_PRIVATE_KEY = os.environ['CHECKEPISODE_RECAPTCHA_PRIVATE_KEY']
RECAPTCHA_OPTIONS = {'theme': 'white'}

SECURITY_CONFIRM_EMAIL = True
SECURITY_EMAIL_SENDER = ('CheckEpisode.com', 'noreply@checkepisode.com')
SECURITY_PASSWORD_HASH = 'bcrypt'

LOG_FILE_PATH = os.environ['CHECKEPISODE_LOG_FILE_PATH']
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

del base
del os
