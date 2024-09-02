from datetime import datetime, timedelta

import jwt
from django.conf import settings
import json
from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone
from django.db import connection
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from apps.core.validations import email_validation


@api_view(['POST'])
def user_register(request: Request):
    """Register a new user."""

    if request.method == 'POST':
        try:
            data = request.data
            full_name = data.get("full_name")
            email = data.get('email')
            password = data.get('password')
            role = data.get('role')

            hashed_password = make_password(password)
            if not email_validation(email):
                return Response({'error': 'Invalid email address'}, status=status.HTTP_400_BAD_REQUEST)

            if not all([full_name, email, password]):
                return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (full_name, email, password, role, created_at, updated_at) VALUES (%s, %s, %s, %s,%s, %s)",
                    [full_name, email, hashed_password, role,
                        timezone.now(), timezone.now()]
                )

            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

        except json.JSONDecodeError:
            return Response(
                {"message": "Invalid JSON in request body"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    return Response({"message": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def get_users(request: Request):
    """Get all users."""

    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            columns = [col[0] for col in cursor.description]
            users = cursor.fetchall()
        result = [dict(zip(columns, row)) for row in users]
        return Response({"data": result}, status=status.HTTP_200_OK)
    return Response({"message": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def get_user(request: Request, id: str):
    """GET a Specific User"""
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s;", [id])
            columns = [col[0] for col in cursor.description]
            user = cursor.fetchall()

        result = [dict(zip(columns, row)) for row in user]
        return Response({"data": result}, status=status.HTTP_200_OK)
    return Response({"message": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def login_user(request: Request):
    """Login a user."""
    if request.method == 'POST':
        data = request.data
        email = data.get("email")
        password = data.get("password")

        # Validate input data
        if not email or not password:
            return Response({"message": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check email validity
        if not email_validation(email):
            return Response({"message": "Invalid email format."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, password FROM users WHERE email = %s", [
                        email]
                )
                user_data = cursor.fetchone()
            if user_data is None:
                return Response({"message": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

            user_id, hashed_password,  = user_data

            if not check_password(password, hashed_password):
                return Response({"message": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

            # Create JWT token
            payload = {
                'user_id': user_id,
                'email': email,
                'exp': datetime.utcnow() + timedelta(hours=24)
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

            return Response({
                "message": "Login successful.",
                "token": token,
                "user_id": user_id,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": "An error occurred during login."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def logout_user(request: Request):
    """Logout a user."""
    if request.method == 'POST':
        try:
            # The client-side should handle removing the token from local storage
            return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "An error occurred during logout."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"message": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def get_current_user(request: Request):
    """Get the currently logged-in user's data."""
    if request.method == 'GET':
        try:
            user_id = request.user.id

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE id = %s", [user_id])
                columns = [col[0] for col in cursor.description]
                user_data = cursor.fetchone()

            if user_data:
                user = dict(zip(columns, user_data))
                return Response({"user": user}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"message": "An error occurred while fetching user data."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"message": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
