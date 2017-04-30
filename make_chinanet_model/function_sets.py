#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,uuid,hashlib,json
reload(sys)
sys.setdefaultencoding('utf-8');
from net_data import NetData
import common

def _get_str_md5(strs):
	md5 = hashlib.md5();
	md5.update(strs);
	return md5.hexdigest();

def print_dic(tdic):
	mjson = json.dumps(tdic,indent = 4,ensure_ascii=False);
	print mjson;

def write_dic_file(tdic,tfile):
	fp = open(tfile,'w+');
	mjson = json.dumps(tdic,indent = 4,ensure_ascii=False);
	fp.write(mjson);
	fp.close();

def _creat_str_dic(strs,stype):
	tdic = dict();
	tdic['str'] = strs;
	tdic['stype'] = stype;
	return tdic;

def _creat_nouns_net_byline(tdic,line,stype):
	str_array = line.split('-');
	prev_itm = None;
	for tstr in str_array:
		citem = None;
		if prev_itm is None:
			t_array = tstr.split('/');
			citem = _creat_str_dic(t_array[0],t_array[1]);
		else:
			citem = _creat_str_dic(tstr,stype);
		if tdic.has_key(citem['str']):
			citem = tdic[citem['str']];
		else:
			tdic[citem['str']] = citem;

		if not prev_itm is None:
			if not prev_itm.has_key('pstr'):
				prev_itm['pstr'] = list();
			if not citem['str'] in prev_itm['pstr']:
				prev_itm['pstr'].append(citem['str']);
			if not citem.has_key('cstr'):
				citem['cstr'] = list();
			if not prev_itm['str'] in citem['cstr']:
				citem['cstr'].append(prev_itm['str']);
		prev_itm = citem;

def _creat_gerund_net_byline(tdic,noun_dic,line):
	str_array = line.split('-');
	prev_itm = None;
	for tstr in str_array:
		citem = None;
		if prev_itm is None:
			t_array = tstr.split('/');
			citem = _creat_str_dic(t_array[0],t_array[1]);
			tdic[citem['str']] = citem;
		else:
			citem = noun_dic.get(tstr,None);
			if citem is None:
				citem = _creat_str_dic(tstr,'NOUN');
				noun_dic[citem['str']] = citem;
		if not prev_itm is None:
			if not prev_itm.has_key('pstr'):
				prev_itm['pstr'] = list();
			if not citem['str'] in prev_itm['pstr']:
				prev_itm['pstr'].append(citem['str']);
			if not citem.has_key('cstr'):
				citem['cstr'] = list();
			if not prev_itm['str'] in citem['cstr']:
				citem['cstr'].append(prev_itm['str']);
		prev_itm = citem;

def link_words_gerund(words_dic,gerund_dic):
	for word in words_dic:
		for gerund in gerund_dic:
			gitem = gerund_dic[gerund];
			if gerund.find(word) <> -1:
				if gitem.has_key('rto'):
					if len(gitem['rto']) < len(word):
						gitem['rto'] = word;
				else:
					gitem['rto'] = word;
	for gerund in gerund_dic:
		gitem = gerund_dic[gerund];
		if gitem.has_key('rto'):
			witem = words_dic[gitem['rto']];
			if not witem.has_key('rto'):
				witem['rto'] = list();
			witem['rto'].append(gerund)
			del gitem['rto'];


def _load_nouns_net_file(tfile):
	fp = open(tfile,'r');
	lines = list();
	for line in fp.readlines():
		line = line.strip('\n').strip('\r');
		if line is None or len(line) == 0 or line[0] == '#': continue;
		lines.append(line);
	fp.close();
	return lines;
#print _get_str_md5(u'sss');

net_data = NetData();

noun_dic = net_data.get_noun_net();
lines = _load_nouns_net_file('./noun.txt');
for line in lines:
	_creat_nouns_net_byline(noun_dic,line,'NOUN');

gerund_dic = net_data.get_gerund_net();
lines = _load_nouns_net_file('./gerund.txt');
for line in lines:
	_creat_gerund_net_byline(gerund_dic,noun_dic,line);
#print_dic(gerund_dic);

verb_dic = net_data.get_verb_net();
lines = _load_nouns_net_file('./verb.txt');
for line in lines:
	_creat_nouns_net_byline(verb_dic,line,None);

link_words_gerund(verb_dic,gerund_dic);
link_words_gerund(noun_dic,gerund_dic);
common.write_dic_file(noun_dic,'./noun_dic.txt');
common.write_dic_file(verb_dic,'./verb_dic.txt');
common.write_dic_file(gerund_dic,'./gerund_dic.txt');
net_data.print_words();
#net_data.print_dot('net_data');

