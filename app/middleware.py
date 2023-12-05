import firebase_admin
from firebase_admin import credentials, auth
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.http import JsonResponse

cred = credentials.Certificate("django-mongodb-firebase-firebase-adminsdk-1wsj6-2f8e17d950.json")
firebase_admin.initialize_app(cred)

class FirebaseAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check for Firebase token in the request headers
        id_token = request.headers.get('Authorization', '').split('Bearer ')[-1]

        # if id_token:
        #     try:
        #         decoded_token = auth.verify_id_token(id_token)
        #         uid = decoded_token['uid']
        #         user, created = User.objects.get_or_create(username=uid)
        #         request.user = user
        #     except auth.InvalidIdTokenError:
        #         print("Invalid Token Error")

        if id_token:
            try:
                # Verify the Firebase token
                decoded_token = auth.verify_id_token(id_token)
                # Set the authenticated user in the request
                request.user = decoded_token
            except auth.InvalidIdTokenError as e:
                # return Response({'error': 'Unauthorized'}, status=401)   #Response should not be used
                return JsonResponse({"error": "Invalid Token Error: "+ e}, status=401)
        else:
            print("ID Token Not Found")
            # return JsonResponse({"error": "ID Token Not Found"}, status=401)

        response = self.get_response(request)
        return response
