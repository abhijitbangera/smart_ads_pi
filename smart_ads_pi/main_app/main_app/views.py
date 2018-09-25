from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from localpi.models import adsDetails
import re
from pytube import YouTube
import os
import urllib
import urlparse
import shutil
import time

def download_image(url, file_name):
    # get the extension
    path = urlparse.urlparse(url).path
    ext = os.path.splitext(path)[1]

    file_path = os.getcwd()+os.sep+'static'+os.sep+'static_dirs'+os.sep+file_name+ext
    exists = os.path.isfile(file_path)

    print ('ext is:', ext)
    print ('file path:', file_path)
    if exists:
        print('removing image file:', file_path)

        os.remove(file_path)
    urllib.urlretrieve(url, file_name+ext)
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

def parse_url(value_from_db, file_name):
    print ('inside parse_url')
    # url='https://www.youtube.com/watch?v=KQScNzvwdnw'
    r_url = re.compile(r"^https?://www.youtube.com")
    r_image = re.compile(r".*\.(jpg|png)$")
    r_gif = re.compile(r".*\.(gif)$")
    print (value_from_db)
    # Add code to do a flag check to see if update is available, only then go to download, else return from the url text itself.
    if r_url.match(value_from_db):
        print ('value_from_db is video')
        download_youtube_video(value_from_db, file_name)
        return 'video'
    elif r_image.match(value_from_db):
        download_image(value_from_db, file_name)
        print('value_from_db is image/gif')
        return 'img'
    elif r_gif.match(value_from_db):
        download_image(value_from_db, file_name)
        print('value_from_db is gif')
        return 'gif'
    else:
        print ('error')
        return 'error'


def test(request):
    my_record = adsDetails.objects.filter(client_id_id=request.user.id).values()
    ad_header = my_record[0]['header'] #ad1
    ad_left_top = parse_url(my_record[0]['left_top'], '2') #ad2
    ad_left_bottom = parse_url(my_record[0]['left_bottom'], '3') #ad3
    ad_right_bottom = parse_url(my_record[0]['right_bottom'],'4') #ad4
    ad_right_top = parse_url(my_record[0]['right_top'],'5') #ad5
    ad_footer = parse_url(my_record[0]['footer'],'6') #ad6
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
