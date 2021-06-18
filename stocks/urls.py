from django.urls import path
from . import views

urlpatterns = [
    # Navbar urls
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('pricing/', views.pricing, name='pricing'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),

    # Registration pages and password change forms
    path('account/send_otp/', views.send_otp, name='send_otp'),
    path('account/validate_mail/', views.validate_mail, name='validate_mail'),
    path('account/open_account/', views.open_account, name='open_account'),
    path('account/create_password/', views.create_pass, name='create_pass'),
    path('account/select_plan/', views.select_plan, name='select_plan'),

    # Pages available when user is logged in 
    path('user/portfolio/', views.portfolio, name='portfolio'),
    path('user/stocks/', views.stocks, name='stocks'),
    path('user/stocks/quote/', views.quote, name='quote'),
    path('user/stocks/price/', views.price, name='price'),
    path('user/stocks/price/<str:symbol>/', views.price, name='price'),
    path('user/stocks/buy/', views.buy, name='buy'),
    path('user/stocks/sell/', views.sell, name='sell'),
    path('user/transaction/history/', views.history, name='history'),
    path('user/logout/', views.logout, name='logout'),

    # Password change forms
    path('account/confirm_mail/', views.confirm_mail, name='confirm_mail'),
    path('account/change_password/', views.change_password, name='change_password'),
]