from rest_framework.authtoken.views import obtain_auth_token # As through this from rest_framework.authtoken we have views and in this class or may be a function obtain_auth_token is written that is imported here
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
from django.urls import path,include
from . import views
urlpatterns = [
    path('login/',obtain_auth_token,name='login'),
    path('register/',views.registration,name='register'),
    path('logout/',views.logout,name='logout'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')

]
