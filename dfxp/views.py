# -*- coding:utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views import generic

from .models import Choice, Poll
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import os
from pycaption import SAMIReader, DFXPWriter
from StringIO import StringIO
import os, mimetypes, urllib
from django.http import StreamingHttpResponse
import chardet
import pymongo
import re
import random


def Index(request):

    image_list = []
    for i in range(1, 4):
        image_list.append(random.randrange(1, 175))

    is_mobile = process_request(request)

    return render(request, 'index.html', {'image_list': image_list, 'is_mobile': is_mobile})


def error(request):
    return render(request, 'error.html', {'encoding': "iso-5589-2"})

@csrf_exempt
def upload(req):
    if req.method == 'POST':
        if 'file' in req.FILES:
            file = req.FILES['file']
            filename = file._name

            module_dir = os.path.dirname(__file__)+"/static/subtitle/"

            if file.content_type != "application/smil":
                return render(req, 'error.html', {'type': 'file'})

            filename += "to.dfpx"
            filename_chdt = chardet.detect(filename)
            #파일명이 아스키일 경우 uft-8 인코딩
            if filename_chdt["encoding"] == "ascii":
                filename = filename.encode('utf-8')

            #공백 _ 로 치환
            filename = re.sub(r"[\s\*]", "_", filename)

            #해당 파일이 이미 변환 되었는지 디비 검색
            connection = pymongo.MongoClient("localhost", 27017)
            db = connection.dfxpDB
            collection = db.file
            sql = {"filename": filename}
            row = collection.find_one(sql)

            pwd = module_dir+filename
            print module_dir

            file_data = ""
            for chunk in file.chunks():
                file_data += chunk

            chdt = chardet.detect(file_data)
            print "encoding : "+chdt['encoding']
            #파일 내용이 euc-kr 일경우 utf-8로 인코딩
            if chdt["encoding"] == "EUC-KR":
                file_data = unicode(file_data, 'euc-kr').encode('utf-8')
            elif chdt["encoding"] == "UTF-16LE":
                file_data = unicode(file_data, 'UTF-16LE').encode('utf-8')
            elif chdt["encoding"] == "utf-8":
                file_data = unicode(file_data, 'UTF-8').encode('utf-8')
            elif chdt["encoding"] == "ISO-8859-2":
                file_data = unicode(file_data, 'cp949').encode('utf-8')
            else:
                return render(req, 'error.html', {'type': 'encoding', 'encoding': chdt["encoding"]})
            # print file_data

            file_data = re.sub("<!--[\sa-zA-Zㄱ-ㅣ가-힣0-9\{\}\;\,\#\:\/\.\-\(\)\\\]+-->", "", file_data)

            #파일이 <sami>로 시작하지 않으면 에러 페이지로
            if file_data.find('<SAMI>') < 0:
                if file_data.find('<sami>') < 0:
                    return render(req, 'error.html', {'type': 'fake_smi'})
            #유니코드로 다시 인코딩
            file_data = file_data.decode('utf-8')

            #파일내의 주석 제거
            # file_data = re.sub("<!--[\sa-zA-Zㄱ-ㅣ가-힣0-9\{\}\;\,\#\:\/\.\-\(\)\\\]+-->", "", file_data)
            # print file_data
            #파일은 utf-8로 인코딩
            fp = open('%s/%s' % (module_dir, filename), 'wb')
            fp.write(DFXPWriter().write(SAMIReader().read(file_data)).encode('utf-8'))
            # fp.write(file_data.encode('utf-8'))
            fp.close()

            #디비 저장
            collection.insert({"filename": filename, "full_path": "/static/subtitle/"+filename})

            #파일 전송
            file_full_path = pwd.format(filename)
            response = StreamingHttpResponse((line for line in open(file_full_path, 'r')))
            response['Content-Disposition'] = "attachment; filename={0}".format(filename)
            response['Content-Length'] = os.path.getsize(file_full_path)
            return response
        #파일이 없다면 에러 페이지로
        return render(req, 'error.html', {'type': 'not_file'})
    #post가 아닌 접근이면 에러 페이지로
    return render(req, 'error.html', {'type': 'get'})


def process_request(request):
        is_mobile = False

        if request.META.has_key('HTTP_USER_AGENT'):
            user_agent = request.META['HTTP_USER_AGENT']

            # Test common mobile values.
            pattern = "(up.browser|up.link|mmp|symbian|smartphone|midp|wap|phone|windows ce|pda|mobile|mini|palm|netfront)"
            prog = re.compile(pattern, re.IGNORECASE)
            match = prog.search(user_agent)

            if match:
                is_mobile = True
            else:
                # Nokia like test for WAP browsers.
                # http://www.developershome.com/wap/xhtmlmp/xhtml_mp_tutorial.asp?page=mimeTypesFileExtension

                if request.META.has_key('HTTP_ACCEPT'):
                    http_accept = request.META['HTTP_ACCEPT']

                    pattern = "application/vnd\.wap\.xhtml\+xml"
                    prog = re.compile(pattern, re.IGNORECASE)

                    match = prog.search(http_accept)

                    if match:
                        is_mobile = True

            if not is_mobile:
                # Now we test the user_agent from a big list.
                user_agents_test = ("w3c ", "acs-", "alav", "alca", "amoi", "audi",
                                    "avan", "benq", "bird", "blac", "blaz", "brew",
                                    "cell", "cldc", "cmd-", "dang", "doco", "eric",
                                    "hipt", "inno", "ipaq", "java", "jigs", "kddi",
                                    "keji", "leno", "lg-c", "lg-d", "lg-g", "lge-",
                                    "maui", "maxo", "midp", "mits", "mmef", "mobi",
                                    "mot-", "moto", "mwbp", "nec-", "newt", "noki",
                                    "xda",  "palm", "pana", "pant", "phil", "play",
                                    "port", "prox", "qwap", "sage", "sams", "sany",
                                    "sch-", "sec-", "send", "seri", "sgh-", "shar",
                                    "sie-", "siem", "smal", "smar", "sony", "sph-",
                                    "symb", "t-mo", "teli", "tim-", "tosh", "tsm-",
                                    "upg1", "upsi", "vk-v", "voda", "wap-", "wapa",
                                    "wapi", "wapp", "wapr", "webc", "winw", "winw",
                                    "xda-",)

                test = user_agent[0:4].lower()
                if test in user_agents_test:
                    is_mobile = True

        return is_mobile
