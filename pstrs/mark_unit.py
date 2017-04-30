#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys
import function_sets as FuncSet
from myexception import MyException
import common
class MarkUnit():
	def __init__(self,net_data):
		self.net_data = net_data;
		self.data = dict();

	def load_data(self,dfile):
		try:
			self.data = common.readfile(dfile);
		except Exception:
			raise MyException(sys.exc_info());

	def encode(self,struct):
		try:
			self._mark_unit(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def _mark_unit(self,struct):
		for words in struct['sp_sentence']:
			if self.data.has_key(words):
				tdic = dict();
				tdic['stype'] = 'UNIT';
				tdic['str'] = words;
				struct['tag_dict'][words] = tdic;

	def _print_words(self):
		for key in self.data:
			if len(key) > 1: print key;

