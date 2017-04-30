#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys
reload(sys);
sys.setdefaultencoding('utf-8');

pos_list = dict();
words_dic = dict();
def load_pos_list(dfile):
	fp = open(dfile,'r');
	for line in fp.readlines():
		line = line.strip('\r').strip('\n');
		if len(line) == 0 or line[0] == '#': continue;
		sps = line.split('\t');
		if len(sps) <> 2: continue;
		pos_list[sps[1]] = sps[0];
	fp.close();

def load_files(dfile):
	fp = open(dfile,'r');
	for line in fp.readlines():
		line = line.strip('\r').strip('\n');
		if len(line) == 0 or line[0] == '#': continue;
		sps = line.split(' ');
		if len(sps) <= 2: continue;

		words = dict();
		plist = list();
		for i,s in enumerate(sps):
			if i == 0:
				words['words'] = s;
			elif len(s) > 0 and s[0] == '_':
				ts = s.replace('_','');
				if len(ts) == 0: continue;
				if not pos_list.has_key(ts):
					sys.stderr.write('the pos [' + sps[0] + '] type [' + ts + '] not found\n');
				else:
					plist.append(pos_list[ts]);
		if len(plist) > 0:
			words['pos'] = plist;
			words_dic[words['words']] = words;
	fp.close();

if ( __name__ == "__main__"):
	if len(sys.argv) <= 1:
		print 'Usage: %s poslist infile' %sys.argv[0];
		sys.exit(-1);
	load_pos_list(sys.argv[1]);

	load_files(sys.argv[2]);
	for word in words_dic.keys():
		witem = words_dic[word];
		print witem['words'],'|'.join(witem['pos']);
