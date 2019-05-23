# sudo apt-get install ffmpeg && sudo apt-get install mediainfo

import os
import subprocess
import datetime
import re

## CHANGE THIS!!!
# EXAMPLE: '/home/user/usb1'
MEDIA_PATH = '<YOUR_PATH_FILES>'


def avi2mkv(AVI_PATH, filename):
    if not AVI_PATH.endswith("/"):
        AVI_PATH += "/"
    subprocess.run(["ffmpeg", "-i", AVI_PATH+filename, AVI_PATH+filename[:-4]+'.mkv'])
    ### TEMPORAL
    subprocess.run(["mv", AVI_PATH+filename, AVI_PATH+'DELETE_'+filename])

    # CHECK FILES DURATION (we need to compare the second grep Duration that corresponds with video in mediainfo)
    avi_duration = subprocess.run("mediainfo " + AVI_PATH+'DELETE_'+filename + " | grep -m 2 Duration | tail -n1", stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8')
    avi_duration_clean = re.search(': (.*)', avi_duration).group(1)
    mkv_duration = subprocess.run("mediainfo " + AVI_PATH+filename[:-4]+'.mkv' + " | grep -m 2 Duration | tail -n1", stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8')
    mkv_duration_clean = re.search(': (.*)', mkv_duration).group(1)
    if avi_duration_clean == mkv_duration_clean:
        update_logs("SUCCESS")
        # DELETE OLD FILES
        subprocess.run(["rm", AVI_PATH+'DELETE_'+filename])
        update_logs("DELETED: " + AVI_PATH+'DELETE_'+filename+"\n")
    else:
        update_logs("++ FAILED CHECK DURATION --> AVI: "+avi_duration_clean+" VS MKV: "+mkv_duration_clean+"\n")



def look_for_avi(DIR_PATH):
    # CHECK PATH "/" AT THE END
    if not DIR_PATH.endswith("/"):
        DIR_PATH +="/"
    # LS ALL FILES FROM PATH
    ls_dir = []
    for e in os.listdir(DIR_PATH):
        ls_dir.append(e)

    # LOOP ALL .AVI FILES AND CONVERT AVI TO MKV FILES
    for ls_file in ls_dir:
        if not ls_file.startswith('.') and not ls_file.startswith('DELETE_'):
            if ls_file[-4:] == '.avi':
                update_logs("START AVI TO MKV: " + DIR_PATH+ls_file)
                avi2mkv(DIR_PATH, ls_file)
            # IF IS FOLDER CHECKS INTO IT
            if os.path.isdir(DIR_PATH+ls_file):
                look_for_avi(DIR_PATH+ls_file)


def update_logs(log_message):
    with open("logs.txt", "a+") as file:
        file.write("\n"+str(datetime.datetime.now()) + ' ---> ' + log_message)


look_for_avi(MEDIA_PATH)
