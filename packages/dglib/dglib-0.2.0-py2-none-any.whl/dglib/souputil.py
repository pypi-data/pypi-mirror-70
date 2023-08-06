# -*- coding: gbk -*-
from __future__ import unicode_literals

import demjson
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
from dglib.utils import decode_json, dget


def fix_url(url):
	if url:
		if url.startswith('//'):
			url = 'http:' + url
		if not url.startswith('http'):
			url = 'http://' + url
	return url


def get_html_encoding(html):
	return EncodingDetector.find_declared_encoding(html, is_html=True, search_entire_document=False)


def to_unicode_html(html, encoding=None, default_encoding='gbk'):
	if not isinstance(html, unicode):
		if not encoding:
			encoding = get_html_encoding(html) or default_encoding
		html = html.decode(encoding, errors='replace')
	return html


def make_soup(html):
	# BeautifulSoup�ڲ�ʹ��lxml�����html��ʱ���ڽ�strת��Ϊunicode��ʱ����ʱ��������⡣
	# Ҳ������ȫת��ʧ�ܣ����ǿ��ܻᶪʧ���е�һЩ���䡣������תΪunicode���ٴ���BeautifulSoup��
	# BeautifulSoup 4.4.1, lxml 3.6.0
	html = to_unicode_html(html)
	return html, BeautifulSoup(html, 'lxml')


def soup_text(soup_obj, selector=None, default='', encoding=None):
	result = default
	if selector is not None:
		soup_obj = soup_obj.select(selector)[0]
	if soup_obj:
		s = soup_obj.string	# NavigableString���޷�pickle���ʺ���ͳһת��Ϊunicode��
		if s is None:
			strings = list(soup_obj.strings)
			if strings:
				s = strings[0]
		if s is not None:
			if encoding:
				result = unicode(s, encoding)
			else:
				result = unicode(s)
	return result


def success_json(html):
	if html:
		html = html.strip()
		try:
			html = html.decode('gbk')
		except UnicodeDecodeError:
			import time
			open('UnicodeDecodeError_%s.html' % int(time.time()), 'w').write(html)
			return None
		if html.endswith(')') or html.endswith(');'):
			p = html.find('(')
			q = html.rfind(')')
			if p != -1 and q != -1:
				html = html[p + 1:q]
		d = decode_json(html)
		if d is None:
			try:
				# ����js�г����Ĳ������ŵ�key��json
				d = demjson.decode(html)
			except:
				pass
		if d:
			succ = d.get('success')
			if succ is True:
				return d
			code = dget(d, 'code/code')
			if code == 0:
				return d
			# �е���û��success�ֶλ�code�ֶεģ�ֻ�����ݣ�������Ҳ��ɹ���
			if succ is None and code is None:
				return d
