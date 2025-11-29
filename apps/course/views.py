from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Course, Lesson, Enrollment


def course(request):
    courses = Course.objects.filter(status='published').select_related('category')
    categories = Category.objects.all()

    context = {
        'courses': courses,
        'categories': categories,
    }
    return render(request, 'course/course.html', context)


@login_required(login_url='login')
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id, status='published')
    lessons = course.lessons.order_by('order')
    is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()

    context = {
        'course': course,
        'all_lessons': lessons,
        'is_enrolled': is_enrolled,
    }
    return render(request, 'course/course_detail.html', context)

@login_required(login_url='login')
def lesson_view(request, course_id, lesson_id):
    course = get_object_or_404(Course, id=course_id, status='published')
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()

    # Boshqa darslar (sidebar)
    other_lessons = course.lessons.order_by('order')

    context = {
        'course': course,
        'lesson': lesson,
        'is_enrolled': is_enrolled,
        'other_lessons': other_lessons,
        'is_free_lesson': lesson.is_free,
    }
    return render(request, 'course/lesson_view.html', context)


# ============================================================
# KURSGA YOZILISH
# ============================================================
@login_required(login_url='login')
def enroll_course(request, course_id):
    """
    Kursga yozilish
    """
    course = get_object_or_404(Course, id=course_id, status='published')

    if request.method == 'POST':
        enrollment, created = Enrollment.objects.get_or_create(student=request.user, course=course)
        if created:
            messages.success(request, f"{course.title} kursiga muvaffaqiyatli yozildingiz!")
            first_lesson = course.lessons.order_by('order').first()
            if first_lesson:
                return redirect('lesson_view', course_id=course.id, lesson_id=first_lesson.id)
        else:
            messages.info(request, "Siz allaqachon bu kursga yozilgansiz.")

    return redirect('course_detail', course_id=course.id)

