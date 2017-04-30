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

ntype = {
	"prev":{
		"小姐":"MISS",
		"女士":"MISS",
		"先生":"SIR",
		"总":"MR"
	},
	"tail":{
		"小":"SIR",
		"老":"SIR"
	}
};

tdata = dict();
data = common.readfile(sys.argv[1]);
for ty in ntype:
	for it in ntype[ty]:
		for dt in data:
			tdic = dict();
			if ty == 'prev':
				tdic['str'] = dt + it;
			elif ty == 'tail':
				tdic['str'] = it + dt;
			tdic['type'] = 'SB';
			tdic['stype'] = ntype[ty][it];
			tdata[tdic['str']] = tdic;

common.print_dic(tdata);
