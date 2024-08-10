import firebase_admin
from firebase_admin import credentials, auth
import os
import json


cred = credentials.Certificate(json.loads(os.environ['FIREBASE_SERVICE_CRED']))
firebase_admin.initialize_app(cred)
