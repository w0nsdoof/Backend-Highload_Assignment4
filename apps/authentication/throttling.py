from rest_framework import throttling

class StaffRateThrottle(throttling.UserRateThrottle):
    scope = 'staff'
    
    def get_cache_key(self, request, view):
        user = request.user
        if user.is_authenticated and user.is_staff:
            return f'staff_{user.pk}'
        return None
