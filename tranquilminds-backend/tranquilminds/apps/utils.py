# from os import confstr
from rest_framework.response import Response
import requests
from django.http import response
# from apps.domain.models import DomainParams
import base64
from datetime import datetime
import requests
import random
from random import seed
from random import randint
from django.db import connection
from datetime import timedelta
import pytz

calendar_schema = "calen"
calendar_table = "calendar"
calmarkdata_table = "calmarkdata"
calmarktype_table = "calmarktype"
caldaysummary_table = "caldaysummary"

#status
passive = 0
active = 1
revert = 2
cancel = 3
finish = 4
pending = 1

IST = pytz.timezone('Asia/kolkata')


def Convert_String(string):
    li = list(string.split(","))
    return li


def formatForBlob(data):
    for item in data:
        for key, value in item.items():
            if key == 'logo' or key == 'logohd' or key == 'logohighres' or key == 'itemlogo' or key == 'fssaiimage' or key == 'image':
                if value:
                    convertedimage = base64.b64encode(value)
                    item[key] = convertedimage
    return data


def checkDataValidation(request_data, values):
    try:
        for value in values:

            # print(type(request_data[value['key']]), value['type'])

            fromValue = value.get('fromValue', None)
            toValue = value.get('toValue', None)
            if value['isCompulsory'] == True:
                if(request_data.get(value['key'], None) == None):
                    raise Exception(f'''{value['key']} is compulsary''')
            if type(request_data[value['key']]) != value['type']:
                if type(request_data[value['key']]) == 'int':
                    request_data[value['key']] = request_data[value['key']]
                    if type(request_data[value['key']]) != (value['type']):
                        raise Exception(
                            f'''{value['key']} should be a {value['type']}''')
                else:
                    raise Exception(
                        f'''{value['key']} should be a {value['type']}''')

            if fromValue and toValue:
                if int(request_data[value['key']]) >= fromValue and int(request_data[value['key']]) <= toValue:
                    pass
                else:
                    raise Exception(f'''Invalid value for {value['key']} ''')
            if fromValue and toValue == None:

                if int(request_data[value['key']]) >= fromValue:
                    pass
                else:
                    raise Exception(f'''Invalid value for {value['key']} ''')
            if fromValue == None and toValue:

                if int(request_data[value['key']]) <= toValue:
                    pass
                else:
                    raise Exception(f'''Invalid value for {value['key']} ''')

        return request_data

    except Exception as err:
        import os
        import sys
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(str(err))
        raise Exception(str(err))


def validateData(request_data, model):
    try:
        for key in model:
            if(request_data.get(key, None) == None):
                return {"Success": False, "Message": key+" is required."}
        return {"Success": True}
    except Exception as err:
        return {"Success": False, "Message": str(err)}


def validate_required_parameters(request, required_params):
    success = True
    if request.method == 'POST' or request.method == 'PATCH':
        for parameter in required_params:
            success = success and request.data.__contains__(parameter)
    else:
        for parameter in required_params:
            success = success and request.GET.__contains__(parameter)
    if success is False:
        raise Exception(
            'parameter' + ' , '.join(required_params) + 'is/are required')


def convert_blob(convert_from, image_to_convert):
    if convert_from == 'blob':
        res = bytes(image_to_convert, 'utf-8')
        return res
    elif convert_from == 'base64':
        res = base64.b64decode(image_to_convert)
        return res


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]

    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def subtractDays(fromDateString, days):
    fromDate = datetime.strptime(str(fromDateString), "%Y%m%d")
    toDate = fromDate - timedelta(days=days)
    toDate = toDate.strftime("%Y%m%d")
    return toDate


def addDays(fromDateString, days):
    fromDate = datetime.strptime(str(fromDateString), "%Y%m%d")
    toDate = fromDate + timedelta(days=days)
    toDate = toDate.strftime("%Y%m%d")
    return toDate


def dictfetchone(cursor):
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    return {
        dict(columns, row)
        # for row in cursor.fetchone()
    }


# def check_if_day_open(domainrecno, today):

#     beginday = DomainParams.objects.get(domainrecno=domainrecno)
#     if beginday.today == today and beginday.dayopen == True:
#         return True
#     else:
#         return False


def write_logs(input):
    f = open("./custom.log", "a")
    f.writelines(input)
    f.close()


def write_logs_customer_app_success(apiName, data):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    date = now.strftime("%d%m%y")
    f = open(f"./Logs/customerapp{date}.log", "a")
    f.writelines(
        [f'\n \n SUCCESS at {apiName} at : {dt_string} \n', f'Request Data : {data}'])
    f.close()


def write_logs_customer_app_error(apiName, data, err, lineNo):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    date = now.strftime("%d%m%y")
    f = open(f"./Logs/customerapp{date}.log", "a")
    f.writelines([f'\n \n ERROR at {apiName} at : {dt_string} \n',
                 f'Request Data : {data} \n', f'Error is {err} at {lineNo}'])
    f.close()


def write_logs_customer_app(apiName, data):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    date = now.strftime("%d%m%y")
    f = open(f"./Logs/customerapp{date}.log", "a")
    f.writelines(
        [f'\n \n SUCCESS at {apiName} at : {dt_string} \n', f'Request Data : {data}'])
    f.close()


def write_logs_success(apiName, data):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    date = now.strftime("%d%m%y")
    f = open(f"./Logs/custom{date}.log", "a")
    f.writelines(
        [f'\n \n SUCCESS at {apiName} at : {dt_string} \n', f'Request Data : {data}'])
    f.close()


def write_logs_sql(apiName, data):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    date = now.strftime("%d%m%y")
    f = open(f"./Logs/localConsole{date}.log", "a")
    f.writelines([f'\n \n{apiName} at : {dt_string} \n', f'{data}'])
    f.close()


def write_logs_error(apiName, data, err, lineNo):
    # now = datetime.now()
    # dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    # date = now.strftime("%d%m%y")
    # f = open(
    #     f"/home/sutraydev04/PythonProjects/bcorelogs/custom{date}.log", "a")
    # # f = open(f"./Logs/custom{date}.log", "a")
    # f.writelines([f'\n \n ERROR at {apiName} at : {dt_string} \n',
    #              f'Request Data : {data} \n', f'Error is {err} at {lineNo}'])
    # f.close()
    pass


def write_logs_SCM_data(apiName, data, data_response):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    f = open("./SCM_Logs2.log", "a")
    f.writelines([f'\n \n AT {dt_string} Api Called {apiName} \n ',
                 f'Data Object Sent - {data} \n ', f'Response - {data_response}'])


def write_API_Called(apiName, data):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    date = now.strftime("%d%m%y")
    f = open(f"./Logs/ApiCalledLogs{date}.log", "a")
    f.writelines(
        [f'\n \n AT {apiName} Api Called {dt_string} \n ', f'Data Object Sent - {data} \n '])


def sendNotifications(to, title, body, type, extradata):
    try:
        url = 'https://fcm.googleapis.com/fcm/send'
        data = {
            "to": str(to),
            "notification": {
                "title": str(title),
                "body": str(body)
            },
            "data": {
                **extradata,
                "autoHide": False,
                "type": str(type),
                "visibilityTime": 00
            }
        }
        headers = {
            "Authorization": "key=AAAAn3v0ywo:APA91bHgoEDpKAV3X2zwMaMoi6tQMWCJbIOXKl9J-XdvS7FiNy00ilPlVuS3YG1YLod8t7LSyENXUCA9o8eI4Wzbhwi_W6L8lJFoFilA7KFjVdUUSzEzyaWisNFssZvQt5sLGlHJ2Nzr"
        }

        r = requests.post(url, headers=headers, json=data, verify=True)
        r.raise_for_status()

        response = r.json()
        return response
    except Exception as err:
        return "sendNotifications" + str(err)


def WebMobNotification(to, title, body, type, extradata):
    try:

        url = 'https://fcm.googleapis.com/fcm/send'
        data = {
            "to": str(to),
            "notification": {
                "title": str(title),
                "body": str(body)
            },
            "data": {
                # **extradata,
                "autoHide": False,
                "type": str(type),
                "visibilityTime": 00
            }
        }
        headers = {
            "Authorization": "key=AAAA3CO-EAQ:APA91bHiIgCOV_s0ZuLBjwRKr1p2--9skJQjFXBfobRCyh6jWeK6M5JteKVQVkrnMPB-zHOPckCiEErsMtOWvJ9BIkie_Wtt-D5rneU13yTdV8ztTi8mnMuhGw4K5Ciw4EU1O4OdXouz"
        }

        r = requests.post(url, headers=headers, json=data, verify=True)
        r.raise_for_status()
        # print("data", data)
        # print("r", r)
        response = r.json()
        # print("response", response)
        return response
    except Exception as err:
        return "WebNotifications" + str(err)


def analyticsNotifications(to, title, body, type):
    try:
        url = 'https://fcm.googleapis.com/fcm/send'
        data = {
            "to": "cI1sDCVNThqbxukj5kuUT3:APA91bE-Ua5HCaLx2BywlqNNPaNC_xkuTAE4OvUMPQgHZm1-2Q2as1JRZ4L4i1uL7Z85zbIvMMkH1IMQe3hDFlaQHVlEBQQZ6taKDymCG-K7eKS1AgHJk6XIRp4mUaQtFAK-nc8F94Lb",
            "notification": {
                "title": str(title),
                "body": str(body)
            },
            "data": {
                "autoHide": False,
                "type": str(type),
                "visibilityTime": 00
            }
        }
        headers = {
            "Authorization": "key= AAAA7UsdRS4:APA91bFLM9c8dwnbZyqneTw7jn1Xp5KeNd6zT7IB_CvsUps6FMv2N5xXxlqmHWLKTcp5RSwtdD3TNriUZ4t9pyyo_537VwDk5p0DVOusmnojxvzHitf7KfWUJMsBjUqKAyqI1A8Qzxrd"
        }

        r = requests.post(url, headers=headers, json=data, verify=False)
        r.raise_for_status()

        response = r.json()
        return response
    except Exception as err:
        return "sendNotifications" + str(err)


def analyticsNotifications(to, title, body, type):
    try:
        url = 'https://fcm.googleapis.com/fcm/send'
        data = {
            "to": "cI1sDCVNThqbxukj5kuUT3:APA91bE-Ua5HCaLx2BywlqNNPaNC_xkuTAE4OvUMPQgHZm1-2Q2as1JRZ4L4i1uL7Z85zbIvMMkH1IMQe3hDFlaQHVlEBQQZ6taKDymCG-K7eKS1AgHJk6XIRp4mUaQtFAK-nc8F94Lb",
            "notification": {
                "title": str(title),
                "body": str(body)
            },
            "data": {
                "autoHide": False,
                "type": str(type),
                "visibilityTime": 00
            }
        }
        headers = {
            "Authorization": "key= AAAA7UsdRS4:APA91bFLM9c8dwnbZyqneTw7jn1Xp5KeNd6zT7IB_CvsUps6FMv2N5xXxlqmHWLKTcp5RSwtdD3TNriUZ4t9pyyo_537VwDk5p0DVOusmnojxvzHitf7KfWUJMsBjUqKAyqI1A8Qzxrd"
        }

        r = requests.post(url, headers=headers, json=data, verify=False)
        r.raise_for_status()

        response = r.json()
        return str(response["results"][0]["message_id"])
    except Exception as err:
        return str(err)


def sendsqlNotifications(to, title, body, type, sqltype, sqlstr):
    try:
        url = 'https://fcm.googleapis.com/fcm/send'
        data = {
            "to": str(to),
            "notification": {
                "title": str(title),
                "body": str(body)
            },
            "data": {
                "autoHide": False,
                "type": str(type),
                "sqltype": str(sqltype),
                "sqlstr": str(sqlstr),
                "visibilityTime": 00
            }
        }
        headers = {
            "Authorization": "key=AAAAn3v0ywo:APA91bHgoEDpKAV3X2zwMaMoi6tQMWCJbIOXKl9J-XdvS7FiNy00ilPlVuS3YG1YLod8t7LSyENXUCA9o8eI4Wzbhwi_W6L8lJFoFilA7KFjVdUUSzEzyaWisNFssZvQt5sLGlHJ2Nzr"
        }

        r = requests.post(url, headers=headers, json=data, verify=False)
        r.raise_for_status()
        response = r.json()
        return response
    except Exception as err:
        return str(err)


def sendOTP(to, otp):
    try:
        url = 'http://SMSnMMS.co.in/smsaspx?ID=vishvas.chitale@gmail.com&Pwd=pass1234&PhNo=' + \
            str(to) + '&Text=Your ChitaleSCM OTP is:' + str(otp) + \
            'Chitale Dairy.&TemplateID=1007772550413560692'
        r = requests.get(url, verify=False)
        r.raise_for_status()
        data = r.json()
        return True
    except Exception as err:
        return str(err)


def SendOTPonMobile(to, otp):
    try:
        url = 'http://108.170.57.10/sendsms/bulksms.php?username=allsutra&password=PEAj6YZV&type=TEXT&sender=MPFISD&mobile=919527997718&message=3608 is the One Time Password(OTP) for your registration and will be valid for 30 mins only. NEVER SHARE YOUR OTP WITH ANYONE.BANK NEVER CALLS TO VERIFY PASSWORD OR OTP. MPFI Project Consultancy Pvt Ltd.'

        r = requests.post(url, verify=False)
        r.raise_for_status()
        data = r.json()
        return True
    except Exception as err:
        return str(err)


def checkifblank(amount):
    if amount == '':
        amount = 0.00
    else:
        amount = float(amount)
    return amount


def getToday():
    now = datetime.now()
    date = now.strftime("%Y%m%d")
    return date


def getTime():
    now = datetime.now()
    time = now.strftime("%H%M%S")
    return time


def getlocaltime():
    datetime_ist = datetime.now(IST)
    curr_clock = datetime_ist.strftime("%H%M%S")
    return curr_clock


def getBillno():
    value = randint(1000000, 9999999)
    return value


def checkmonth():
    return datetime.now().strftime("%m")


def checkyear():
    return datetime.now().strftime("%Y")


today = datetime.now().strftime("%Y%m%d")
nowtime = datetime.now().strftime("%H%M%S")
# financialyear = 22
financialyear = 23


def validate_allparams(request_data):
#     # print("value", request_data)
#     if (request_data.get('itemrecno') != None) and (request_data.get('itemrecno') != "") and (request_data.get('itemrecno') > 0):
#         return request_data.get('itemrecno')

#     else:
#         raise serializers.ValidationError("Itemrecno must be int")
    pass


def getlocaltime():

    datetime_ist = datetime.now(IST)

    curr_clock = datetime_ist.strftime("%H%M%S")

    return curr_clock


def geteventtype(eventtype):

    if eventtype == 1:
        return "Action"

    if eventtype == 2:
        return "Referal"



def getquestiontype(questiontype):

    if questiontype == 1:
        return "Text Answer"

    if questiontype == 2:
        return " Capture Image"

    if questiontype == 3:
        return "MCQ"

    if questiontype == 4:
        return "True / False"

    if questiontype == 5:
        return " Multiple choise"

    if questiontype == 9:
        return "Internal"


#### api methods for error log function
post_method = 1
get_method = 2
patch_method = 3
delete_method = 4


def WriteErrorLogs(apiname, apimethod, requestbody, responsebody):
    trdate = datetime.now().strftime("%Y%m%d")
    trtime = getlocaltime()
    tenantrecno = 9

    adderror= ' INSERT INTO errorlog ( trdate, trtime, tenantrecno, apiname, apimethod, requestbody, responsebody ) VALUES ( %s, %s, %s, %s, %s, %s, %s )'
    with connection.cursor()as c:
        c.execute(adderror, [trdate, trtime, tenantrecno, apiname, apimethod, requestbody, responsebody])


def removespaces(string):
    return "".join(string.split())


def changedlog(tenantrecno, domainrecno, tablename, recno, method, fieldname, oldvalue, newvalue, domainuserrecno):
    trdate = datetime.now().strftime("%Y%m%d")
    trtime = getlocaltime()

    addchangedlog = " INSERT INTO changedlog ( tenantrecno, domainrecno, tablename, tablerecno, method, fieldname, oldvalue, newvalue, domainuserrecno, trdate, trtime ) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s ) "
    with connection.cursor() as c:
        c.execute(addchangedlog, [tenantrecno, domainrecno, tablename, recno, method, fieldname, oldvalue, newvalue, domainuserrecno, trdate, trtime])


def deletelog(tenantrecno, domainrecno, tablename, recno, method, domainuserrecno):
    trdate = datetime.now().strftime("%Y%m%d")
    trtime = getlocaltime()

    oldvalue=True 
    newvalue=False

    adddeletelog = " INSERT INTO changedlog ( tenantrecno, domainrecno, tablename, tablerecno, method, fieldname, oldvalue, newvalue, domainuserrecno, trdate, trtime ) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s ) "
    with connection.cursor() as c:
        c.execute(adddeletelog, [tenantrecno, domainrecno, tablename, recno, method, 'Record Deleted', oldvalue, newvalue, domainuserrecno, trdate, trtime])