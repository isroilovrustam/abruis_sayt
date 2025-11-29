from django.db import models


class Category(models.Model):
    """Portfolio kategoriyalari"""
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class, e.g., 'fab fa-react'")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['title']

    def __str__(self):
        return self.title


class Portfolio(models.Model):
    """Portfolio loyihalar"""
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(help_text="Loyiha tavsifi")
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="portfolios"
    )

    # Rasm
    image = models.ImageField(
        upload_to='portfolio_images/%Y/%m/',
        help_text="Loyiha rasmi (recommended: 800x600px)"
    )

    # Texnologiyalar (JSON yoki comma-separated text)
    technologies = models.TextField(
        help_text="Texnologiyalarni vergul bilan ajratib yozing: Django, React, PostgreSQL"
    )

    # Havolalar
    project_url = models.URLField(blank=True, null=True, help_text="Loyiha saytining URL'i")
    github_url = models.URLField(blank=True, null=True, help_text="GitHub repository URL'i")
    demo_url = models.URLField(blank=True, null=True, help_text="Demo URL'i (project_url bo'lsa, bu ham istifodalanil)")

    # Vaqt belgilari
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    year = models.IntegerField(blank=True, null=True, help_text="Loyiha yaratilgan yil")

    # Status
    is_featured = models.BooleanField(default=False, help_text="Bosh sahifada ko'rsatilsin?")
    is_active = models.BooleanField(default=True, help_text="Aktiv loyihami?")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Portfolio"
        verbose_name_plural = "Portfolios"

    def __str__(self):
        return self.title

    def get_technologies_list(self):
        """Texnologiyalarni list sifatida qaytarish"""
        return [tech.strip() for tech in self.technologies.split(',') if tech.strip()]

    def get_demo_url(self):
        """Demo yoki project URL'ni qaytarish"""
        return self.demo_url or self.project_url or '#'

    def get_github_url(self):
        """GitHub URL'ni qaytarish, agar bo'lmasa #"""
        return self.github_url or '#'
