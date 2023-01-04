from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.home, name='home'),

    path('products/', views.products, name='products'),
    path('category/<str:category>', views.category, name='category'),

    path('contact/', views.contact, name='contact'),

    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),

    path('myprofile/', views.myprofile, name='myprofile'),
    path('edit-profile/', views.editprofile, name='edit-profile'),
    path('edit-account/', views.editaccount, name='edit-account'),
    path('delete-account/', views.deleteaccount, name='delete-account'),
    path('remove-picture/', views.removepicture, name='remove-picture'),
    
    path('mymarket/', views.check_market, name='mymarket'),
    path('create-market/', views.createmarket, name='create-market'),
    path('edit-market/', views.editmarket, name='edit-market'),
    path('edit-market/edit/<str:product_name>', views.editproduct, name='edit-product'),
    path('edit-market/delete/<str:product_name>', views.deleteproduct, name='delete-product'),
    path('<str:market_name>/', views.market, name='market'),
    path('<str:market_name>/<str:product_name>', views.productdetail, name='product-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)