from django.urls import path, include

urlpatterns = [
    path('', include('users.urls')),
    path('course/', include('course.urls')),
    path('portfolio/', include('portfolio.urls')),
]
