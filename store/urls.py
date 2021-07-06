from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.update_item, name='update_item'),
    path('process_order/', views.process_order, name='update_item'),
    path('registration', views.registration, name='registration'),
    path('log_in', views.log_in, name='log_in'),
    path('log_out', views.log_out, name='log_out')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
