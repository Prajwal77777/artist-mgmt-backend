import uuid
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from apps.core.models import User
from django.db import connection
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response


@csrf_exempt
def user_register(request: Request):
    """Register a new user."""

    if request.method == 'POST':
        try:
            data = request.data
            id = str(uuid.uuid4())
            first_name = data.get("first_name")
            last_name = data.get('last_name')
            email = data.get('email')
            password = data.get('password')
            phone = data.get('phone')
            dob = data.get('dob')
            gender = data.get('gender')
            role = data.get('role')

            hashed_password = make_password(password)

            if not all([first_name, last_name, email, phone, gender]):
                return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (id, first_name, last_name, email, password, phone, dob, gender, role, created_at, updated_at) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    [id, first_name, last_name, email, hashed_password, phone, dob,
                        gender, role, timezone.now(), timezone.now()]
                )

            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

        except json.JSONDecodeError:
            return Response(
                {"message": "Invalid JSON in request body"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    return Response({"message": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
