#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,re,common
from myexception import MyException

#mark time mood ,time status
class MarkTMood():
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
			self._mark_tmood_tag(struct);
		except Exception as e:
			raise MyException(sys.exc_info());

	def _mark_tmood_tag(self,struct):
		for tag in struct['sp_sentence']:
			tdic = self._mark_words(tag);
			if not tdic is None:
				struct['tag_list'][tag] = tdic;

	def _mark_words(self,tstr):
		for key in self.data.keys():
			item = self.data[key];
			for nk in item.keys():
				nitem = item[nk];
				if tstr in nitem:
					tdic = dict();
					tdic['type'] = 'TMOOD';
					tdic['stype'] = nk;
					tdic['str'] = tstr;
					return tdic;
		return None;

	def _print_words(self):
		for key in self.data.keys():
			item = self.data[key];
			for nk in item.keys():
				nitem = item[nk];
				for nnk in nitem: print nnk;
