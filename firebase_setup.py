import firebase_admin
from firebase_admin import credentials, auth
import os

cred = credentials.Certificate(os.path.join(os.getcwd(), 'firebase_service_cred.json'))
firebase_admin.initialize_app(cred)
