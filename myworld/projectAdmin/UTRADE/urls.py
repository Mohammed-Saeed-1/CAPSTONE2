from django.urls import path
from . import views

app_name = 'Utrade'

urlpatterns = [

    path('profile', views.profile, name='profile'),

    path('dashboard' ,views.dashboard , name='dashboard'),
    path('logout' ,views.Logout , name='logout'),

    path('' ,views.home , name='home'),
    path('for_testing' ,views.for_testing , name='for_testing'),
    

    path('register' ,views.register , name='register'),
    path('login' ,views.Login , name='login'),

    path('first_interests' ,views.first_interests , name='first_interests'),
    path('next_interests' ,views.next_interests , name='next_interests'),

    path('portfolio' ,views.portfolio , name='portfolio'),
    path('fav' ,views.fav , name='fav'),
    path('news' ,views.news , name='news'),
    path('search' ,views.search , name='search'),

    path('trade' ,views.trade , name='trade'),
    path('next_trade' ,views.next_trade , name='next_trade'),
    path('result' ,views.result , name='result'),

    path('pages-contact' ,views.contact , name='pages-contact'),
    path('users-profile' ,views.user_profile , name='users-profile'),
    path('pages-faq' ,views.faq , name='pages-faq'),



    #for get and post between database and frontend
    path('get_favorite_stocks/', views.get_favorite_stocks, name='get_favorite_stocks'),
    path('save_favorite_stocks/', views.save_favorite_stocks, name='save_favorite_stocks'),

    path('save_plans/', views.save_plans, name='save_plans'),
    path('get_plans/', views.get_plans, name='get_plans'),

    path('save_wallet/', views.save_wallet, name='save_wallet'),
    path('get_wallet/', views.get_wallet, name='get_wallet'),


    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('delete_profile_picture/', views.delete_profile_picture, name='delete_profile_picture'),

    #for testing
    # # path('test' ,views.test , name='test'),
    # path('calc/' ,views.calculate , name='utrade'),
    # path('test/', views.sum_numbers, name='sum_numbers'),


    path('get_stock_data/', views.get_stock_data, name='get_stock_data'),
    path('add_stock_data/', views.add_stock_data, name='add_stock_data'),



    #news_predictions (step 3) create a url for the route then (step 4) after makemigerations, ==>python manage.py migrate --fake UTRADE  
    path('news_predictions/', views.news_prediction_json, name='news_prediction_json'),
    path('financial_predictions/', views.financial_prediction_json, name='financial_prediction_json'),
    path('predictions/', views.prediction_list_json, name='prediction_list_json'),
]


