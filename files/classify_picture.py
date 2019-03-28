# -*- coding: utf-8 -*-

"""
功能：对照片按照拍摄时间进行归类
"""

import shutil
import os
import time
import exifread


class ReadFailException(Exception):
    pass


def getOriginalDate(filename):
    try:
        fd = open(filename, 'rb')
    except BaseException as e:
        raise ReadFailException("unopen file[%s]\n" % filename)
    data = exifread.process_file(fd)
    if data:
        try:
            t = data['EXIF DateTimeOriginal']
            return str(t).replace(":", ".")[:7]
        except:
            pass
    state = os.stat(filename)
    return time.strftime("%Y.%m", time.localtime(state[-2]))


def classifyPictures(path):
    for root, dirs, files in os.walk(path, True):
        dirs[:] = []
        for filename1 in files:
            filename = os.path.join(root, filename1)
            f, e = os.path.splitext(filename)
            if e.lower() not in ('.jpg', '.png', '.mp4'):
                continue
            info = "文件名: " + filename + " "
            t = ""
            try:
                t = getOriginalDate(filename)
            except Exception as e:
                print(e)
                continue
            info = info + "拍摄时间：" + t + " "
            pwd = os.path.join(root, t)
            dst = os.path.join(pwd, filename1)
            if not os.path.exists(pwd):
                os.mkdir(pwd)
            print(info, dst)
            shutil.copy2(filename, dst)
            # os.remove(filename)


if __name__ == "__main__":
    path = "/Users/daren/temp/aa/origin"
    classifyPictures(path)
