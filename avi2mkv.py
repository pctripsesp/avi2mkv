import os
import subprocess
import datetime

## CHANGE THIS!!!
# EXAMPLE: '/home/user/usb1'
MEDIA_PATH = '<YOUR_PATH_FILES>'


def avi2mkv(AVI_PATH, filename):
    if not AVI_PATH.endswith("/"):
        AVI_PATH += "/"
    subprocess.run(["ffmpeg", "-i", AVI_PATH+filename, AVI_PATH+filename[:-4]+'.mkv'])
    ### TEMPORAL
    subprocess.run(["mv", AVI_PATH+filename, AVI_PATH+'DELETE_'+filename])

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
                update_logs("SUCCESS")
            # IF IS FOLDER CHECKS INTO IT
            if os.path.isdir(DIR_PATH+ls_file):
                look_for_avi(DIR_PATH+ls_file)


def update_logs(log_message):
    with open("logs.txt", "a+") as file:
        file.write("\n"+str(datetime.datetime.now()) + ' ---> ' + log_message)


look_for_avi(MEDIA_PATH)
