from rest_framework import permissions
from .models import Exam
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Admin foydalanuvchilar o‘zgartira oladi,
    oddiy userlar faqat ko‘rishi mumkin.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        return request.user and request.user.is_staff
    
class IsUserInExam(permissions.BasePermission):
    """
    Faqat exam.users ichida bo‘lgan userlargagina ruxsat beradi
    """

    def has_permission(self, request, view):
        exam_id = view.kwargs.get("pk")  # yoki urldagi exam id
        if not exam_id:
            return False
        
        try:
            exam = Exam.objects.get(pk=exam_id)
        except Exam.DoesNotExist:
            return False

        return request.user.is_authenticated and request.user in exam.users.all()