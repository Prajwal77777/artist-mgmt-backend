# config/middlewares.py

from django.http import JsonResponse


class RoleBasedAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_role = request.session.get('role')

        # Allow registration without role restrictions
        if request.path == '/auth/user/register/' and request.method == 'POST':
            response = self.get_response(request)
            return response
        if request.path == '/auth/user/login/' and request.method == 'POST':
            response = self.get_response(request)
            return response
        if request.path == '/auth/user/logout/' and request.method == 'POST':
            response = self.get_response(request)
            return response

        # Check for permissions based on path and role
        if request.path.startswith('/auth/user') and user_role != 'super_admin':
            return JsonResponse({'error': 'Permission Denied'}, status=403)

        if request.path.startswith('/admin/artist') and user_role not in ['super_admin', 'artist_manager']:
            return JsonResponse({'error': 'Permission Denied'}, status=403)

        if request.path.startswith('/admin/music') and user_role not in ['super_admin', 'artist_manager', 'artist']:
            return JsonResponse({'error': 'Permission Denied'}, status=403)

        response = self.get_response(request)
        return response
