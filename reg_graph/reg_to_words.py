#!/usr/bin/python
#-*- coding:utf-8 -*-
from graph import Graph
from graph_node import GraphNode
from trans_model import TransModel
tm = TransModel();
def reg_to_words(reg_str):
	tm.creat_graph(reg_str);
	tm.graph.print_path();
