from django import forms
from .models import Course, Lesson, Enrollment


class CourseForm(forms.ModelForm):
    """Kurs yaratish va tahrirlash forması"""

    class Meta:
        model = Course
        fields = ['title', 'description', 'short_description', 'category', 'price',
                  'level', 'image', 'status']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Kurs nomi',
                'required': True
            }),
            'short_description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Qisqa tavsif',
                'maxlength': '500'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Kurs haqida batafsil ma\'lumot',
                'rows': 6
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'level': forms.Select(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }

        labels = {
            'title': 'Kurs Nomi',
            'short_description': 'Qisqa Tavsif',
            'description': 'To\'liq Tavsif',
            'category': 'Kategoriya',
            'price': 'Narxi (so\'m)',
            'level': 'Daraja',
            'status': 'Holati',
            'image': 'Kurs Rasmı',
        }


class LessonForm(forms.ModelForm):
    """Dars yaratish va tahrirlash forması"""

    class Meta:
        model = Lesson
        fields = ['title', 'description', 'content', 'video_file', 'order', 'duration_seconds', 'thumbnail']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dars nomi'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Qisqa tavsif',
                'rows': 3
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Dars matni/kontent',
                'rows': 10
            }),
            'video_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'video/*'
            }),
            'thumbnail': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '1',
                'min': '1'
            }),
            'duration_seconds': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '1800',
                'min': '0',
                'help_text': 'Davomiylikni sekundlarda kiriting (masalan: 30 daqiqa = 1800)'
            }),
        }

        labels = {
            'title': 'Dars Nomi',
            'description': 'Qisqa Tavsif',
            'content': 'Dars Kontent',
            'video_file': 'Video Fayl',
            'thumbnail': 'Thumbnail Rasm',
            'order': 'Tartib Raqami',
            'duration_seconds': 'Davomiyligi (sekund)',
        }


class CommentForm(forms.ModelForm):
    """Sharh qoldirish forması"""

    RATING_CHOICES = [
        (5, '⭐⭐⭐⭐⭐ Ajoyib (5)'),
        (4, '⭐⭐⭐⭐ Yaxshi (4)'),
        (3, '⭐⭐⭐ O\'rtacha (3)'),
        (2, '⭐⭐ Yomon (2)'),
        (1, '⭐ Juda Yomon (1)'),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'rating-radio'
        }),
        label='Kursni Baholang'
    )

    class Meta:
        model = Comment
        fields = ['rating', 'comment']

        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Kurs haqida sizning fikringiz...',
                'rows': 5,
                'minlength': '10',
                'maxlength': '1000'
            }),
        }

        labels = {
            'comment': 'Sizning Sharhingiz'
        }

    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        if comment and len(comment) < 10:
            raise forms.ValidationError('Sharh kamida 10 ta belgidan iborat bo\'lishi kerak.')
        return comment


# Alias for backward compatibility
ReviewForm = CommentForm