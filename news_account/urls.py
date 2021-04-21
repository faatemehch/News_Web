from django.urls import path
from .views import (LoginView,
                    RegisterView,
                    Logout,
                    UserInformationView,
                    UpdateUserInformationView,

                    )

urlpatterns = [
    path( 'login', LoginView.as_view(), name='login' ),
    path( 'register', RegisterView.as_view(), name='register' ),
    path( 'logout', Logout.as_view(), name='logout' ),
    path( 'user_info/<id>/', UserInformationView.as_view(), name='user_info' ),
    path( 'update/<pk>/', UpdateUserInformationView.as_view(), name='update_user_info' ),
]
