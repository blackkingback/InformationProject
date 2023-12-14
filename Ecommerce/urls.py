from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "tweets"
urlpatterns = [
                path('main_page/', views.main_page, name='main_page'),
                path('get_product_detail/<str:asin>', views.get_product_detail, name='get_product_detail'),
                path('search_by_category/<str:search_text>', views.search_by_category, name='search_by_category'),
                path('search_bar/', views.search_bar, name='search_bar'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
