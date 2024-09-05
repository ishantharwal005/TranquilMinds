from django.conf.urls import url
from apps.message.views import ActiveChatsList

urlpatterns = [
    url(r'^active_chats/(?P<therapist_id>[A-Za-z0-9]+)/$', ActiveChatsList.as_view(), name='active_chats'),
]