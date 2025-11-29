from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Sum, Count
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


# ============================================================
# KATEGORIYA
# ============================================================
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Kategoriya nomi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

    def __str__(self):
        return self.name


# ============================================================
# KURS
# ============================================================
class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', "Boshlang'ich"),
        ('intermediate', "O'rta"),
        ('advanced', "Yuqori"),
    ]

    STATUS_CHOICES = [
        ('draft', "Qoralama"),
        ('published', "Nashr qilingan"),
        ('archived', "Arxivlangan"),
    ]

    title = models.CharField(max_length=200, verbose_name="Kurs nomi")
    description = models.TextField(verbose_name="To'liq tavsif")
    short_description = models.CharField(max_length=500, blank=True, verbose_name="Qisqa tavsif")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='courses', verbose_name="Kategoriya")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Narx")
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner', verbose_name="Daraja")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Holati")
    image = models.ImageField(upload_to='course_images/', blank=True, null=True, verbose_name="Kurs posteri")

    # Avtomatik hisoblanadigan maydonlar
    total_hours = models.FloatField(default=0, editable=False, verbose_name="Umumiy soat")
    lessons_count = models.IntegerField(default=0, editable=False, verbose_name="Darslar soni")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Kurs"
        verbose_name_plural = "Kurslar"
        indexes = [models.Index(fields=['category', 'status'])]

    def __str__(self):
        return self.title

    def update_stats(self):
        """Darslardan soat va sonni hisoblash"""
        agg = self.lessons.aggregate(total_secs=Sum('duration_seconds'), cnt=Count('id'))
        total_seconds = agg['total_secs'] or 0
        self.total_hours = round(total_seconds / 3600, 2)
        self.lessons_count = agg['cnt'] or 0
        self.save(update_fields=['total_hours', 'lessons_count'])

    @property
    def total_duration_formatted(self):
        """Umumiy vaqtni formatlangan holda qaytarish"""
        total_seconds = int(self.total_hours * 3600)
        hrs = total_seconds // 3600
        mins = (total_seconds % 3600) // 60
        if hrs > 0:
            return f"{hrs} soat {mins} daqiqa"
        elif mins > 0:
            return f"{mins} daqiqa"
        else:
            return f"{total_seconds} sekund"


# ============================================================
# DARS
# ============================================================
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name="Kurs")
    title = models.CharField(max_length=200, verbose_name="Dars nomi")
    description = models.TextField(verbose_name="Dars tavsifi")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartibi")
    content = models.TextField(blank=True, verbose_name="Dars mazmuni")

    video_file = models.FileField(upload_to='course_videos/%Y/%m/', blank=True, null=True, verbose_name="Video fayl")
    duration_seconds = models.PositiveIntegerField(default=0, verbose_name="Davomiyligi (sekund)")
    thumbnail = models.ImageField(upload_to='course_thumbnails/%Y/%m/', blank=True, null=True, verbose_name="Thumbnail")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        unique_together = ('course', 'order')
        verbose_name = "Dars"
        verbose_name_plural = "Darslar"
        indexes = [models.Index(fields=['course', 'order'])]

    def __str__(self):
        return f"{self.course.title} → Dars {self.order}: {self.title}"

    @property
    def duration_formatted(self):
        hrs = self.duration_seconds // 3600
        mins = (self.duration_seconds % 3600) // 60
        if hrs > 0:
            return f"{hrs} soat {mins} daqiqa"
        elif mins > 0:
            return f"{mins} daqiqa"
        else:
            return f"{self.duration_seconds} sekund"

    @property
    def is_free(self):
        return self.order <= 3


# Dars qo'shilganda/o'chirilganda → Kurs statistikasini yangilash
@receiver([post_save, post_delete], sender=Lesson)
def update_course_on_lesson_change(sender, instance, **kwargs):
    instance.course.update_stats()


# ============================================================
# KURSGA QAYD ETISH
# ============================================================
class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('active', "Faol"),
        ('completed', "Tugallangan"),
        ('cancelled', "Bekor qilingan"),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    progress = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'course')
        ordering = ['-enrolled_at']
        verbose_name = "Kursga yozilish"
        verbose_name_plural = "Kursga yozilishlar"

    def __str__(self):
        return f"{self.student} → {self.course}"