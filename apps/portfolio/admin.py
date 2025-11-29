from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count
from .models import Portfolio, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Kategoriya admin"""
    list_display = ('title', 'portfolio_count', 'icon_preview')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', )

    def portfolio_count(self, obj):
        """Kategoriyada nechta portfolio bor"""
        count = obj.portfolios.count()
        return format_html(
            '<span style="background:#4F46E5;color:white;padding:4px 8px;border-radius:4px;">{} ta</span>',
            count
        )

    portfolio_count.short_description = 'Loyihalar'

    def icon_preview(self, obj):
        """Icon preview"""
        if obj.icon:
            return format_html('<i class="{}"></i> {}', obj.icon, obj.icon)
        return "—"

    icon_preview.short_description = 'Icon'


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    """Portfolio admin"""
    list_display = (
        'title_with_status',
        'category_badge',
        'tech_preview',
        'featured_badge',
        'image_thumb',
        'created_at'
    )
    list_filter = ('category', 'is_featured', 'is_active', 'created_at', 'year')
    search_fields = ('title', 'description', 'technologies')
    readonly_fields = ('created_at', 'updated_at', 'image_preview', 'technologies_preview')
    date_hierarchy = 'created_at'
    ordering = ('-is_featured', '-created_at')

    fieldsets = (
        ('📋 Asosiy Ma\'lumotlar', {
            'fields': ('title', 'description', 'category', 'year')
        }),
        ('🖼️ Rasm va Havolalar', {
            'fields': ('image', 'image_preview', 'project_url', 'demo_url', 'github_url'),
            'description': 'Rasmni yuklangandan so\'ng oldindan ko\'rish avtomatik yangilanadi.'
        }),
        ('⚙️ Texnologiyalar', {
            'fields': ('technologies', 'technologies_preview'),
            'description': 'Texnologiyalarni vergul bilan ajratib yozing (masalan: Django, React, PostgreSQL)'
        }),
        ('🎯 Statuslar', {
            'fields': ('is_featured', 'is_active'),
            'description': 'is_featured - bosh sahifada ko\'rsatilishi uchun'
        }),
        ('📅 Vaqt Belgilari', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    # Title bilan status
    def title_with_status(self, obj):
        status = "✅" if obj.is_active else "❌"
        return format_html('{} {}', status, obj.title)

    title_with_status.short_description = 'Loyiha'

    # Kategoriyani badge sifatida ko'rsatish
    def category_badge(self, obj):
        colors = {
            'web': '#3498db',
            'app': '#e74c3c',
            'ecommerce': '#2ecc71',
            'design': '#9b59b6',
            'other': '#95a5a6'
        }
        color = colors.get(obj.category.slug, '#3498db')
        return format_html(
            '<span style="background:{};color:white;padding:5px 10px;border-radius:6px;font-size:12px;font-weight:600;">{}</span>',
            color,
            obj.category.title
        )

    category_badge.short_description = 'Kategoriya'

    # Texnologiyalarni preview qilish
    def tech_preview(self, obj):
        techs = obj.get_technologies_list()
        if len(techs) > 3:
            display = ', '.join(techs[:3]) + f' <i>+{len(techs) - 3}</i>'
        else:
            display = ', '.join(techs) if techs else '—'
        return format_html(display)

    tech_preview.short_description = 'Texnologiyalar'

    def technologies_preview(self, obj):
        """Forma ichida texnologiyalar preview"""
        techs = obj.get_technologies_list()
        if not techs:
            return "Texnologiya kiritilmagan"

        html = '<div style="display: flex; flex-wrap: wrap; gap: 8px;">'
        for tech in techs:
            html += format_html(
                '<span style="background:#4F46E5;color:white;padding:4px 8px;border-radius:4px;font-size:12px;">{}</span>',
                tech
            )
        html += '</div>'
        return format_html(html)

    technologies_preview.short_description = 'Texnologiyalar Preview'

    # Featured badge
    def featured_badge(self, obj):
        if obj.is_featured:
            return format_html(
                '<span style="background:#f39c12;color:white;padding:4px 8px;border-radius:4px;font-weight:600;">⭐ Featured</span>'
            )
        return "—"

    featured_badge.short_description = 'Asosiy'

    # Rasm thumbnail ro'yxatda
    def image_thumb(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:50px;height:50px;object-fit:cover;border-radius:6px;box-shadow:0 2px 4px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        return "❌ Rasm yo'q"

    image_thumb.short_description = 'Rasm'

    # Katta rasm preview forma ichida
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<div style="max-width:300px;"><img src="{}" style="width:100%;border-radius:8px;box-shadow:0 4px 10px rgba(0,0,0,0.15);" /></div>',
                obj.image.url
            )
        return format_html(
            '<div style="padding:20px;background:#f5f5f5;border-radius:8px;text-align:center;color:#999;">Rasm yuklanmagan</div>'
        )

    image_preview.short_description = 'Rasm Oldindan Ko\'rish'

    def get_queryset(self, request):
        """Optimized queryset"""
        return super().get_queryset(request).select_related('category')
