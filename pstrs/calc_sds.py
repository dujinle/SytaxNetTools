#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,re,common
import reg_to_words as Reg2Words
import function_sets as FuncSet
from myexception import MyException

class CalcSDS():
	def __init__(self,net_data):
		self.net_data = net_data;
		self.data = dict();
		self.idx = 0;
		self.vdict = {'SB':0,'VERB':1,'STH':2};

	def load_data(self,dfile):
		try:
			if dfile is None: raise Exception('dfile is none');
			self.data = common.read_json(dfile);
		except Exception:
			raise MyException(sys.exc_info());

	def encode(self,struct):
		try:
			self._calc_sds(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def _calc_sds(self,struct):
		pstr = '';
		plist = list();
		for istr in struct['sp_sentence']:
			pstr = pstr + istr;
			if not struct['tag_dict'].has_key(pstr):
				continue;
			else:
				pitem = struct['tag_dict'][pstr];
				if not pitem.has_key('stype'): continue;
				if self.vdict.has_key(pitem['stype']):
					pidx = self.vdict[pitem['stype']];
					plist.append(pstr);
					if pidx == 2 and self.idx == 1 and len(plist) > 1:
						self._add_sds(struct,plist);
						plist = list();
						self.idx = 0;
					elif pidx == 1 and self.idx == 0 and len(plist) > 1:
						self._add_sds(struct,plist);
						plist = list();
						self.idx = 0;
					self.idx = pidx;
				else:
					plist = list();
				pstr = '';

	def _add_sds(self,struct,plist):
		key = '';
		tlist = list();
		for item in plist:
			key = key + item;
			tlist.append(struct['tag_dict'][item]);
			del struct['tag_dict'][item];
		tdic = dict();
		tdic['stc'] = tlist;
		tdic['stype'] = 'SDS';
		struct['tag_dict'][key] = tdic;

	def _print_words(self): pass;

