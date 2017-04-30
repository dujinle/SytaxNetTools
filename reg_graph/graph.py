#!/usr/bin/python
#-*- coding:utf-8 -*-

class Graph():
	def __init__(self):
		self.start = self.end = 0;
		self.nodes = dict();

	def add_edge(self,n1,n2,char):
		edge_info = dict();
		edge_info['to'] = n2.nid;
		edge_info['str'] = char;
		n1.edge_list.append(edge_info);
		self.nodes[n1.nid] = n1;
		self.nodes[n2.nid] = n2;

	def print_dot(self,name):
		print 'digraph ' + name + ' {';
		print '\tnode[fontname=FangSong]';
		for nid in self.nodes:
			node = self.nodes[nid];
			for edge in node.edge_list:
				print '\t' + str(nid) + '->' + str(edge['to']) + '[label=' + edge['str'] + ']';
		print '}';

	def print_path(self):
		mydic = dict();
		mydic['id'] = self.start;
		mydic['str'] = '';
		mydic['nids'] = list();
		vector = list();
		vector.append(mydic);
		while len(vector) > 0:
			mdic = vector[-1];
			del vector[-1];
			node = self.nodes[mdic['id']];
			for edge in node.edge_list:
				mydic = dict();
				mydic['id'] = edge['to'];
				mydic['nids'] = list(mdic['nids']);
				mydic['nids'].append(mdic['id']);
				if edge['to'] in mdic['nids']:
					if edge['str'] == 'E': continue;
				if edge['str'] <> 'E':
					mydic['str'] = mdic['str'] + edge['str'];
				else:
					mydic['str'] = mdic['str'];
				vector.append(mydic);
			if mdic['id'] == self.end:
				print mdic['str'];

