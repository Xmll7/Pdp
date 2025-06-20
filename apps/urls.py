from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.views import SessionListView, SessionDestroyAPIView, \
    LeaderBoardListAPIView, GetStudentHomeworkListAPIView, HomeworkCreateAPIView, StudentSubmissionListAPIView, \
    RegisterCreateAPIView, TeacherHomeworkViewSet, TeacherGroupViewSet, TeacherSubmissionViewSet, TeacherViewSet, \
    StudentViewSet, GroupViewSet

urlpatterns = [
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('sessions-list', SessionListView.as_view(), name='sessions_list'),
    path('api/auth/sessions/delete/<int:pk>', SessionDestroyAPIView.as_view()),

    # Studet
    path('api/student/leaders-list', LeaderBoardListAPIView.as_view()),
    path('api/student/my-homework', GetStudentHomeworkListAPIView.as_view()),
    path('api/student/create-homework', HomeworkCreateAPIView.as_view()),
    path('api/student/submissions/list', StudentSubmissionListAPIView.as_view()),




]


urlpatterns += [
    path('auth/register/', RegisterCreateAPIView.as_view(), name='register'),
]

# Teacher routes
teacher_router = DefaultRouter()
teacher_router.register(r'teacher/homework', TeacherHomeworkViewSet, basename='teacher-homework')
teacher_router.register(r'teacher/groups', TeacherGroupViewSet, basename='teacher-groups')
teacher_router.register(r'teacher/submissions', TeacherSubmissionViewSet, basename='teacher-submissions')

# Admin routes
admin_router = DefaultRouter()
admin_router.register(r'admin/teacher', TeacherViewSet, basename='admin-teachers')
admin_router.register(r'admin/student', StudentViewSet, basename='admin-students')
admin_router.register(r'admin/groups', GroupViewSet, basename='admin-groups')


urlpatterns += teacher_router.urls
urlpatterns += admin_router.urls
