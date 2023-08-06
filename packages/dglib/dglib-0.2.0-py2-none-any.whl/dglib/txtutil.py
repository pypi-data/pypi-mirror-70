# -*- coding: gbk -*-
import os
import codecs
import __builtin__
from bs4 import UnicodeDammit


def get_fileencoding(filename, default=None, detail=None):
	encoding = default
	skip_bytes = 0
	if os.path.isfile(filename):
		f = __builtin__.open(filename, "rb")
		try:
			s = f.read(2)
			"""
			ANSI��				�޸�ʽ���壻
			Unicode��			ǰ�����ֽ�ΪFFFE��
			Unicode big endian��	ǰ���ֽ�ΪFEFF��
			UTF-8 with BOM��		ǰ���ֽ�ΪEFBBBF��
			"""
			if s == chr(0xff) + chr(0xfe):
				encoding = "utf_16_le"
				skip_bytes = 2
			elif s == chr(0xfe) + chr(0xff):
				encoding = "utf_16_be"
				skip_bytes = 2
			elif s == chr(0xef) + chr(0xbb):
				encoding = "utf-8-sig"
				skip_bytes = 3
		except:
			pass
		if not encoding:
			# ʹ��BeautifulSoup�ı���ʶ����
			f.seek(0)
			line = f.readline()
			dammit = UnicodeDammit(line)
			# ע�⣬���ַ�����ʱ��ȡ���ı�����'windows-1252'�������ַ�����һ�֣���������ɿ���
			encoding = dammit.original_encoding
		f.close()
	if isinstance(detail, dict):
		detail["encoding"] = encoding
		detail["skip_bytes"] = skip_bytes
	return encoding


def open(filename, mode="r", encoding=None, skip_bytes=0):
	detail = {}
	if encoding is None:
		encoding = get_fileencoding(filename, detail=detail)
	if encoding is None:
		encoding = "gb18030"
	if not skip_bytes:
		skip_bytes = detail.get("skip_bytes", skip_bytes)

	# ע�⣺codecs.open �����Ƿ�ָ����mode�������Զ�����ģʽ�򿪡�
	# �����Ҫ���д����ı��ļ��е�\r\n -> \n
	f = codecs.open(filename, mode=mode, encoding=encoding)
	f.seek(skip_bytes)	# ����ָʾͷ
	# ע�⣺f.read()���ص���unicode
	return f


def readfile(filename, encoding="gbk"):
	with open(filename) as f:
		content = f.read()
		content = content.replace(u"\r\n", u"\n")
		if encoding:
			content = content.encode(encoding)
	return content


if __name__ == "__main__":
	print readfile("1.txt")
