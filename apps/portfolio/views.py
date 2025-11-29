from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render
from .models import Portfolio, Category


def portfolio_list(request):
    portfolios = Portfolio.objects.filter(is_active=True)
    category_id = request.GET.get('category')
    if category_id:
        portfolios = portfolios.filter(category_id=category_id)

    portfolios = portfolios.order_by('-is_featured', '-created_at')

    # Pagination (12 ta har sahifada)
    paginator = Paginator(portfolios, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Kategoriyalar
    categories = Category.objects.annotate(
        count=Count('portfolios')
    ).order_by('title')

    context = {
        'page_obj': page_obj,
        'portfolios': page_obj.object_list,
        'categories': categories,
        'selected_category': category_id,
        'total_count': portfolios.count(),
    }

    return render(request, 'portfolio.html', context)