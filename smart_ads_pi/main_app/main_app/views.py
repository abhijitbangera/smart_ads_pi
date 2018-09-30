from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from localpi.models import adsDetails
import re
from pytube import YouTube
import os
import urllib
try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse
import shutil
import time
import requests
import json
import main_app.settings as settings
from django.contrib.auth.models import User



def download_image(url, file_name):
    # get the extension
    path = urlparse(url).path
    ext = os.path.splitext(path)[1]

    file_path = os.getcwd()+os.sep+'static'+os.sep+'static_dirs'+os.sep+file_name+ext
    exists = os.path.isfile(file_path)

    print ('ext is:', ext)
    print ('file path:', file_path)
    if exists:
        print('removing image file:', file_path)

        os.remove(file_path)
    urllib.request.urlretrieve(url, file_name+ext)
    shutil.move(file_name+ext, file_path)
    return

def download_youtube_video(url, file_name):
    print ('downloading url:', url)
    print ('filename is:', os.getcwd()+os.sep+'static'+os.sep+'static_dirs'+os.sep+file_name)
    file_path= os.getcwd()+os.sep+'static'+os.sep+'static_dirs'+os.sep+file_name+'.mp4'
    exists = os.path.isfile(file_path)
    if exists:
        print('removing video file:', file_path)
        time.sleep(3)
        os.remove(file_path)
    yt = YouTube(url)
    yt.streams.first().download()
    os.rename(yt.streams.first().default_filename, file_path)
    return

def get_api(id):
    url= settings.url
    response = requests.get(url+'api/clientads/?id='+str(id))
    json_data = json.loads(response.text)
    print ('.....')
    print (json_data)
    print (User.objects.get(username=json_data[0]['client_id']))
    print ('.....')
    my_record = adsDetails.objects.get(client_id_id=User.objects.get(username=json_data[0]['client_id']))
    my_record.header=json_data[0]['header']
    my_record.left_top = json_data[0]['left_top']
    my_record.left_bottom = json_data[0]['left_bottom']
    my_record.right_top = json_data[0]['right_top']
    my_record.right_bottom = json_data[0]['right_bottom']
    my_record.footer = json_data[0]['footer']
    my_record.save()
    return json_data

def post_api(json_data, id):
    headers = {
        'Content-Type': "application/json",
        'Cache-Control': "no-cache",
    }

    url = settings.url
    print ('doing post operation')
    print (json_data)
    json_data[0]['client_id'] = str(id)
    data= json.dumps(json_data)

    print ('????')
    print (data)
    response = requests.post(url + 'api/post_clientads/', data=data, headers=headers)
    print (response)
    return

def parse_url(value_from_db, file_name, download_flag):
    if not value_from_db:
        return
    print ('inside parse_url')
    # url='https://www.youtube.com/watch?v=KQScNzvwdnw'
    r_url = re.compile(r"^https?://www.youtube.com")
    r_image = re.compile(r".*\.(jpg|png)$")
    r_gif = re.compile(r".*\.(gif)$")
    print (value_from_db)
    # Add code to do a flag check to see if update is available, only then go to download, else return from the url text itself.
    if r_url.match(value_from_db):
        print ('value_from_db is video')
        if download_flag:
            download_youtube_video(value_from_db, file_name)
        return 'video'
    elif r_image.match(value_from_db):
        print('value_from_db is image')
        if download_flag:
            download_image(value_from_db, file_name)
        return 'img'
    elif r_gif.match(value_from_db):
        print('value_from_db is gif')
        if download_flag:
            download_image(value_from_db, file_name)
        return 'gif'
    else:
        print ('value is text')
        return value_from_db


def test(request):
    my_record = adsDetails.objects.filter(client_id_id=settings.client_id).values()
    print (my_record)
    print (settings.client_id)
    # print (get_api(request.user.id))
    api_response = get_api(settings.client_id)
    download_flag=  (api_response[0]['update_flag'])
    ad_header = my_record[0]['header'] #ad1
    ad_left_top = parse_url(my_record[0]['left_top'], '2', download_flag) #ad2
    ad_left_bottom = parse_url(my_record[0]['left_bottom'], '3', download_flag) #ad3
    ad_right_bottom = parse_url(my_record[0]['right_bottom'],'4', download_flag) #ad4
    ad_right_top = parse_url(my_record[0]['right_top'],'5', download_flag) #ad5
    ad_footer = parse_url(my_record[0]['footer'],'6', download_flag) #ad6
    post_api(api_response, settings.client_id)
    context = {
        'ad_header':ad_header,
        'ad_left_top':ad_left_top,
        'ad_left_bottom':ad_left_bottom,
        'ad_right_bottom':ad_right_bottom,
        'ad_right_top':ad_right_top,
        'ad_footer':ad_footer
    }
    print (ad_header)
    return render(request, 'index2.html', context=context)
