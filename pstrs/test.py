#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys
reload(sys)
sys.setdefaultencoding('utf-8');

base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../commons'));
sys.path.append(os.path.join(base_path,'../wordsegs'));
sys.path.append(os.path.join(base_path,'../reg_graph'));
sys.path.append(os.path.join(base_path,'../timer'));
import common
from time_mager import TimeMager
from word_seg import WordSeg

from net_data import NetData
from mark_tag import MarkTag
from mark_num import MarkNum
from mark_unit import MarkUnit
from mark_tmood import MarkTMood

from merge_obj import MergeObj

from calc_verb import CalcVerb
from calc_prep import CalcPrep
from calc_num_unit import CalcNumUnit
from calc_sds import CalcSDS

word_seg = WordSeg();
timer = TimeMager(word_seg);
net_data = NetData();
net_data.set_noun_net(os.path.join(base_path,'../tdata/noun_dic.data'));
net_data.set_verb_net(os.path.join(base_path,'../tdata/verb_dic.data'));
net_data.set_gerund_net(os.path.join(base_path,'../tdata/gerund_dic.data'));
#net_data.print_dot('net_data');
timer.init('Timer');
struct = dict();

mark_tag = MarkTag(net_data);
mark_num = MarkNum(net_data);
mark_unit = MarkUnit(net_data);
mark_tmood = MarkTMood(net_data);
merge_obj = MergeObj(net_data);

calc_prep = CalcPrep(net_data);
calc_verb = CalcVerb(net_data);
calc_nunit = CalcNumUnit(net_data);
calc_sds = CalcSDS(net_data);

mark_unit.load_data('../tdata/unit.txt');
mark_num.load_data('../tdata/num.txt');
mark_tmood.load_data('../tdata/time_mood.txt');

calc_prep.load_data('../tdata/calc_prep.txt');
calc_verb.load_data('../tdata/calc_verb.txt');

fp = open('./test.txt','rb');
for line in fp.readlines():
	line = line.strip('\n');
	if line[0] == '#' or len(line) == 0: continue;
	struct['text'] = line.decode('utf-8');
	struct['tag_dict'] = dict();
	timer.encode(struct);
	struct['sp_sentence'] = word_seg.tokens(struct['text']);
	mark_tag.encode(struct);
	mark_num.encode(struct);
	mark_unit.encode(struct);
	mark_tmood.encode(struct);
	merge_obj.encode(struct);

	calc_prep.encode(struct);
	calc_verb.encode(struct);
	calc_nunit.encode(struct);
	calc_sds.encode(struct);
	common.print_dic(struct);
	break;

