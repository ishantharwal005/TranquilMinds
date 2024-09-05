from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.therapist.serializers import *
from apps.therapist.models import *
from django.db import connection
from apps.utils import dictfetchall as dictfetchall
import os
import sys
from apps.utils import *


class TherapistCRUD(APIView):

    def get(self, request, therapistid = None):

        success = False      
        try:
            if therapistid:
                get = 'SELECT * FROM therapist WHERE therapistid = %s'
                with connection.cursor() as c:
                    c.execute(get, [therapistid])
                    row = dictfetchall(c)
                success = True
            else:
                get = 'SELECT therapist.*, user.name AS therapistname FROM therapist JOIN user ON therapist.userid = user.userid WHERE therapist.active = True'
                with connection.cursor() as c:
                    c.execute(get)
                    row = dictfetchall(c)
                success = True

            return Response({'Success' : success, 'Message' : row}, status=200)
            
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            errorresp=f'Error: {str(err)} at line no {exc_tb.tb_lineno}'
            WriteErrorLogs('TherapistCRUD', get_method, str("request_data"), errorresp)
            print(exc_type, fname, exc_tb.tb_lineno)
            return Response({'Success' : success, 'Error' : str(err)}, status=400) 

    def post(self, request):

        success = False

        try:
            request_data = request.data
            userid = request_data['userid']
            bio = request_data['bio']
            specialiazation = request_data['specialiazation']
            experience = request_data['experience']
            education = request_data['education']
            active = request_data.get('active', 1)
            
        
            serializer = therapistSerializer(data = request.data)

            if serializer.is_valid():
                add = 'INSERT INTO therapist (userid, bio, specialiazation, education, experience, active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'


                with connection.cursor() as c:
                    c.execute(add, [userid, bio, specialiazation, education, experience, active])

                get = 'SELECT * FROM therapist ORDER BY userid DESC LIMIT 1'
                with connection.cursor() as c:
                    c.execute(get)
                    row = dictfetchall(c)
                success = True

                return Response({'Success' : success, 'Message' : row}, status=200)
            
            else:
                return Response({'Success': success, 'Error' : serializer.errors}, status=400)

        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            errorresp=f'Error: {str(err)} at line no {exc_tb.tb_lineno}'
            WriteErrorLogs('TherapistCRUD', post_method, str(request_data), errorresp)
            print(exc_type, fname, exc_tb.tb_lineno)
            return Response({'Success' : success, 'Error' : str(err)}, status=400)