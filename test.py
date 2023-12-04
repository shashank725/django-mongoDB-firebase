from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
import django
django.setup()
from django.core.management import call_command
from main.settings import MONGO_DB_URL


uri = MONGO_DB_URL
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)