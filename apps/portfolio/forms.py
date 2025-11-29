from django import forms
from .models import Portfolio


class PortfolioForm(forms.ModelForm):
    """Portfolio loyihasi yaratish va tahrirlash forması"""

    class Meta:
        model = Portfolio
        fields = ['title', 'description', 'category', 'image', 'technologies',
                  'project_url', 'github_url']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Loyiha nomi',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Loyiha haqida batafsil tavsif',
                'rows': 5
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'technologies': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'React, Django, PostgreSQL, Bootstrap',
                'help_text': 'Vergul bilan ajratilgan'
            }),
            'project_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com'
            }),
            'github_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/username/repo'
            }),
        }

        labels = {
            'title': 'Loyiha Nomi',
            'description': 'Tavsif',
            'category': 'Kategoriya',
            'image': 'Loyiha Rasmı',
            'technologies': 'Ishlatilgan Texnologiyalar',
            'project_url': 'Loyiha Manzili (ixtiyoriy)',
            'github_url': 'GitHub Manzili (ixtiyoriy)',
        }
