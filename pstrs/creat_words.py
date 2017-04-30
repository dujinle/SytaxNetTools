#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys
reload(sys)
sys.setdefaultencoding('utf-8');

base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../commons'));
sys.path.append(os.path.join(base_path,'../reg_graph'));
from net_data import NetData
from mark_tag import MarkTag
from mark_tmood import MarkTMood
from mark_unit import MarkUnit
from merge_prep import MergePrep
from merge_verb import MergeVerb
import common

net_data = NetData();
net_data.set_noun_net(os.path.join(base_path,'../tdata/noun_dic.data'));
net_data.set_verb_net(os.path.join(base_path,'../tdata/verb_dic.data'));
net_data.set_gerund_net(os.path.join(base_path,'../tdata/gerund_dic.data'));

mark_tag = MarkTag(net_data);
mark_unit = MarkUnit(net_data);
mark_tmood = MarkTMood(net_data);
merge_prep = MergePrep(net_data);
merge_verb = MergeVerb(net_data);

merge_prep.load_data('../tdata/calc_prep.txt');
merge_verb.load_data('../tdata/calc_verb.txt');
mark_unit.load_data('../tdata/unit.txt');
mark_tmood.load_data('../tdata/time_mood.txt');

mark_tag._print_words();
mark_unit._print_words();
merge_prep._print_words();
merge_verb._print_words();
mark_tmood._print_words();
