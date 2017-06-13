#!/usr/bin/python
#-*- coding:utf-8 -*-

import collections,os,codecs,sys


sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
def _read_words(filename):
	with codecs.open(filename,'r','utf-8') as f:
		tdic = dict();
		while True:
			line = f.readline();
			if not line: break;
			line = line.strip('\n').strip('\r');
			if len(line) == 0 or line[0] == '#': continue;
			split = line.split('\t');
			keys = split[0].split(' ');
			values = split[1].split(' ');
			if len(keys) <> len(values):
				print ' '.join(keys),' '.join(values),'unmatch';
			for i,istr in enumerate(keys):
				if tdic.has_key(istr):
					if tdic[istr] <> values[i]:
						print istr,values[i],'unmatch';
				else:
					tdic[istr] = values[i];
		return tdic;


def djl_raw_data(data_path=None):
	train_path = os.path.join(data_path, "djl.train.txt")

	tdic = _read_words(train_path);
	for key in tdic.keys():
		print key,tdic[key];

if __name__ == '__main__':
	djl_raw_data('./data');
