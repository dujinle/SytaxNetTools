#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,re,common
import reg_to_words as Reg2Words
import function_sets as FuncSet
from myexception import MyException

class CalcNumUnit():
	def __init__(self,net_data):
		self.net_data = net_data;
		self.data = dict();

	def load_data(self,dfile):
		try:
			if dfile is None: raise Exception('dfile is none');
			self.data = common.read_json(dfile);
		except Exception:
			raise MyException(sys.exc_info());

	def encode(self,struct):
		try:
			self._calc_num_unit(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def _calc_num_unit(self,struct):
		nlist = list();
		ulist = list();
		for key in struct['tag_dict']:
			item = struct['tag_dict'];
			if item.has_key('stype'):
				if item['stype'] == 'NUM':
					nlist.append(item);
				elif item['stype'] == 'UNIT':
					ulist.append(item);
		for num in nlist:
			for unit in ulist:
				ustr = num['str'] + unit['str'];
				if struct['text'].find(ustr) <> -1:
					tdic = dict();
					tdic['type'] = 'NUNIT';
					tdic['stc'] = list();
					tdic['stc'].append(num);
					tdic['stc'].append(unit);
					struct['tag_dict'][ustr] = tdic;

	def _print_words(self): pass;
