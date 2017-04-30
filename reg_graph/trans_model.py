#!/usr/bin/python
#-*- coding:utf-8 -*-
from graph import Graph
from graph_node import GraphNode

class TransModel():
	def __init__(self):
		self.op_list = list();
		self.graph = Graph();
		self.ht_list = list();
		self.reg_str = None;

	def creat_graph(self,reg_str):
		self.reg_str = reg_str;
		slen = len(reg_str);
		for i,s in enumerate(reg_str):
			if self.is_operator(s) == False:
				n1 = GraphNode();
				n2 = GraphNode();
				self.base_operator(n1,n2,s);
				if (i + 1 < slen) and (self.is_operator(reg_str[i + 1]) == False or reg_str[i + 1] == '('):
					self.op_list.append('&');
			else:
				if s == '(': self.op_list.append(s);
				elif s == '|': self.op_list.append(s);
				elif s == '+':
					if len(self.ht_list) == 0: return None;
					g1 = self.ht_list[-1];
					del self.ht_list[-1];
					self.plus_operator(g1);
					if (i + 1 < slen) and (self.is_operator(reg_str[i + 1]) == False or reg_str[i + 1] == '('):
						self.op_list.append('&');
				elif s == ')':
					if len(self.ht_list) == 0: return None;
					self.bracket_operator();
					if (i + 1 < slen) and (self.is_operator(reg_str[i + 1]) == False or reg_str[i + 1] == '('):
						self.op_list.append('&');
				elif s == '*':
					if len(self.ht_list) == 0: return None;
					g1 = self.ht_list[-1];
					del self.ht_list[-1];
					self.asterisk_operator(g1);
		while len(self.op_list) > 0:
			op = self.op_list[-1];
			del self.op_list[-1];
			g2 = dict(self.ht_list[-1]);
			del self.ht_list[-1];
			g1 = dict(self.ht_list[-1]);
			del self.ht_list[-1];
			if op == '&':
				self.combine_opreator(g1,g2);
			elif op == '|':
				self.or_operator(g1,g2);

	#calc ) operator
	def bracket_operator(self):
		op = self.op_list[-1];
		del self.op_list[-1];
		while op <> '(':
			g2 = dict(self.ht_list[-1]);
			del self.ht_list[-1];
			g1 = dict(self.ht_list[-1]);
			del self.ht_list[-1];
			if op == '&':
				self.combine_opreator(g1,g2);
			elif op == '|':
				self.or_operator(g1,g2);
			op = self.op_list[-1];
			del self.op_list[-1];

	#calc * operator
	def asterisk_operator(self,g1):
		n1 = self.graph.nodes[g1['start']];
		n2 = self.graph.nodes[g1['end']];
		n3 = GraphNode();
		self.graph.add_edge(n2,n1,'E');
		self.graph.add_edge(n1,n3,'E');
		self.graph.add_edge(n2,n3,'E');
		head_tail = dict();
		head_tail['start'] = n1.nid;
		head_tail['end'] = n3.nid;
		self.graph.start = n1.nid;
		self.graph.end = n3.nid;
		self.ht_list.append(head_tail);

	#calc + operator
	def plus_operator(self,g1):
		n1 = self.graph.nodes[g1['start']];
		n2 = self.graph.nodes[g1['end']];
		n3 = GraphNode();
		self.graph.add_edge(n2,n1,'E');
		self.graph.add_edge(n2,n3,'E');
		head_tail = dict();
		head_tail['start'] = n1.nid;
		head_tail['end'] = n3.nid;
		self.graph.start = n1.nid;
		self.graph.end = n2.nid;
		self.ht_list.append(head_tail);

	#calc | operator
	def or_operator(self,g1,g2):
		g11 = self.graph.nodes[g1['start']];
		g12 = self.graph.nodes[g1['end']];
		g21 = self.graph.nodes[g2['start']];
		g22 = self.graph.nodes[g2['end']];
		g3 = GraphNode();
		g4 = GraphNode();
		self.graph.add_edge(g3,g11,'E');
		self.graph.add_edge(g3,g21,'E');
		self.graph.add_edge(g12,g4,'E');
		self.graph.add_edge(g22,g4,'E');
		head_tail = dict();
		self.graph.start = g3.nid;
		self.graph.end = g4.nid;
		head_tail['start'] = g3.nid;
		head_tail['end'] = g4.nid;
		self.ht_list.append(head_tail);

	def is_operator(self,char):
		if char == ')' or char == '(': return True;
		if char == '+' or char == '*': return True;
		if char == '|': return True;
		return False;

	def base_operator(self,n1,n2,char):
		head_tail = dict();
		head_tail['start'] = n1.nid;
		head_tail['end'] = n2.nid;
		self.graph.start = n1.nid;
		self.graph.end = n2.nid;
		self.graph.add_edge(n1,n2,char);
		self.ht_list.append(head_tail);

	def combine_opreator(self,g1,g2):
		g11 = self.graph.nodes[g1['start']];
		g12 = self.graph.nodes[g1['end']];
		g21 = self.graph.nodes[g2['start']];
		g22 = self.graph.nodes[g2['end']];
		self.graph.add_edge(g12,g21,'E');
		self.graph.start = g11.nid;
		self.graph.end = g22.nid;
		head_tail = dict();
		head_tail['start'] = g11.nid;
		head_tail['end'] = g22.nid;
		self.ht_list.append(head_tail);
