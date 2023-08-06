# -*- coding: gbk -*-
import sys
import os
import re
import glob
import codecs
import datetime
import threading
import time
import logging.handlers

from .utils import module_path, extractbaseext, isoformat_date, makesure_dirpathexists, SYS_ENCODING

__all__ = ["BlackHole", "CompositeFile", "ScreenLogger", "StreamToLogger", "NoneTracer", "Tracer", "Tracer2", "MyStreamHandler",
		"DailyRotatingFileHandler", "Utf8DailyRotatingFileHandler", "UdpLogHandler", "get_logger", "get_logger2", "std_formatter",
		"get_tracer", "get_nonetracer", "get_classtracer", "get_filetracer", "redirect_stdout_stderr_tologger", "nullfile"]


class BlackHole(object):
	softspace = 0

	def write(self, text):
		pass

	def flush(self):
		pass


class CompositeFile(object):
	"""
	�����ļ����󣬿�ͨ��add()�����������ļ�����һ�������
	�磺.add(sys.sysout)
	"""
	def __init__(self, filename="", mode="w", encoding="", nocache=False):
		self.files = []
		self.encoding = encoding
		if filename:
			if encoding:
				codecs.open(filename, mode, encoding)
			else:
				f = open(filename, mode)
			self.files.append(f)
		self.nocache = nocache

	def add(self, f):
		if f not in self.files:
			self.files.append(f)

	def remove(self, f):
		if f in self.files:
			self.files.remove(f)

	def write(self, text):
		for f in self.files:
			unicode_safe_write(f, text, self.encoding)
		if self.nocache:
			self.flush()

	def flush(self):
		for f in self.files:
			if hasattr(f, 'flush'):
				f.flush()

	def close(self):
		for f in self.files:
			f.close()


class SafeOutStream(object):
	def __init__(self, underlying_stream, encoding=None, errors='replace'):
		self.underlying_stream = underlying_stream
		self.encoding = encoding
		self.errors = errors

	def write(self, s):
		if isinstance(s, unicode):
			s = s.encode(self.encoding, errors=self.errors)
		self.underlying_stream.write(s)

	def flush(self):
		self.underlying_stream.flush()


class ScreenLogger(object):
	"""
	�ɽ���Ļ���������ͬʱ���浽һ����־�ļ���
	�÷���
	sys.stdout = sys.stderr = ScreenLogger("��־�ļ���")
	"""
	def __init__(self, filename="", encoding=None, append=False, showtime=False, logfile=None):
		self.filename = filename
		self.append = append
		self.showtime = showtime
		self.logfile = logfile
		self.lastlogtime = 0
		self.encoding = encoding
		self.stdout = sys.__stdout__

	def create_file(self, filename, append):
		if append and os.path.exists(filename):
			logfile = codecs.open(filename, "a", self.encoding)
		else:
			makesure_dirpathexists(filename)
			logfile = codecs.open(filename, "w", self.encoding)
		return logfile

	def write(self, s):
		if self.showtime:
			now = int(time.time())
			if self.lastlogtime != now:
				self.lastlogtime = now
				s = "\n".join([time.strftime("\n%Y-%m-%d %H:%M:%S"), s])

		ascii = unicode_safe_write(self.stdout, s)
		if not self.logfile and self.filename:
			try:
				self.logfile = self.create_file(self.filename, self.append)
			except:
				pass
		if self.logfile:
			try:
				unicode_safe_write(self.logfile, s, safe_stuff=ascii)
				self.logfile.flush()
			except:
				pass

	def flush(self):
		self.stdout.flush()
		if self.logfile:
			try:
				self.logfile.flush()
			except:
				pass


class StreamToLogger(object):
	"""
	Fake file-like stream object that redirects writes to a logger instance.
	http://www.electricmonk.nl/log/2011/08/14/redirect-stdout-and-stderr-to-a-logger-in-python/
	"""
	def __init__(self, logger, log_level=logging.INFO):
		self.logger = logger
		self.log_level = log_level

	def write(self, buf):
		for line in buf.rstrip().splitlines():
			self.logger.log(self.log_level, line.rstrip())


class NoneTracer(object):
	class __FakeMethod(object):
		def __call__(self, *args, **kwargs):
			pass

	def __init__(self, *args, **kwargs):
		self.__fakemethod = self.__FakeMethod()

	def __getattr__(self, name):
		return self.__fakemethod


class Tracer(object):
	def __init__(self, *args, **kwargs):
		self.logger = get_logger(*args, **kwargs)
		self.filehandler = None

		self.trace_lock = threading.RLock()

		self._trace_save = False
		self.trace_saved = ""

	def __del__(self):
		handlers = self.logger.handlers[:]
#		print "Tracer.__del__() - remove %d handler(s): %s" % (len(handlers), handlers)
		for hdlr in handlers:
			self.logger.removeHandler(hdlr)
			hdlr.acquire()
			try:
				hdlr.close()
			finally:
				hdlr.release()

	@property
	def screen_handler(self):
		for hdlr in self.logger.handlers:
			if isinstance(hdlr, MyStreamHandler):	# logging.StreamHandler
				return hdlr

	def setlevel(self, levelname):
		"""
		���ü�¼�ĵȼ��������ڵ����������ż�¼����־��
		���磺setlevel("WARNING")
		"""
		level = logging.getLevelName(levelname.upper())
		self.logger.setLevel(level)

	def debug(self, s):
		return self.trace(s, "debug")

	def info(self, s):
		return self.trace(s, "info")

	def warning(self, s):
		return self.trace(s, "warning")

	def error(self, s):
		return self.trace(s, "error")

	def critical(self, s):
		return self.trace(s, "critical")

	def trace_begin_save(self):
		self.trace_lock.acquire()
		self.trace_saved = ""
		self._trace_save = True
		self.trace_lock.release()

	def trace_end_save(self):
		self.trace_lock.acquire()
		self._trace_save = False
		self.trace_lock.release()

	def trace(self, *args, **kwargs):
		with self.trace_lock:
			s = " ".join(map(str, args))
			method = kwargs.get("method", "info").lower()

			if self._trace_save:
				self.trace_saved = "".join([self.trace_saved, s])

			buffname = "__screen_buf_%s" % method
			try:
				buff = self.__dict__[buffname]
				self.__dict__[buffname] = "".join([buff, s])
			except:
				self.__dict__[buffname] = s

			while True:
				buff = self.__dict__[buffname]
				i = buff.find("\n")
				if i == -1:
					break
				getattr(self.logger, method)(buff[:i])	# self.logger.<method>(...)
				self.__dict__[buffname] = buff[i + 1:]

	def traceline(self, *args, **kwargs):
		s = " ".join(map(str, args)) + "\n"
		self.trace(s, **kwargs)

	def tracelock(self):
		self.trace_lock.acquire()

	def traceunlock(self):
		self.trace_lock.release()

	def enable_filelog(self, logdir="", filename="", subtitle="",
		backup_count=30, max_bytes=0):

		def translate(s):
			"""
			ת�����в�������Ϊ�ļ������ַ�
			"""
			table = {"\\": "�v",
				"/": "�M",
				":": "��",
				"*": "��",
				"?": "��",
				'"': "��",
				">": "��",
				"<": "��",
				"|": "�O"}
			for k, v in table.iteritems():
				s = s.replace(k, v)
			return s

		if not filename:
			if subtitle:
				subtitle = "[%s]" % subtitle
			filename = r"%s%s.log" % (re.sub("<|>", "", self.logger.name),
				subtitle)
			filename = translate(filename)
		if logdir:
			filename = os.sep.join([logdir, filename])

		if self.filehandler:
			self.logger.removeHandler(self.filehandler)
		handler = DailyRotatingFileHandler(filename, backup_count, max_bytes)
		self.logger.addHandler(handler)
		handler.setFormatter(self.logger.handlers[0].formatter)
		self.filehandler = handler

	def disable_filelog(self):
		handlers = self.logger.handlers[:]
		for hdlr in handlers:
			if isinstance(hdlr, DailyRotatingFileHandler):
				self.logger.removeHandler(hdlr)
				hdlr.acquire()
				try:
					hdlr.close()
				finally:
					hdlr.release()


DefaultTracer = Tracer


class Tracer2(object):
	"""
	����extra������չlogger name��ʵ��ʹ��ͬһ��logger��¼��ͬ�������־ʱ�ֳܷ��˴ˡ�
	"""
	def __init__(self, *args, **kwargs):
		self.subtitle = kwargs.get("subtitle", "")
		formatter = logging.Formatter("%(asctime)s %(name)s%(subtitle)s: %(message)s", "%H:%M:%S")
		self.logger = get_logger2(*args, formatter=formatter, **kwargs)

	def debug(self, s):
		return self.logger.debug(s, extra=dict(subtitle=self.subtitle))

	def info(self, s):
		return self.logger.info(s, extra=dict(subtitle=self.subtitle))

	def warning(self, s):
		return self.logger.warning(s, extra=dict(subtitle=self.subtitle))

	def error(self, s):
		return self.logger.error(s, extra=dict(subtitle=self.subtitle))

	def critical(self, s):
		return self.logger.critical(s, extra=dict(subtitle=self.subtitle))

	def traceline(self, *args, **kwargs):
		s = " ".join(map(str, args))
		self.info(s, **kwargs)


class UnicodeLoggerFormatter(logging.Formatter):
	"""
	���Fomatter��msg��дǰͳһת��Ϊunicode�����codecs.open�򿪵���־�ļ�д�б����str��UnicodeDecodeError�����⡣
	����logging.conf��֧��ΪFormatter�����Զ��������������־�����ļ����޷�ֱ��ʹ�ô��ࡣ
	��ֱ������־�����ļ���ʹ�ô�������ࡣ
	"""
	def __init__(self, fmt=None, datefmt=None, encoding=None, errors='replace'):
		super(UnicodeLoggerFormatter, self).__init__(fmt, datefmt)
		self.encoding = encoding
		self.errors = errors

	def format(self, record):
		try:
			s = self._format(record)
		except UnicodeError as e:
			self.dump_record(record)
			import traceback
			return 'UnicodeLoggerFormatter - %s (see LogRecord.dump)->\n%s' % \
				   (e.message, traceback.format_exc())

		if isinstance(s, str):
			s = unicode(s, self.encoding, self.errors)
		return s

	def _format(self, record):
		"""
		�����˸����format()����
		��� s = self._fmt % record.__dict__ ���쳣�����˴���
		һ����˵�Ǹ�ʽ��ģ���ַ�����record����ĳ������ֵ�����Ͳ�һ�£�һ����str��һ����unicode��
		����Unicode�Զ�ת��ʧ�ܵ��µġ�
		"""
		record.message = record.getMessage()
		if self.usesTime():
			record.asctime = self.formatTime(record, self.datefmt)
		try:
			s = self._fmt % record.__dict__
		except UnicodeError:
			fmt_type = type(self._fmt)
			adverse_type = unicode if fmt_type is str else str
			import copy
			_record = copy.copy(record)
			for k, v in _record.__dict__.iteritems():
				if isinstance(v, adverse_type):
					v = safe_coding(v)
					setattr(_record, k, v)
			s = self._fmt % _record.__dict__
		if record.exc_info:
			# Cache the traceback text to avoid converting it multiple times
			# (it's constant anyway)
			if not record.exc_text:
				record.exc_text = self.formatException(record.exc_info)
		if record.exc_text:
			if s[-1:] != "\n":
				s = s + "\n"
			try:
				s = s + record.exc_text
			except UnicodeError:
				# Sometimes filenames have non-ASCII chars, which can lead
				# to errors when s is Unicode and record.exc_text is str
				# See issue 8924.
				# We also use replace for when there are multiple
				# encodings, e.g. UTF-8 for the filesystem and latin-1
				# for a script. See issue 13232.
				s = s + record.exc_text.decode(sys.getfilesystemencoding(),
											   'replace')
		return s

	def dump_record(self, record):
		import cPickle as pickle
		pickle.dump(record, open('LogRecord.dump', 'wb'))


class UnicodeFromGBKLoggerFormatter(UnicodeLoggerFormatter):
	"""
	���������־������Ҫ������gbk���������ʱ��ʹ�ô�Formatter�ࡣ

	��־�����ļ���ʹ�õ�ʾ����
	[formatter_dailyFileFormatter]
	class=tracer.UnicodeFromGBKLoggerFormatter
	format=%(asctime)s.%(msecs)03d - [%(thread)d] - %(levelname)s - %(name)s - %(message)s
	datefmt=%H:%M:%S
	"""
	def __init__(self, fmt=None, datefmt=None):
		super(UnicodeFromGBKLoggerFormatter, self).__init__(fmt, datefmt, encoding="gbk")


class UnicodeFromMbcsLoggerFormatter(UnicodeLoggerFormatter):
	def __init__(self, fmt=None, datefmt=None):
		super(UnicodeFromMbcsLoggerFormatter, self).__init__(fmt, datefmt, encoding="mbcs")


class UnicodeFromUtf8LoggerFormatter(UnicodeLoggerFormatter):
	def __init__(self, fmt=None, datefmt=None):
		super(UnicodeFromUtf8LoggerFormatter, self).__init__(fmt, datefmt, encoding="utf-8")


class MyStreamHandler(logging.Handler):
	"""
	ϵͳ�Դ���StreamHandler��д��ǰ����msg���������ͺ�stream.encoding
	���		��������		�Ƿ�ָ����encoding	����ʽ
	1)		unicode		��					�ȳ���д��unicode��ʧ�ܺ�ʹ��encoding������д��
	2)		unicode		��					�ȳ���д��unicode��ascii������str��ʧ�ܺ�д����UTF-8�����str��
	3)		str			-					�ȳ���д��str��ʧ�ܺ���str����unicode��UTF-8�ٴα��룬�ᱨ��
	- logging.FileHandler._open()��ָ����encodingʱ��ʹ��codecs.open���ļ�����δָ��ʱʹ��open���ļ�����
	- codecs.open��ָ����encodingʱ��̶��Զ����Ʒ�ʽ���ļ���������writeʱ�ٶ�������unicode���ͣ�����encode����
		�����������str�ͻ��ڵ�3������쳣��
	����ೢ�Խ��������⡣

	A handler class which writes logging records, appropriately formatted,
	to a stream. Note that this class does not close the stream, as
	sys.stdout or sys.stderr may be used.
	"""

	def __init__(self, strm=None):
		"""
		Initialize the handler.

		If strm is not specified, sys.stderr is used.
		"""
		logging.Handler.__init__(self)
		if strm is None:
			strm = sys.stderr
		self.stream = strm

	def flush(self):
		"""
		Flushes the stream.
		"""
		self.acquire()	# Python2.7��ʼ���ӵ�
		try:
			if self.stream and hasattr(self.stream, "flush"):
				self.stream.flush()
		finally:
			self.release()

	def emit(self, record):
		"""
		Emit a record.

		If a formatter is specified, it is used to format the record.
		The record is then written to the stream with a trailing newline.  If
		exception information is present, it is formatted using
		traceback.print_exception and appended to the stream.  If the stream
		has an 'encoding' attribute, it is used to encode the message before
		output to the stream.
		"""
		try:
			msg = self.format(record)
			stream = self.stream
			fs = "%s\n"
			try:
				if (not isinstance(msg, unicode) or
					getattr(stream, 'encoding', None) is None):
					stream.write(fs % msg)
				else:
					stream.write(fs % msg.encode(stream.encoding))
			except UnicodeError:
				stream.write(fs % msg)
			self.flush()
		except (KeyboardInterrupt, SystemExit):
			raise
		except:
			self.handleError(record)


class DailyRotatingFileHandler(logging.handlers.BaseRotatingHandler):
	def __init__(self, filename, backup_count=0, max_bytes=0, encoding=None, mode="a", delay=1):
		self.base_filename = os.path.normpath(filename)
		base, ext = extractbaseext(filename)
		filename = ".".join([base, isoformat_date(), ext])
		self.makedirs(filename)

		# ʹ��delay=1�ӳ������ļ����ɱ��������ʱ���³�ʼ��ʧ�ܡ�
		logging.handlers.BaseRotatingHandler.__init__(self, filename, mode, encoding, delay)

		self.backup_count = backup_count
		self.max_bytes = max_bytes
		self.currentDate = isoformat_date()
#		print self.baseFilename

	def close(self):
		"""
		�����Խ����delay����Ϊ1��δ��¼���ݣ��ᵼ��close()��Ч���Handler.lock���й¶�����⡣
		��� http://bugs.python.org/issue19523
		"""
		if self.stream:
			self.flush()
			if hasattr(self.stream, "close"):
				self.stream.close()
			logging.StreamHandler.close(self)
			self.stream = None
		else:
			logging.Handler.close(self)

	def makedirs(self, filename):
		absdir = os.path.split(filename)[0]
		try:
			os.makedirs(absdir)
		except:
			pass

	def shouldRollover(self, record):
		if self.max_bytes > 0:		# are we rolling over?
			if self.stream:			# ��ʹ��delay=1�ӳٴ����ļ�����ʱself.streamΪNone��
				msg = "%s\n" % self.format(record)
				self.stream.seek(0, 2)	# due to non-posix-compliant Windows feature
				if self.stream.tell() + len(msg) >= self.max_bytes:
					return True
		if self.currentDate != isoformat_date():
			return True
		return False

	def doRollover(self):
		"""
		do a rollover; in this case, a date/time stamp is appended to the filename
		when the rollover happens.  However, you want the file to be named for the
		start of the interval, not the current time.  If there is a backup count,
		then we have to get a list of matching filenames, sort them and remove
		the one with the oldest suffix.
		"""
		self.stream.close()

		self.currentDate = isoformat_date()
		base, ext = extractbaseext(self.base_filename)
		self.baseFilename = ".".join([base, isoformat_date(), ext])
		i = 1
		while os.path.exists(self.baseFilename):
			self.baseFilename = ".".join([base, isoformat_date(), str(i), ext])
			i += 1
		self.makedirs(self.baseFilename)

		if self.encoding:
			self.stream = codecs.open(self.baseFilename, self.mode, self.encoding)
		else:
			self.stream = open(self.baseFilename, self.mode)

		# ʹ���ơ�objname[1][2]*.log���������ļ������Թ�������Ϊglob��ת��[]��
		unmagic_base = base.replace("[", "[[]")

		log_files = glob.glob("%s*.%s" % (unmagic_base, ext))
		for file_ in log_files:
			m = re.match(".*?(\d{4})-(\d{2})-(\d{2}).*?\.%s" % ext, file_)
			if m and len(m.groups()) == 3:
				try:
					g = map(int, m.groups())
					d = datetime.date(g[0], g[1], g[2])
					delta = d.today() - d
					if delta.days > self.backup_count:
						print "����ɾ��������־: %s" % file_
						os.remove(file_)
				except:
					pass

	def handleError(self, record):
		"""
		���Դ���������
		"""
#		print "handleError"
		pass


class Utf8DailyRotatingFileHandler(DailyRotatingFileHandler):
	"""
	ʹ��DailyRotatingFileHandler��encoding��Ϊutf8��ʱ�����ļ���ǿ�ư�abģʽд��
	���»��з����UNIX���ˡ����������ش�������
	"""
	def __init__(self, *args, **kwargs):
		DailyRotatingFileHandler.__init__(self, *args, **kwargs)

	def emit(self, record):
		"""
		Emit a record.

		Output the record to the file, catering for rollover as described
		in doRollover().
		"""
		try:
			if self.shouldRollover(record):
				self.doRollover()
			if self.stream is None:
				# ��������self.encodingʱself._open()��ʹ��codecs.open�����ļ���
				# �����ᵼ��2�����⣬��һ���ļ���ʼ���Զ�����ģʽ�򿪣����з��޷���ȷ��\r\nд�롣
				# �ڶ���������codecs.open��д��ʱʼ�ջᰴself.encoding���б��룬
				# ��д��������Ѿ���utf8�����strʱҲ���ٴ���һ��utf8���룬�������롣
				# ����������ǿ����open�򿪣��Լ����б��������
#				self.stream = self._open()
				self.stream = open(self.baseFilename, self.mode)
			if self.encoding and (self.encoding not in ("utf-8", "utf8")):
				msg = unicode(self.format(record), "gbk").encode("utf8")
			else:
				msg = self.format(record)
			msg += "\n"
			if type(msg) is unicode:
				msg = msg.encode("utf8")
			self.stream.write(msg)
			self.flush()
		except (KeyboardInterrupt, SystemExit):
			raise
		except:
			self.handleError(record)


class UdpLogHandler(logging.Handler):
	def __init__(self, host, port):
		logging.Handler.__init__(self)
		self.host = host
		self.port = port

		import socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	def emit(self, record):
		msg = "%s\n" % self.format(record)
		self.sock.sendto(msg, 0, (self.host, self.port))


def get_logger(classname="", subtitle="", file_handler_tuple=(),):
	""" file_handler_tuple: (filename, backup_count=0, encoding=None)
	"""
	classname = re.sub("<class '(.*?)'>", r"\1", classname)
	if subtitle:
		subtitle = "[%s]" % subtitle
	classname = "<%s%s>" % (classname.split(".")[-1:][0], subtitle)

	# ��ͬһclassname�Ķ�ε��ã�getLogger()�᷵����ǰ�Ķ���
	logger = logging.getLogger(classname)
	# ����ڼ����µ�handlerǰ���������ǰ��handlers��
	for handler in logger.handlers[:]:
		logger.removeHandler(handler)	# ��logger.handlers�б����Ƴ�
		handler.close()					# ��logging._handlers��logging._handlerList���Ƴ�
	# file handler
	if file_handler_tuple:
		handler = DailyRotatingFileHandler(*file_handler_tuple)
		logger.addHandler(handler)
		# ������б�����÷��򽫵��¾��й¶����Ҫԭ�������loggingʹ����һ��ȫ���б�������Handler����
#		logger.file_handler = handler	# ����һ�� file_handler ��Ա����
	else:
		# screen handler
		handler = MyStreamHandler(sys.stdout)	# ����ʹ��stdout������stderr��ֻ�г������ʱ�ļ�¼�ˣ�������
		logger.addHandler(handler)
		# ������б�����÷��򽫵��¾��й¶����Ҫԭ�������loggingʹ����һ��ȫ���б�������Handler����
#		logger.screen_handler = handler	# ����һ�� screen_handler ��Ա����
	# formatter
	formatter = std_formatter()
	for hdlr in logger.handlers:
		hdlr.setFormatter(formatter)
	# level
	logger.setLevel(logging.DEBUG)
	return logger


def get_logger2(name, handlers="sf", **kwargs):
	logger = logging.getLogger(name)
	# ��get_logger��ͬ�����logger�Ѵ��ڣ�get_logger2����������handlers��
	if not logger.handlers:
		# screen handler
		if "s" in handlers:
			handler = MyStreamHandler(sys.stdout)
			logger.addHandler(handler)
		# file handler
		if "f" in handlers:
			filename = kwargs.get("filename")
			if filename is None:
				logpath = kwargs.get("logpath", module_path() + "Logs\\")
				filename = "%s%s.log" % (logpath, name)
			keys = filter(lambda x: x in "backup_count max_bytes encoding mode delay".split(), kwargs)
			subkwargs = {}
			for key in keys:
				subkwargs[key] = kwargs[key]
			handler = DailyRotatingFileHandler(filename, **subkwargs)
			logger.addHandler(handler)
		# formatter
		formatter = kwargs.get("formatter", std_formatter())
		for handler in logger.handlers:
			handler.setFormatter(formatter)
	# level
	level = kwargs.get("level")
	if isinstance(level, (str, unicode)):
		level = logging._levelNames.get(level)
	if level is None:
		level = logging.DEBUG
	logger.setLevel(level)
	return logger


def std_formatter():
	return logging.Formatter("%(asctime)s %(name)s: %(message)s", "%H:%M:%S")


def get_tracer(*args, **kwargs):
	"""
	����ͨ���� DefaultTracer ����Ϊ NoneTracer ���� tracer��
	"""
	return DefaultTracer(*args, **kwargs)


def get_nonetracer(*args, **kwargs):
	_tracer = NoneTracer(*args, **kwargs)
	if args:
		obj = args[0]
		obj.trace = _tracer.trace
		obj.traceline = _tracer.traceline
	return _tracer


def get_classtracer(obj, subtitle="", logdir="", backup_count=2, name="", file_enabled=False):
	if not name:
		name = obj.__class__.__name__
	_tracer = get_tracer(name, subtitle)
	if file_enabled:
		if not logdir:
			logdir = module_path() + "logs\\{classname}"
		logdir = logdir.replace("{classname}", name)
		_tracer.enable_filelog(logdir=logdir, backup_count=backup_count)
	# ����־�����󶨵�����
	obj.trace = _tracer.trace
	obj.traceline = _tracer.traceline
	return _tracer


def get_filetracer(obj, subtitle="", logdir="", backup_count=2, name=""):
	return get_classtracer(obj, subtitle, logdir, backup_count, name, file_enabled=True)


def redirect_stdout_stderr_tologger():
	logger_stdout = logging.getLogger('STDOUT')
	stdout = CompositeFile()	# ʹ��CompositeFile������py2exe.boot_common�е�sys.stdout��ͻ��
	stdout.add(sys.stdout)
	stdout.add(StreamToLogger(logger_stdout, logging.INFO))
	sys.stdout = stdout

	logger_stderr = logging.getLogger('STDERR')
	stderr = CompositeFile()	# ʹ��CompositeFile������py2exe.boot_common�е�sys.stderr��ͻ��
	stderr.add(sys.stderr)
	stderr.add(StreamToLogger(logger_stderr, logging.ERROR))
	sys.stderr = stderr


def test_redirect_stdout_stderr_tologger():
	redirect_stdout_stderr_tologger()

	logging.basicConfig(
		level=logging.DEBUG,
		format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
		filename="stdout_stderr.log",
		filemode='a'
	)

	print "Test to standard out"
	raise Exception('Test to standard error')


def nullfile():
	import platform
	return "/dev/null" if platform.system() == "Linux" else "nul"


def unicode_safe_write(f, s, encoding=None, safe_stuff=None):
	"""
	д����ʱ�������UnicodeError���Զ�������룬δָ��encodingʱĬ��Ϊϵͳ����SYS_ENCODING��
	:param f: ��write�����Ķ���
	:param s: Ҫд�����ݣ�������unicode��str��
	:param encoding: ��д����ʱ����UnicodeError�����ǽ�unicode<->strʱ���õı��룬Ĭ��Ϊϵͳ����SYS_ENCODING��
	:param safe_stuff: ����UnicodeErrorʱд����������ΪNone�Ļ��Ż�ȥ������ת�������ͬ���������ʱ�����Ч�ʡ�
	:return:
	"""
	try:
		f.write(s)
	except UnicodeError:
		safe_stuff = safe_coding(s)
		f.write(safe_stuff)
	return safe_stuff


def safe_coding(s, encoding=None, safe_stuff=None, errors='replace'):
	if not encoding:
		encoding = SYS_ENCODING
	if isinstance(s, unicode):
		if safe_stuff is None:
			safe_stuff = s.encode(encoding, errors=errors)
	else:
		if safe_stuff is None:
			safe_stuff = s.decode(encoding, errors=errors)
	return safe_stuff


class Tester(object):
	"""
	�������������Tracer�����Դй¶�����
	�������������ʱ�����̵ľ����Ӧ�ñ��ֲ��䣬
	�ڴ�Ӧ�ó������ӣ���Ϊ���ݸ�logging.getLogger()�����Ʋ�ͬ�����´����µĶ���
	"""
	def __init__(self):
		self.tracer = get_filetracer(self, subtitle=str(time.time()))
		self.traceline("begin")

	def __del__(self):
		self.traceline("end")


def test_leak():
	while True:
		_ = Tester()
		time.sleep(.01)


def test_leak2():
	"""
	http://bugs.python.org/issue19523
	������FileHandlerʱʹ����delay=1������δ��¼���ݣ��ᵼ��close()��Ч���Handler.lock���й¶��
	ĿǰDailyRotatingFileHandler����ͨ������close����������������⡣
	"""
	while True:
		filename = "test.log"
		handler = logging.FileHandler(filename, mode="w", delay=1)
		handler.close()
#		handler.lock = None
		time.sleep(.01)


if __name__ == "__main__":
	test_leak()
