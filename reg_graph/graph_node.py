#!/usr/bin/python
#-*- coding:utf-8 -*-

class GraphNode():
	static_id = 0;
	def __init__(self):
		self.nid = GraphNode.static_id;
		GraphNode.static_id = GraphNode.static_id + 1;
		self.edge_list = list();

	def get_nid(self): return self.nid;
	def has_edge(self): return len(self.edge_list) > 0;
