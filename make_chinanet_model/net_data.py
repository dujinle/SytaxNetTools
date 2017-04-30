#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,json
import common
from myexception import MyException

#story all the data net info
class NetData():
	def __init__(self):
		self.noun_net = dict();
		self.verb_net = dict();
		self.gerund_net = dict();
		pass;
	def get_noun_net(self): return self.noun_net;

	def get_verb_net(self): return self.verb_net;

	def get_gerund_net(self): return self.gerund_net;

	def set_noun_net(self,dfile):
		djson = common.read_json(dfile);
		self.noun_net.update(djson);
	def set_verb_net(self,dfile):
		djson = common.read_json(dfile);
		self.verb_net.update(djson);
	def set_gerund_net(self,dfile):
		djson = common.read_json(dfile);
		self.gerund_net.update(djson);

	def print_dot(self,name):
		def _dot_format(item):
			strs = item['str'] + ':' + item['stype'];
			return strs;
		def _get_net_item(tdic):
			for t in tdic:
				item = tdic[t];
				if item.has_key('pstr'):
					for pid in item['pstr']:
						pitem = tdic[pid];
						print '\t\"' + _dot_format(item) + '\"->\"' + _dot_format(pitem) + '\"[label=parent]';
				if item.has_key('rto'):
					for rid in item['rto']:
						ritem = self.gerund_net[rid];
						print '\t\"' + _dot_format(item) + '\"->\"' + _dot_format(ritem) + '\"[label=relate]';
				print '\t\"' + _dot_format(item) + '\"';

		def _get_gr_net_item(tdic):
			for t in tdic:
				item = tdic[t];
				if item.has_key('pstr'):
					for pid in item['pstr']:
						pitem = self.noun_net[pid];
						print '\t\"' + _dot_format(item) + '\"->\"' + _dot_format(pitem) + '\"[label=parent]';
				print '\t\"' + _dot_format(item) + '\"';
		print 'digraph ' + name + ' {';
		print '\tnode[fontname=FangSong]';
		_get_net_item(self.noun_net);
		_get_net_item(self.verb_net);
		_get_gr_net_item(self.gerund_net);
		print '}'

	def print_words(self):
		for tstr in self.noun_net:
			print tstr;
		for tstr in self.verb_net:
			print tstr;
		for tstr in self.gerund_net:
			print tstr;
		

