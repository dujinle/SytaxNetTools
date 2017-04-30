#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
import function_sets as FuncSet
from myexception import MyException

class MergeObj():
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
			self._merge_same_wtype(struct);
			self._move_other_item(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def _merge_same_wtype(self,struct):
		prev = same = None;
		for idx,words in enumerate(struct['sp_sentence']):
			if not prev is None and struct['tag_dict'].has_key(words)\
				and struct['tag_dict'].has_key(prev):

				cur = struct['tag_dict'][words];
				pitem = struct['tag_dict'][prev];
				if pitem.has_key('stype') and cur.has_key('stype'):
					if cur['stype'] == 'UNIT' or cur['stype'] == 'VERB':
						prev = words;
						continue;
					if pitem['stype'] == cur['stype']:
						same = [pitem,cur];
					elif not same is None:
						self._add_same(pitem['stype'],same,struct);
						same = None;
			elif not same is None:
				self._add_same(pitem['stype'],same,struct);
				same = None;
			prev = words;

	def _add_same(self,stype,same,struct):
		kstr = '';
		for item in same:
			kstr = kstr + item['str'];
			if struct['tag_dict'].has_key(item['str']):
				del struct['tag_dict'][item['str']];
		struct['tag_dict'][kstr] = dict();
		struct['tag_dict'][kstr]['objs']= same;
		struct['tag_dict'][kstr]['stype'] = stype;

	def _move_other_item(self,struct):
		remove = list();
		for key in struct['tag_dict']:
			if len(key) > 1:
				for istr in key:
					if struct['tag_dict'].has_key(istr):
						remove.append(istr);
		for ri in remove:
			del struct['tag_dict'][ri];
