from django.conf.urls import url
from apps.therapist.views import *


urlpatterns = [
     url(r'^therapist/$', TherapistCRUD.as_view(), name= "Therapist CRUD"),
     url(r'^therapist/(?P<therapist>[A-Za-z0-9]+)/$', TherapistCRUD.as_view(), name="Therapist CRUD"),

     # url(r'^login/$', TherapistLogin.as_view(), name= "Therapist Login"),
]