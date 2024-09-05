from django.conf.urls import url
from apps.user.views import *


urlpatterns = [
     url(r'^user/$', UserCRUD.as_view(), name= "User CRUD"),
     url(r'^user/(?P<userid>[A-Za-z0-9]+)/$', UserCRUD.as_view(), name="User CRUD"),

     url(r'^login/$', UserLogin.as_view(), name= "User Login"),
]