from django.urls import path
from . import views

# Added all of the URLs which are used in this application
urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('', views.request_ride, name="request_ride"),
    path('request_ride/', views.request_ride, name="request_ride"),
    path('ride_status/', views.ride_status, name="ride_status"),
    path('accept_reject_ride/', views.accept_reject_ride, name="accept_reject_ride"),
    path('leader_board/', views.leader_board, name="leader_board"),
    path('car_registration/', views.car_registration, name="car_registration"),
    path('car_registration_update/<str:pk>/', views.car_registration_update, name="car_registration_update"),
    path('car_registration_delete/<str:pk>/', views.car_registration_delete, name="car_registration_delete"),
    path('ride_insert/', views.ride_insert, name="ride_insert"),
    path('ride_update/<str:pk>/', views.ride_update, name="ride_update"),
    path('ride_delete/<str:pk>/', views.ride_delete, name="ride_delete"),
    path('member_profile/', views.member_profile, name="member_profile"),
    path('instructions/', views.instructions, name="instructions"),
    # path('create_ride/<str:pk_test>/', views.create_ride, name="create_ride"),
    # path('car_registration/<str:pk_test>/', views.car_registration, name="car_registration"),
    # path('member_profile/<str:pk_test>/', views.member_profile, name="member_profile"),

]
