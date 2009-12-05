import sys,os
import time
import re
import shutil
from cement.exceptions import *
from cement.logging import get_logger
from configobj import ConfigObj
from string import strip
import inspect
import tempfile
import tarfile

log = get_logger(__name__)

def create_tgz(src_dir, dst_file):
    orig_dir = os.curdir
    dir_name = os.path.basename(src_dir.rstrip('/'))
    file_check = os.path.exists(
        os.path.join(os.curdir, '%s.tgz' % os.path.basename(src_dir))
        )
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
    dir_name = t.getnames()[0]
    t.extractall(path=dst_dir)
    t.close()
    
def convert_bytes(bytes):
    bytes = float(bytes)
    if bytes >= 1099511627776:
        terabytes = bytes / 1099511627776
        size = '%.2fT' % terabytes
    elif bytes >= 1073741824:
        gigabytes = bytes / 1073741824
        size = '%.2fG' % gigabytes
    elif bytes >= 1048576:
        megabytes = bytes / 1048576
        size = '%.2fM' % megabytes
    elif bytes >= 1024:
        kilobytes = bytes / 1024
        size = '%.2fK' % kilobytes
    else:
        size = '%.2fb' % bytes
    return size
                       
def sort_dict(adict):
    return sorted(adict.items(), lambda x, y: cmp(x[1], y[1]))

    
def get_timestamp():
    log.debug('get_timestamp()')
    now = time.mktime(time.localtime())
    time_stamp = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime(now))
    return time_stamp
    
    
def get_db_timestamp():
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
    log.debug('copy_path()')
    shutil.copy(src_path, dest_path)
    log.debug('copied %s to %s' % (src_path, dest_path))


def validate_config(config):
    required_settings = [
        'config_source', 'config_file', 'debug', 'log_file', 'data_dir',
        'enabled_plugins', 'plugin_config_dir', 'plugins_dir', 
        'plugin_configs', 'app_name', 'datastore_type', 'tmp_dir'
        ]
    for s in required_settings:
        if not config.has_key(s):
            raise cementConfigError, "config['%s'] value missing!" % s