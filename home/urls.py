from django.urls import path
from home.views import *


urlpatterns = [
	path('api/signup/', SignupAPI.as_view(), name="api-signup"),
	path('api/verify/<token>/',VerifyUserAPI.as_view(), name="api-verify"),
	path('api/login/', LoginAPI.as_view(), name="api-login"),
	
]