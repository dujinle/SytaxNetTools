#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8');
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../commons'));
import common

if len(sys.argv) <= 2:
	print 'Usage:%s infile type desc' %sys.argv[0];
	sys.exit(-1);

tp = desc = None;
if len(sys.argv) > 2:
	tp = sys.argv[2];
if len(sys.argv) > 3:
	desc = sys.argv[3]
data = common.read_json(sys.argv[1]);
for dt in data.keys():
	tda = data[dt];
	if not tda.has_key('type') and not tp is None:
		tda['type'] = tp;
	if not tda.has_key('str'):
		tda['str'] = dt;
	if not desc is None:
		tda['desc'] = list();
		tda['desc'].append(desc);

common.print_dic(data);
