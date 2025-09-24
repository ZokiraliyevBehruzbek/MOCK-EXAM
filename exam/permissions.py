from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Admin foydalanuvchilar o‘zgartira oladi,
    oddiy userlar faqat ko‘rishi mumkin.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        return request.user and request.user.is_staff
