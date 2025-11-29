from django.urls import path
from .views import (
    course,
    course_detail,
    lesson_view,
    enroll_course,
)


urlpatterns = [
    path('', course, name='course'),
    path('<int:course_id>/', course_detail, name='course_detail'),
    path('<int:course_id>/lesson/<int:lesson_id>/', lesson_view, name='lesson_view'),
    path('<int:course_id>/enroll/', enroll_course, name='enroll'),
]