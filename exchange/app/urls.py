from django.urls import path
from . import views

urlpatterns = [
    path("wallet/", views.wallet, name="wallet"),
    path('', views.homepage, name="homepage"),
    path('nuovo_ordine', views.nuovo_ordine, name='nuovo_ordine'),
    path('all-order', views.AllOrder.as_view(template_name='all_order.html'), name='all-order'),
    path('profit', views.profit, name='profit')
]