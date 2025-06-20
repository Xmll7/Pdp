from rest_framework.permissions import BasePermission



class IsAdmin(BasePermission):
    # Permission adminga tekshiradi

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsTeacher(BasePermission):
    # Permission teacherga tekshiradi

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teacher'


class IsStudent(BasePermission):
    # Permission studentga tekshiradi

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'





