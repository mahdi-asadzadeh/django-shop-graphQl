from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, F, Sum, Avg
from django.db.models.functions import ExtractYear, ExtractMonth
from django.http import JsonResponse

from order.models import Order
from product.models import Product
from .utils.charts import months, colorPrimary, colorSuccess, colorDanger, generate_color_palette, get_year_dict


@staff_member_required
def get_filter_options(request):
    grouped_purchases = Order.objects.annotate(year=ExtractYear('create')).values('year').order_by('-year').distinct()

    options = [purchase['year'] for purchase in grouped_purchases]

    return JsonResponse({
        'options': options,
    })


@staff_member_required
def get_sales_chart(request, year):
    purchases = Order.objects.filter(create__year=year, paid=True)

    grouped_purchases = purchases.annotate(price_total=F('price')).annotate(month=ExtractMonth('create'))\
        .values('month').annotate(average=Sum('price')).values('month', 'average').order_by('month')
    sales_dict = get_year_dict()

    for group in grouped_purchases:
        sales_dict[months[group['month']-1]] = round(group['average'], 2)

    return JsonResponse({
        'title': f'Sales in {year}',
        'data': {
            'labels': list(sales_dict.keys()),
            'datasets': [{
                'label': 'Amount ($)',
                'backgroundColor': colorPrimary,
                'borderColor': colorPrimary,
                'data': list(sales_dict.values()),
            }]
        },
    })



@staff_member_required
def payment_method_chart(request, year):
    purchases = Order.objects.all()

    return JsonResponse({
        'title': f'Payment success rate in {year}',
        'data': {
            'labels': ['paid', 'unpaid'],
            'datasets': [{
                'label': 'Amount ($)',
                'backgroundColor': [colorSuccess, colorDanger],
                'borderColor': [colorSuccess, colorDanger],
                'data': [
                    purchases.filter(paid=True).count(),
                    purchases.filter(paid=False).count(),
                ],
            }]
        },
    })


@staff_member_required
def product_types(request):
    products = Product.objects.all()

    return JsonResponse({
        'title': f'Product Types',
        'data': {
            'labels': ['Gold', 'Gewelry'],
            'datasets': [{
                'label': 'Amount ($)',
                'backgroundColor': [colorSuccess, colorDanger],
                'borderColor': [colorSuccess, colorDanger],
                'data': [
                    products.filter(gold_or_jewelry=True).count(),
                    products.filter(gold_or_jewelry=False).count(),
                ],
            }]
        },
    })


@staff_member_required
def number_of_products(request):
    products = Product.objects.all().count()
    return JsonResponse({'number_of_producs':products})

