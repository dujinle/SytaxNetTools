#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
import function_sets as FuncSet
from myexception import MyException

class MarkNum():
	def __init__(self,net_data):
		self.net_data = net_data;
		self.data = dict();

	def load_data(self,dfile):
		try:
			self.data = common.read_json(dfile);
		except Exception:
			raise MyException(sys.exc_info());

	def encode(self,struct):
		try:
			self._mark_num(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def _mark_num(self,struct):
		for words in struct['sp_sentence']:
			match = self._match_num_reg(words);
			if not match is None:
				tdic = dict();
				tdic['stype'] = 'NUM';
				tdic['str'] = words;
				struct['tag_dict'][words] = tdic;

	def _match_num_reg(self,words):
		for key in self.data:
			idata = self.data[key];
			comp = re.compile(idata);
			match = comp.match(words);
			if not match is None: return match;
		return None;

	def _print_words(self): pass;
