#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys
import function_sets as FuncSet
from myexception import MyException

class MarkTag():
	def __init__(self,net_data):
		self.net_data = net_data;

	def encode(self,struct):
		try:
			self._mark_tag(struct);
			self._deal_time(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def _mark_tag(self,struct):
		noun_net = self.net_data.get_noun_net();
		verb_net = self.net_data.get_verb_net();
		gerund_net = self.net_data.get_gerund_net();
		if not struct.has_key('sp_sentence'): return None;
		for words in struct['sp_sentence']:
			if noun_net.has_key(words):
				struct['tag_dict'][words] = noun_net[words];
			elif verb_net.has_key(words):
				struct['tag_dict'][words] = verb_net[words];
			elif gerund_net.has_key(words):
				struct['tag_dict'][words] = gerund_net[words];
			else:
				pass;

	def _deal_time(self,struct):
		if struct.has_key('intervals') and len(struct['intervals']) > 0:
			inters = struct['intervals'];
			for ints in inters:
				mtime = dict(struct['intervals'][0]);
				twords = ints['str'].replace('_','');
				struct['tag_dict'][twords] = mtime;
				del struct['intervals'][0];
		if struct.has_key('intervals'): del struct['intervals'];

	def _print_words(self):
		noun_net = self.net_data.get_noun_net();
		verb_net = self.net_data.get_verb_net();
		gerund_net = self.net_data.get_gerund_net();
		for tstr in noun_net:
			print tstr;
		for tstr in verb_net:
			print tstr;
		for tstr in gerund_net:
			print tstr;
