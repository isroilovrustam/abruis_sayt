"""
apps/course/admin.py - ZAMONAVIY & TO'LIQ ADMIN PANEL
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import (
    Category, Course, Lesson, Enrollment,
)


# ============================================================
# CATEGORY ADMIN
# ============================================================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'courses_count', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at']

    def courses_count(self, obj):
        count = obj.courses.count()
        return format_html(f'<b>{count}</b> ta kurs')
    courses_count.short_description = 'Kurslar soni'


# ============================================================
# COURSE ADMIN - ENG MUHIMI!
# ============================================================
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'category',
        'price',
        'total_hours_badge',
        'lessons_count',
        'students_count',
        'status_badge',
        'created_at'
    ]
    list_filter = ['status', 'category', 'level', 'created_at']
    search_fields = ['title', 'short_description']
    readonly_fields = ['total_hours', 'lessons_count', 'created_at', 'updated_at']

    fieldsets = (
        ('Asosiy', {
            'fields': ('title', 'category', 'status', 'level')
        }),
        ('Tavsif', {
            'fields': ('short_description', 'description')
        }),
        ('Narx va Rasm', {
            'fields': ('price', 'image')
        }),
        ('Statistika (Avtomatik)', {
            'fields': ('total_hours', 'lessons_count'),
            'classes': ('collapse',),
            'description': 'Bu maydonlar darslardan avtomatik hisoblanadi'
        }),
        ('Vaqt', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def total_hours_badge(self, obj):
        if obj.total_hours == 0:
            return "-"
        color = "#10B981" if obj.total_hours >= 10 else "#F59E0B"
        return format_html(
            f'<span style="background:{color}; color:white; padding:4px 10px; border-radius:4px; font-weight:600;">'
            f'{obj.total_hours} soat</span>'
        )
    total_hours_badge.short_description = 'Umumiy davomiylik'

    def students_count(self, obj):
        count = obj.enrollments.count()
        return format_html(f'<b>{count}</b> talaba')
    students_count.short_description = 'Talabalar'

    def status_badge(self, obj):
        colors = {
            'draft': '#FCD34D',
            'published': '#10B981',
            'archived': '#EF4444'
        }
        color = colors.get(obj.status, '#6B7280')
        return format_html(
            f'<span style="background:{color}; color:white; padding:4px 12px; border-radius:4px; font-weight:600;">'
            f'{obj.get_status_display()}</span>'
        )
    status_badge.short_description = 'Holati'


# ============================================================
# LESSON ADMIN - ZAMONAVIY
# ============================================================
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('lesson_preview', 'order', 'course', 'duration_badge', 'video_status', 'is_free_badge')
    list_editable = ('order',)                    # Endi birinchi emas → ruxsat beriladi!
    list_display_links = ('lesson_preview',)      # Bu ustunga bosilganda → edit sahifasiga o‘tadi

    search_fields = ('title', 'course__title')
    list_filter = ('course', 'course__category')
    readonly_fields = ('created_at', 'updated_at', 'duration_formatted')

    def lesson_preview(self, obj):
        return f"Dars {obj.order}: {obj.title}"
    lesson_preview.short_description = "Dars nomi"

    def duration_badge(self, obj):
        if not obj.duration_seconds:
            return "–"
        mins = obj.duration_seconds // 60
        return format_html(f'<b>{mins}</b> daq')
    duration_badge.short_description = "Davomiyligi"

    def video_status(self, obj):
        if obj.video_file:
            return format_html('<span style="color:green;">Video bor</span>')
        return format_html('<span style="color:#999;">Video yo‘q</span>')
    video_status.short_description = "Video"

    def is_free_badge(self, obj):
        if obj.order <= 3:
            return format_html('<span style="background:#10b981;color:white;padding:3px 8px;border-radius:4px;font-size:11px;">BEPUL</span>')
        return format_html('<span style="background:#8b5cf6;color:white;padding:3px 8px;border-radius:4px;font-size:11px;">PREMIUM</span>')
    is_free_badge.short_description = "Turi"


# ============================================================
# ENROLLMENT ADMIN
# ============================================================
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course_link', 'progress_bar', 'status_badge', 'enrolled_at']
    list_filter = ['status', 'course', 'enrolled_at']
    search_fields = ['student__username', 'student__email', 'course__title']
    readonly_fields = ['enrolled_at', 'completed_at', 'progress']

    def course_link(self, obj):
        return format_html(f'<a href="/admin/course/course/{obj.course.id}/change/">{obj.course.title}</a>')
    course_link.short_description = 'Kurs'

    def progress_bar(self, obj):
        color = "#10B981" if obj.progress >= 80 else "#F59E0B" if obj.progress >= 40 else "#EF4444"
        return format_html(
            f'<div style="width:120px; height:24px; background:#E5E7EB; border-radius:4px; overflow:hidden;">'
            f'<div style="width:{obj.progress}%; height:100%; background:{color}; transition:width 0.4s;"></div>'
            f'</div> <b>{obj.progress}%</b>'
        )
    progress_bar.short_description = 'Progress'

    def status_badge(self, obj):
        colors = {'active': '#10B981', 'completed': '#3B82F6', 'cancelled': '#EF4444'}
        color = colors.get(obj.status, '#6B7280')
        return format_html(
            f'<span style="background:{color}; color:white; padding:4px 10px; border-radius:4px;">'
            f'{obj.get_status_display()}</span>'
        )
    status_badge.short_description = 'Holati'

# ============================================================
# ADMIN SAYT SOZLAMLARI
# ============================================================
admin.site.site_header = "ABRUISDEV — Kurs Platformasi"
admin.site.site_title = "Abruis Admin"
admin.site.index_title = "Assalomu alaykum! Xush kelibsiz"