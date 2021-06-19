from django.urls import path

from . import views

app_name = 'charts'

urlpatterns = [
    path('filter-options/', views.get_filter_options, name='chart_filter_options'),
    path('sales/<int:year>/', views.get_sales_chart, name='chart_sales'),
    path('products-type/', views.product_types, name='products_type'),
    path('number_of_products/', views.number_of_products, name='number_of_products'),
    path('payment-method/<year>/', views.payment_method_chart)
]