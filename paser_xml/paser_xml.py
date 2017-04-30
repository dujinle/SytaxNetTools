#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys,xml.sax
reload(sys);
sys.setdefaultencoding('utf-8');
class W_T(xml.sax.ContentHandler):
	def __init__(self):
		self.tag = None;
		self.data = list();
		self.twp = list();
		self.twr = dict();
		self.ttype = dict();
		self.words = '';
		self.filter = False;

	def startElement(self, tag, attributes):
		if tag == 'w:t': self.tag = 'w_t';
		elif tag == 'w:r':
			self.tag = 'w_r';
			if attributes.has_key('w:rsidRPr'):
				self.twr['rsidRPr'] = attributes['w:rsidRPr'];
			else:
				self.twr['rsidRPr'] = 'null';
		elif tag == 'w:rPr' and self.tag == 'w_r': self.tag = 'w_rpr';
		elif tag == 'w:rFonts' and self.tag == 'w_rpr':
			if attributes.has_key('w:hint'):
				self.ttype['hint'] = attributes['w:hint'];
		elif tag == 'w:szCs' and self.tag == 'w_rpr':
			if attributes.has_key('w:val'):
				self.ttype['szcs'] = attributes['w:val'];
		elif tag == 'w:bdr' and self.tag == 'w_rpr':
			if attributes.has_key('w:val'):
				self.ttype['bdr'] = attributes['w:val'];
		elif tag == 'w:p': self.tag = 'w_p';
		elif tag == 'w:drawing' or tag == 'w:pict':
			self.filter = True;

	def endElement(self,tag):
		if tag == 'w:r':
			if self.twr.has_key('words'):
				self.twp.append(self.twr);
			self.twr = dict();
		elif tag == 'w:rPr':
			self.twr['type'] = self.ttype;
			self.ttype = dict();
		elif tag == 'w:t':
			self.twr['words'] = self.words;
			self.words = '';
		elif tag == 'w:p':
			if self.filter == False:
				self.data.append(self.twp);
			else:
				self.filter = False;
			self.twp = list();

	def characters(self, content):
		if not self.tag is None and self.tag == 'w_t':
			content = content.replace(u'【',' ');
			content = content.replace(u'】',' ');
			content = content.replace(u'①',' ');
			content = content.replace(u'②',' ');
			content = content.replace(u'③',' ');
			content = content.strip('\n').strip('\t').strip(' ');
			if len(content) > 0:
				self.words = self.words + content

if ( __name__ == "__main__"):
	if len(sys.argv) <= 1:
		print 'Usage: %s inxml' %sys.argv[0];
		sys.exit(-1);

	# 创建一个 XMLReader
	parser = xml.sax.make_parser()
	# turn off namepsaces
	parser.setFeature(xml.sax.handler.feature_namespaces, 0)

	# 重写 ContextHandler
	Handler = W_T()
	parser.setContentHandler( Handler )

	parser.parse(sys.argv[1]);
	for wp in Handler.data:
		for wr in wp:
			if wr.has_key('type') and wr['type'].has_key('bdr'):
				sys.stdout.write('_' + wr['words'] + ' ');
			else:
				sys.stdout.write(wr['words'] + ' ');
		sys.stdout.write('\n');
