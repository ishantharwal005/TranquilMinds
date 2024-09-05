from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.user.serializers import *
from apps.user.models import *
from django.db import connection
from apps.utils import dictfetchall as dictfetchall
import os
import sys
from apps.utils import *
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.


class UserLogin(APIView):
    def post(self, request):
        success = False

        try: 
            request_data = request.data
            username = request_data['username']
            password = request_data['password']

            pwd = 'SELECT * from user WHERE username = %s'
            with connection.cursor() as c:
                c.execute(pwd, [username])
                user = dictfetchall(c)
            
            if not user:
                return Response({'Success' : success, 'Message' : 'User is invalid or is inactive'}, status=400)
            
            if check_password(password, user[0]['password']):
                success = True
                return Response({'Success' : success, 'Message' : { 'userid': user[0]['userid'], 'usertype': user[0]['usertype']}}, status=200)
            else:
                return Response({'Success' : success, 'Message' : 'Incorrect password'}, status=400)
            
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            errorresp=f'Error: {str(err)} at line no {exc_tb.tb_lineno}'
            WriteErrorLogs('UserLogin', get_method, str("request_data"), errorresp)
            print(exc_type, fname, exc_tb.tb_lineno)
            return Response({'Success' : success, 'Error' : str(err)}, status=400) 

class UserCRUD(APIView):

    def get(self, request, userid = None):

        success = False      
        try:
            if userid:
                get = 'SELECT * FROM user WHERE userid = %s'
                with connection.cursor() as c:
                    c.execute(get, [userid])
                    row = dictfetchall(c)
                success = True
            else:
                get = 'SELECT * FROM user WHERE active = True'
                with connection.cursor() as c:
                    c.execute(get)
                    row = dictfetchall(c)
                success = True

            return Response({'Success' : success, 'Message' : row}, status=200)
            
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            errorresp=f'Error: {str(err)} at line no {exc_tb.tb_lineno}'
            WriteErrorLogs('UserCRUD', get_method, str("request_data"), errorresp)
            print(exc_type, fname, exc_tb.tb_lineno)
            return Response({'Success' : success, 'Error' : str(err)}, status=400) 

    def post(self, request):

        success = False

        try:
            request_data = request.data
            username = request_data['username']
            raw_password = request_data['password']
            email = request_data['email']
            usertype = request_data['usertype']
            name = request_data['name']
            contact = request_data['contact']
            dob = request_data['dob']
            active = request_data.get('active', 1)
            
            hashed_password = make_password(raw_password)
            serializer = userSerializer(data = request.data)

            if serializer.is_valid():
                add = 'INSERT INTO user (username, password, email, usertype, name, contact, dob, active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'


                with connection.cursor() as c:
                    c.execute(add, [username, hashed_password, email, usertype, name, contact, dob, active])

                get = 'SELECT * FROM user ORDER BY userid DESC LIMIT 1'
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
            WriteErrorLogs('UserCRUD', post_method, str(request_data), errorresp)
            print(exc_type, fname, exc_tb.tb_lineno)
            return Response({'Success' : success, 'Error' : str(err)}, status=400)
        
    def patch(self, request):

        success = False

        try:
            request_data = request.data
            userid = request_data['userid']

            try:
                user_obj = UserModel.objects.get(userid = userid)
            except:
                raise Exception({'Success': success, 'Error': 'Not Found'})
            
            username = request_data.get('username', user_obj.username)
            password = request_data.get('password', user_obj.password)
            email = request_data.get('email', user_obj.email)
            usertype = request_data.get('usertype', user_obj.usertype)
            name = request_data.get('name', user_obj.name)
            contact = request_data.get('contact', user_obj.contact)
            dob = request_data.get('dob', user_obj.dob)
            active = request_data.get('active', user_obj.active)
            

            update = 'UPDATE user SET username = %s, password = %s, email = %s, usertype = %s, name = %s, contact = %s, dob = %s, active = %s WHERE userid = %s'
            with connection.cursor() as c:
                c.execute(update, [username, password, email, usertype, name, contact, dob, active, userid])
            success = True
            return Response({'Success': success, 'Message': 'Updated Successfully'}, status=200)
            
            
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            errorresp=f'Error: {str(err)} at line no {exc_tb.tb_lineno}'
            WriteErrorLogs('UserCRUD', patch_method, str(request_data), errorresp)
            print(exc_type, fname, exc_tb.tb_lineno)
            return Response({'Success' : success, 'Error' : str(err)}, status=400)
        
    def delete(self, request):

        success = False

        try:
            request_data = request.data
            userid = request_data['userid']
            
            delete = f'UPDATE user SET active = False WHERE userid = {userid}'
            with connection.cursor() as c:
                    c.execute(delete)
            success = True
            return Response({'Success' : success, 'Message': 'Deleted'}, status = 200)
           

        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            errorresp=f'Error: {str(err)} at line no {exc_tb.tb_lineno}'
            WriteErrorLogs('UserCRUD', delete_method, str(request_data), errorresp)
            print(exc_type, fname, exc_tb.tb_lineno)
            return Response({'Success' : success, 'Error' : str(err)}, status=400) 