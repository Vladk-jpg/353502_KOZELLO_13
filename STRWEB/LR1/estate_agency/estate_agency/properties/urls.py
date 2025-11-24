from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('property/<int:property_id>/', views.property_detail, name='property_detail'),
    path('property/<int:property_id>/reserve/', views.property_reserve, name='property_reserve'),
    path('categories/', views.category_list, name='category_list'),
    path('client/purchases/', views.client_purchases, name='client_purchases'),
    path('client/reservations/', views.client_reservations, name='client_reservations'),
    path('promo-codes/', views.promo_codes, name='promo_codes'),
    
    path('api/properties/', views.api_properties, name='api_properties'),

    path('agent/properties/', views.agent_property_list, name='agent_property_list'),
    path('agent/properties/create/', views.agent_property_create, name='agent_property_create'),
    path('agent/properties/<int:property_id>/edit/', views.agent_property_edit, name='agent_property_edit'),
    path('agent/properties/<int:property_id>/delete/', views.agent_property_delete, name='agent_property_delete'),
    path('agent/sales/', views.agent_sales, name='agent_sales'),
    path('sales/monitoring/', views.admin_sales, name='sales_monitoring'),
]