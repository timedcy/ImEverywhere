#!/usr/bin/env python3
# -*- coding:utf8 -*-
# PEP 8 check with Pylint
"""
My tools
"""
import sys
import os
import time
import functools
import random
import string
import xlrd
import xlwt


def time_me(info="used", format="s"):
    def _time_me(fn):
        @functools.wraps(fn)
        def _wrapper(*args, **kwargs):
            start = time.clock()
            result = fn(*args, **kwargs)
            if format == "s":
                print("%s %s %s"%(fn.__name__, info, time.clock() - start), "s")
            elif format == "ms":
                print("%s %s %s" % (fn.__name__, info, 1000*(time.clock() - start)), "ms")
            return result
        return _wrapper
    return _time_me
	
  
def get_current_time(format="%Y-%m-%d-%H-%M-%S"):
    """
    Get current time with specific format string.
    """
    assert isinstance(format, str), "The format must be a string."
    return time.strftime(format, time.localtime())

def random_item(mylist):
    assert mylist is not None, "The list can not be None."
    item = mylist[random.randint(0, len(mylist)-1)]
    return item	
	
def file_replace(origin_filepath, new_filepath):
    with open(origin_filepath, 'w') as origin:
        with open(new_filepath, 'r') as new:
            for line in new.readlines():
                origin.write(line)

				
def change_known_hosts(database_name):
    assert isinstance(database_name, str), "The database name must be a string."
    origin_known_hosts = "C:/Users/10449/.neo4j/known_hosts"
    new_known_hosts = "C:/Users/10449/.neo4j/known_hosts_" + database_name
    file_replace(origin_known_hosts, new_known_hosts)
	
def get_data_excel(filepath):
    """Get excel source"""
    is_valid = False   
    try:
        # if it is xls
        if os.path.isfile(filepath):
            filename = os.path.basename(filepath)
            if filename.split('.')[1] == 'xls':
                is_valid = True
        data = None
        if is_valid:
            data = xlrd.open_workbook(filepath)
    except Exception as e:
        print('Error：%s' %e)
        return None
    return data
	
@time_me(format="ms")	
def test():
    print(get_current_time())
	

if __name__ == "__main__":
    test()		
	