from django.http import JsonResponse


def required_role(allowed_roles=[]):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            user_role = request.session.get('role')
            if user_role not in allowed_roles:
                return JsonResponse({'error': 'Permission Denied'}, status=403)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
