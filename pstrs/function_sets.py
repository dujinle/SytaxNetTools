#!/usr/bin/python
#-*- coding:utf-8 -*-
import uuid,hashlib,json
from net_data import NetData

def _get_str_uid(strs,namespace = None):
	if namespace is None:
		return str(uuid.uuid3(uuid.NAMESPACE_DNS,strs));
	else:
		return str(uuid.uuid3(namespace,strs));

def _get_str_md5(strs):
	md5 = hashlib.md5();
	md5.update(strs);
	return md5.hexdigest();

def _creat_str_dic(strs,stype):
	tdic = dict();
	tdic['str'] = strs;
	tdic['stype'] = stype;
	return tdic;
