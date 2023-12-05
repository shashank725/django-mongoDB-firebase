from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import json

import firebase_admin
from firebase_admin import auth, credentials
# cred = credentials.Certificate("django-mongodb-firebase-firebase-adminsdk-1wsj6-2f8e17d950.json")
# firebase_admin.initialize_app(cred)
# Create your views here.

@csrf_exempt
@require_POST
def register_view(request):
    # Extract data from the request payload
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    first_name = request.POST.get('first_name', '')
    last_name = request.POST.get('last_name', '')
    if not email or not password:
        return JsonResponse({"error": "Email and password are required."}, status=401)
    if len(password) < 8:
        return JsonResponse({"error": "This password is too short. It must contain at least 8 characters."}, status=401)
    if any(len(value) > 100 for value in [username, email, password, first_name, last_name]):
        return JsonResponse({"error": "Only 100 characters are allowed for a field"}, status=401)
    # Create a unique username for the user
    # generated_username = generate_unique_username(username)
    if check_username(username):
        return JsonResponse({"error": "A user with that username already exists"}, status=401)
    else:
        user = User.objects.create_user(username=username, email=email, password=password,
                                        first_name=first_name, last_name=last_name)
        response_data = {"username": username, "email": email}
        return JsonResponse(response_data, status=201)

# def generate_unique_username(base_username):
#     return base_username
def check_username(username):
    try:
        user = User.objects.get(username=username)
        if not user:
            return True
    except User.DoesNotExist as e:
        print(e)
        return False



@csrf_exempt
@require_http_methods(["GET", "POST"])
def login_view(request):
    data = json.loads(request.body)
    # data = json.loads(request.body.decode('utf-8'))
    username = data.get('username')
    password = data['password']
    if not username or not password:
        return JsonResponse({"error": "Username and password are required."}, status=400)
    # Authenticate the user
    user = authenticate(request, username=username, password=password)
    if user is not None:
        # Use Firebase auth to create a custom_token
        custom_token = create_custom_token(user)
        if custom_token:
            response_data = {"username": user.username, "email": user.email, "full_name": user.first_name+" "+user.last_name}
            return JsonResponse(response_data, status=200)
        else:
            return JsonResponse({"error": "Error creating custom token."}, status=401)
    else:
        return JsonResponse({"error": "Username or password is invalid."}, status=401)


def create_custom_token(user):
    # Create a custom token for the user using Firebase Auth
    try:
        custom_token = auth.create_custom_token(user.username)
        return custom_token
    except auth.InvalidIdTokenError as e:
        print(f"Error creating custom token: {e}")
        return None

