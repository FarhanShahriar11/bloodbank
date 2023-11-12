from django.urls import path
from .views import *
urlpatterns = [
    path('', index, name='index'),
    path('requests/', request_list, name='request_list'),
    path('requests/<int:id>', request_detail, name='request_detail'),

    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),

    path('user/', user_index, name='user_index'),

    path('user/requests/', donor_request_list, name='user_request_list'),
    path('user/requests/<int:pk>', donor_request_detail, name='user_request_detail'),
    path('user/requests/new/', donor_request_add, name='user_request_add'),

    path('user/donations/', donor_donation_list, name='user_donation_list'),
    path('user/donations/new/', donor_donation_add, name='user_donation_add'),

    path('user/profile/', donor_profile, name='user_profile'),

    path('staff/', staff_index, name='staff_index'),

    path('staff/requests/', staff_request_list, name='staff_request_list'),
    path('staff/requests/<int:pk>', staff_request_detail, name='staff_request_detail'),

    path('staff/donors/', staff_donor_list, name='staff_donor_list'),
    path('staff/donors/new/', staff_donor_add, name='staff_donor_add'),

    path('staff/stocks/', staff_stock_list, name='staff_stock_list'),
    path('staff/stocks/<int:pk>/', staff_stock_detail, name='staff_stock_detail'),
    path('staff/stocks/new/', staff_stock_add, name='staff_stock_add'),


]