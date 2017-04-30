#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8');
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../commons'));
import common

if len(sys.argv) <= 1:
	print 'Usage:%s infile' %sys.argv[0];

data = common.readfile(sys.argv[1]);
for dt in data:
	for dc in dt:
		print dc;

