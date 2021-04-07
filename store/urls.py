from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.Store.as_view(), name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.update_item, name='update_item')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)