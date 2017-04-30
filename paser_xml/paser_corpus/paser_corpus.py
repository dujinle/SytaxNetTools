#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys,xml.sax,json
reload(sys);
sys.setdefaultencoding('utf-8');

def print_dic(struct):
	value = json.dumps(struct,indent = 4,ensure_ascii=False);
	print value;

class XmlHandler(xml.sax.ContentHandler):
	def __init__(self):
		self.data = dict();
		self.cels = ['0','0','0','0','0','0','0','0','0','0','0','0','0'];
		self.cur_idx = self.lines = 0;
		self.cur_dic = dict();
		self.paser_flg = False;
		self.data_flg = False;

	def _fetch_row(self):
		cur_list = self.cur_dic.keys();
		tdic = cur_dic = dict();
		idx = 0;
		while True:
			if idx >= len(cur_list): break;
			iit = cur_list[idx];
			isr = self.cur_dic[iit];
			if idx == 0:
				tdic = cur_dic;
				tdic[isr] = dict();
				tdic[isr]['idx'] = iit;
			elif idx < len(cur_list) - 1:
				key = self.cur_dic[cur_list[idx - 1]];
				tdic = tdic[key];
				tdic[isr] = dict();
				tdic[isr]['idx'] = iit;
			if idx == len(cur_list) - 1:
				key = self.cur_dic[cur_list[idx - 1]];
				tdic[key]['str'] = isr;
			idx = idx + 1;
		return cur_dic;

	def _add_to_dic(self,cur_dic):

		tdic = cur_dic;
		mydata = self.data;
		while True:
			keys = tdic.keys();
			if len(keys) <= 0: break;
			key = keys[0];
			tdic = tdic[key];
			if mydata.has_key(key):
				mydata = mydata[key];
			else:
				mydata[key] = dict(tdic);
				break;


	def startElement(self, tag, attributes):
		if tag == 'Cell' and attributes.has_key('ss:Index'):
			self.paser_flg = True;

		if tag == 'Cell' and self.paser_flg:
			if not attributes.has_key('ss:Index'):
				self.cur_idx = self.cur_idx + 1;
			else:
				self.cur_idx = int(attributes['ss:Index']);
		if self.paser_flg and tag == 'Data':
			self.data_flg = True;

	def endElement(self,tag):
		if tag == 'Row' and self.paser_flg:
			self.paser_flg = False;
			cur_dic = self._fetch_row();
#			print_dic(cur_dic);
			self._add_to_dic(cur_dic);
			if self.lines >= 10:
				print_dic(self.data);
				sys.exit(0);
			self.lines = self.lines + 1;
		if tag == 'Data' and self.paser_flg:
			self.cur_dic[self.cur_idx] = self.cels[self.cur_idx];

	def characters(self, content):
		if self.data_flg:
			self.cels[self.cur_idx] = content;
			self.data_flg = False;

if __name__ == "__main__":
	if len(sys.argv) <= 1:
		print 'Usage: %s inxml' %sys.argv[0];
		sys.exit(-1);

	# 创建一个 XMLReader
	parser = xml.sax.make_parser();
	# turn off namepsaces
	parser.setFeature(xml.sax.handler.feature_namespaces, 0);

	# 重写 ContextHandler
	Handler = XmlHandler();
	parser.setContentHandler(Handler);

	parser.parse(sys.argv[1]);
