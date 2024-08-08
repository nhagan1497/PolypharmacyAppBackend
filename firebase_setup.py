import firebase_admin
from firebase_admin import credentials, auth
import os
import json

try:
    cred = credentials.Certificate(os.path.join(os.getcwd(), 'firebase_service_cred.json'))
except json.JSONDecodeError:
    cred = credentials.Certificate(json.loads(os.environ['FIREBASE_SERVICE_CRED']))

firebase_admin.initialize_app(cred)
