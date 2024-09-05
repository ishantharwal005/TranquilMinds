from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from apps.message.models import Message

from django.db.models import Max, OuterRef, Subquery
from apps.message.models import Message
from rest_framework.views import APIView
from rest_framework.response import Response

class ActiveChatsList(APIView):
    def get(self, request, therapist_id):
        # First, find the latest message timestamp for each sender to the therapist
        latest_messages = Message.objects.filter(
            recipientid=therapist_id
        ).values(
            'senderid'
        ).annotate(
            latest_timestamp=Max('timestamp')
        ).values('senderid', 'latest_timestamp')

        # Then, query the messages again to get the details of these latest messages
        latest_messages_details = Message.objects.filter(
            timestamp=Subquery(
                latest_messages.filter(senderid=OuterRef('senderid')).values('latest_timestamp')[:1]
            ),
            senderid=Subquery(
                latest_messages.filter(senderid=OuterRef('senderid')).values('senderid')[:1]
            ),
            recipientid=therapist_id
        )

        # Format the response
        active_chats = [
            {
                'senderid': message.senderid,
                'latest_message': message.content,
                'timestamp': message.timestamp
            } for message in latest_messages_details
        ]

        return Response({"active_chats": active_chats})