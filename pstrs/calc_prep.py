#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,re,common
import reg_to_words as Reg2Words
import function_sets as FuncSet
from myexception import MyException

class CalcPrep():
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
			self._match_prep(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def _match_prep(self,struct):
		for idx,words in enumerate(struct['sp_sentence']):
			for ktype in self.data:
				for item in self.data[ktype]:
					comp = re.compile(item['reg']);
					match = comp.match(words);
					if match is None: continue;
					self._match_rule(item,idx,struct);

	def _match_rule(self,item,idx,struct):
		plist = pword = reg_str = None;
		dlist = list();
		#Scan the back of the words_list
		if item['pos'] == 'prev':
			if idx >= len(struct['sp_sentence']) - 1: return False;
			cword = struct['sp_sentence'][idx];
			idx = idx + 1;
			pword = struct['sp_sentence'][idx];
			while True:
				idx = idx + 1;
				if idx >= len(struct['sp_sentence']): break;
				if struct['tag_dict'].has_key(pword): break;
				pword = pword + struct['sp_sentence'][idx];
			plist = [cword,pword];
			if not struct['tag_dict'].has_key(pword): return False;
			pitem = struct['tag_dict'][pword];
			if pitem.has_key('stype'): reg_str = cword + pitem['stype'];
		#Scan the opposite side
		elif item['pos'] == 'after':
			if idx <= 0: return False;
			pword = struct['sp_sentence'][idx];
			idx = idx - 1;
			cword = struct['sp_sentence'][idx];
			while True:
				idx = idx - 1;
				if idx < 0: break;
				if struct['tag_dict'].has_key(cword): break;
				cword = struct['sp_sentence'][idx] + cword;
			plist = [cword,pword];
			if not struct['tag_dict'].has_key(cword): return False;
			citem = struct['tag_dict'][cword];
			if citem.has_key('stype'): reg_str = citem['stype'] + pword;
		xx_str = item['calc_reg'].replace('KEY',item['reg']);
		comp = re.compile(xx_str);
		if reg_str is None or comp.search(reg_str) is None: return False;

		for istr in plist:
			if not struct['tag_dict'].has_key(istr):
				item = FuncSet._creat_str_dic(istr,'prep');
				dlist.append(item);
			else:
				dlist.append(struct['tag_dict'][istr]);
				del struct['tag_dict'][istr];
		struct['tag_dict'][''.join(plist)] = dlist;

	def _print_words(self):
		for ktype in self.data:
			for item in self.data[ktype]:
				reg_str = item['reg'];
				Reg2Words.reg_to_words(reg_str);

