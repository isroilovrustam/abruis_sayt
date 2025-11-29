from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from course.models import Course, Enrollment
from portfolio.models import Portfolio
from .forms import UserRegistrationForm, UserProfileForm, CustomAuthenticationForm
from .models import UserProfile


def get_courses_for_index(limit=3):
    return Course.objects.filter(status='published').order_by('-created_at')[:limit]


def index(request):
    courses = get_courses_for_index(3)
    total_students = Enrollment.objects.values('student').distinct().count()
    total_courses = Course.objects.filter(status='published').count()
    total_portfolios = Portfolio.objects.filter(is_active=True).count()

    portfolios = Portfolio.objects.filter(is_active=True).order_by('-is_featured', '-created_at')[:3]
    context = {'courses': courses, 'portfolios': portfolios, 'total_students': total_students,
               'total_courses': total_courses, 'total_portfolios': total_portfolios, }
    return render(request, 'index.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.get_full_name() or user.username}!")
            return redirect('index')
        else:
            messages.error(request, "Username yoki parol noto'g'ri!")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Tabriklaymiz! Hisobingiz yaratildi.")
            return redirect('profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, "Siz tizimdan chiqdingiz.")
    return redirect('index')


@login_required(login_url='login')
def profile(request):
    user = request.user

    enrolled_courses = Enrollment.objects.filter(
        student=user,
        status='active'
    ).select_related('course').order_by('-enrolled_at')

    enrolled_courses_count = enrolled_courses.count()

    completed_courses_count = Enrollment.objects.filter(
        student=user,
        status='completed'
    ).count()

    total_lessons = sum(e.course.lessons_count or 0 for e in enrolled_courses)
    total_hours = sum(e.course.total_hours or 0 for e in enrolled_courses)

    context = {
        'user': user,
        'profile': user.profile,
        'enrolled_courses': enrolled_courses,
        'enrolled_courses_count': enrolled_courses_count,
        'completed_courses_count': completed_courses_count,
        'total_lessons': total_lessons,
        'total_hours': total_hours,
        'certificates_count': completed_courses_count,
    }

    return render(request, 'registration/profile.html', context)


@login_required(login_url='login')
def profile_edit(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile, user=user)
        if form.is_valid():
            user.email = form.cleaned_data.get('email', user.email)
            user.first_name = form.cleaned_data.get('first_name', user.first_name)
            user.last_name = form.cleaned_data.get('last_name', user.last_name)
            user.save()
            form.save()
            messages.success(request, "Profil muvaffaqiyatli yangilandi!")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile, user=user)

    return render(request, 'registration/profile_edit.html', {'form': form, 'user': user, 'profile': profile})
