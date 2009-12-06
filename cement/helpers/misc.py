"""Misc Cement helper methods."""

import os
import time
import re
import shutil
import tempfile
import tarfile

from cement.core.log import get_logger
from cement.core.exc import CementIOError

log = get_logger(__name__)

def create_tgz(src_dir, dst_file):
    orig_dir = os.curdir
    dir_name = os.path.basename(src_dir.rstrip('/'))
    if os.path.exists(dst_file):
        raise CementIOError, \
            "%s already exists!" % os.path.basename(dst_file)
    
    tmp_dir = tempfile.mkdtemp()
    os.chdir(tmp_dir)

    shutil.copytree(
        src_dir, os.path.join(tmp_dir, dir_name)
        )
    t = tarfile.open(dst_file, 'w:gz')
    t.add('./%s' % dir_name)
    t.close()
    os.chdir(orig_dir)
    shutil.rmtree(tmp_dir)
    
    
def extract_tgz(src_file, dst_dir):
    t = tarfile.open(src_file, 'r:gz')
    t.extractall(path=dst_dir)
    t.close()
    
def convert_bytes(_bytes):
    """
    Convert bytes to a more appropriate human readable number.
    """
    _bytes = float(_bytes)
    if _bytes >= 1099511627776:
        terabytes = _bytes / 1099511627776
        size = '%.2fT' % terabytes
    elif _bytes >= 1073741824:
        gigabytes = _bytes / 1073741824
        size = '%.2fG' % gigabytes
    elif _bytes >= 1048576:
        megabytes = _bytes / 1048576
        size = '%.2fM' % megabytes
    elif _bytes >= 1024:
        kilobytes = _bytes / 1024
        size = '%.2fK' % kilobytes
    else:
        size = '%.2fb' % _bytes
    return size


def get_timestamp():
    """Get a timestamp."""
    log.debug('get_timestamp()')
    now = time.mktime(time.localtime())
    time_stamp = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime(now))
    return time_stamp
    
    
def get_db_timestamp():
    """Get a database savvy timestamp."""
    log.debug('get_db_timestamp()')
    now = time.mktime(time.localtime())
    time_stamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
    return time_stamp


def sub_special_characters(text):
    """Replaces all the "special characters" in a string with '_'."""
    log.debug('sub_special_characters()')
    text = re.sub(' ', '_', str(text))
    text = re.sub(r"[^A-Za-z0-9\.]", "-", text)
    return text 


def copy_path(src_path, dest_path):
    """Copy a src path to a destination path."""
    log.debug('copy_path()')
    shutil.copy(src_path, dest_path)
    log.debug('copied %s to %s' % (src_path, dest_path))


