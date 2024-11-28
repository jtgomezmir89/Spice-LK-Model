

# Copyright (c) 2015, 2016, 2017 MURAMATSU Atsushi <amura@tomato.sakura.ne.jp>

import sys
import os
import io
import math
import locale
import struct
import gzip
import subprocess
from datetime import datetime
from abc import ABCMeta, abstractmethod
import numpy as np



try:
	from typing import (Text, Tuple, List, Dict,
						IO, Callable, Iterable, Optional, Union, Any)
except ImportError:
	Text = Any = None # type: ignore
	class _DummyCls(object):
		def __getitem__(self, *args): pass # type: ignore
	Tuple = List = Dict = IO = _DummyCls # type: ignore
	Callable = Iterable = Optional = Union = _DummyCls # type: ignore

INDEX_TYPES = ('time', 'frequency')

if sys.version_info[0] >= 3:
	def _to_string_lat1(by): # type: (bytes) -> Text
		return by.decode('latin-1')
	def _to_string_utf16le(by): # type: (bytes) -> Text
		return by.decode('utf-16le')
	def _readline_lat1(fd): # type: (IO[bytes]) -> Text
		return _to_string_lat1(fd.readline())
	def _readline_utf16le(fd): # type: (IO[bytes]) -> Text
		by = fd.readline()
		if len(by) % 2 == 1 and by[-1] == ord("\n"):
			by += fd.read(1)
		return _to_string_utf16le(by)
	def _check_utf16le(by): # type: (bytes) -> bool
		if 0 in by:
			return True
		return False
	_basestring = str
else:
	def _to_string_lat1(by): # type: (bytes) -> Text
		return by
	def _to_string_utf16le(by): # type: (bytes) -> Text
		return unicode(by, coding='utf-16le') # type: ignore
	def _readline_lat1(fd): # type: (IO[bytes]) -> Text
		return _to_string_lat1(fd.readline())
	def _readline_utf16le(fd): # type: (IO[bytes]) -> Text
		by = fd.readline()
		if len(by) % 2 == 1 and by[-1] == "\n":
			by += fd.read(1)
		return _to_string_utf16le(by)
	def _check_utf16le(by): # type: (bytes) -> bool
		if "\0" in by:
			return True
		return False
	_basestring = basestring

LTSPICE_FILES = [
	("LTspiceXVII", "XVIIx64.exe", 17),
	("LTspiceXVII", "XVIIx86.exe", 17),
	("LTspiceIV", "scad3.exe", 4),
]

LTSPICE = None
def get_ltspice_program(forced_version=None):
	# type: (int) -> Optional[List[Text]]
	"""Get LTspice command.
	Args:
		forced_version (int, optional): select LTspice version.
			Now supported versions are 4 and 17.
			Default is latest version which is founded.
	Returns:
		None, list[str].
		If LTspice is not found, this function returns None.
	"""
	if sys.platform in ('win32', 'win64'):
		progdirs = []
		progdir = os.getenv("PROGRAMFILES")
		if progdir is not None:
			progdirs.append(progdir)
		progdir_x86  = os.getenv("ProgramFiles(x86)")
		if progdir_x86 is not None:
			progdirs.append(progdir_x86)
		for progdir in progdirs:
			for d, f, v in LTSPICE_FILES:
				if (forced_version is not None and v != forced_version):
					continue
				exefile = os.path.join(progdir, "LTC", d, f)
				if os.path.exists(exefile):
					return [ exefile ]
	elif sys.platform == 'darwin':
		exefile = "/Applications/LTspice.app/Contents/MacOS/LTspice"
		if os.path.exists(exefile):
			return [ exefile ]
	else: # UN*X with wine
		for progdir in (
				os.path.expanduser("~/.wine/drive_c/Program Files"),
				os.path.expanduser("~/.wine/drive_c/Program Files (x86)")):
			if not os.path.exists(progdir):
				continue
			for d, f, v in LTSPICE_FILES:
				if (forced_version is not None and v != forced_version):
					continue
				exefile = os.path.join(progdir, "LTC", d, f)
				if os.path.exists(exefile):
					return [ "wine", exefile ]
	return None
if LTSPICE is None:
	LTSPICE = get_ltspice_program()

def _parse_date(s): # type: (Text) -> datetime
	old_locale = locale.getlocale(locale.LC_TIME)
	try:
		locale.setlocale(locale.LC_TIME, "C")
		return datetime.strptime(s, "%a %b %d %H:%M:%S %Y")
	finally:
		locale.setlocale(locale.LC_TIME, old_locale)

def _parse_any(s): # type: (Text) -> Union[int,float,Text]
	try:
		return int(s)
	except ValueError:
		try:
			return float(s)
		except ValueError:
			return s

def read_ltspice_log(logfile): # type: (Text) -> Optional[Dict[Text,Any]]
	"""Read information of LTspice simulation from logfile
	Args:
		logfile (str): filename of logfile.
			Gzipped logfile is also supported.
	Returns:
		dict: informations
	
		Now supported informations are:
		:steps: tuple of (variable, step value)
		:date: Simulated date
		:total elasp time: Total elasp time of simulation
	"""
	if not os.path.exists(logfile):
		return None
	
	encoding = 'latin-1'
	if logfile.endswith(".gz"):
		_open = gzip.open # type: Callable[..., IO]
	else:
		_open = io.open
	with _open(logfile, 'rb') as f:
		line = f.readline()
		if _check_utf16le(line):
			encoding = 'utf-16le'
	result = {} # type: Dict[Text,Any]
	step_data = []
	with _open(logfile, 'r', encoding=encoding) as f:
		for line in f:
			if line.startswith(".step "):
				k, v = line[6:].split('=', 1)
				step_data.append((k.strip().lower(), float(v)))
			elif ':' in line:
				k, v = [ s.strip() for s in line.split(':', 1) ]
				k = k.lower()
				if k == 'date':
					v = _parse_date(v.strip())
				elif k == 'total elapsed time':
					v = float(v.strip().split()[0])
				result[k] = v
			elif '=' in line:
				k, v = [ s.strip() for s in line.split('=', 1) ]
				result[k.lower()] = _parse_any(v)
	if len(step_data):
		result['steps'] = tuple(step_data)
	return result

class _DataReaderBase(object):
	__metaclass__ = ABCMeta

	@abstractmethod
	def get_bulk_lengths(self):
		# type: () -> Iterable[int]
		pass

	@abstractmethod
	def get_bulk(self, start, end, stride):
		# type: (int, int, int) -> Optional[np.ndarray]
		pass

class _RawDataReader(_DataReaderBase):
	def __init__(self, f, col, row, index, var_using,
				 is_binary, is_complex, is_stepped, readline):
		# type: (IO[bytes], int, int, int, List[int], bool, bool, bool, Callable[[IO[bytes]],Text]) -> None
		
		self.f = f
		self.col = col
		self.row = row
		self.index = index
		self.var_using = np.array(var_using)
		self.readline = readline
		self.is_binary = is_binary
		self.is_complex = is_complex

		if is_binary:
			self.skip_row = self._skip_row_binary
			if is_complex:
				self.get_row = self._get_row_binary_cpx
				self.fmt = "<%dd" % (2 * self.col)
			else:
				self.get_row = self._get_row_binary_real
				fmt = ["<"]
				for c in range(self.col):
					if c == index:
						fmt.append("d")
					else:
						fmt.append("f")
				self.fmt = "".join(fmt)
			self.rowsize = struct.calcsize(self.fmt)
		else:
			self.get_row = self._get_row_text
			self.skip_row = self._skip_row_text
		
		if is_stepped:
			self.data_bulk = self._check_bulk_info()
		else:
			self.data_bulk = [(self.row, 0)]
		self.next_bulk = 0

	def _get_row_binary_cpx(self, check_n=None): # type: (int) -> np.ndarray
		v = struct.unpack(self.fmt, self.f.read(self.rowsize))
		return np.array([ complex(v[2*i], v[2*i+1]) for i in range(self.col) ])

	def _get_row_binary_real(self, check_n=None): # type: (int) -> np.ndarray
		return np.array(struct.unpack(self.fmt, self.f.read(self.rowsize)))

	def _get_row_text(self, check_n=None): # type: (int) -> np.ndarray
		def _complex(st): # type: (Text) -> complex
			return complex(*[ float(s) for s in st.split(',') ])
		if self.is_complex:
			_parser = _complex # type: Callable[[Text], Union[float,complex]]
		else:
			_parser = float
		result = []
		v, st = self.readline(self.f).strip().split()
		try:
			n = int(v)
		except ValueError:
			raise Exception("broken format")
		if check_n is not None and n != check_n:
			raise Exception("broken format")
		result.append(_parser(st))
		for i in range(1, self.col):
			st = self.readline(self.f).strip()
			result.append(_parser(st))
		return np.array(result)

	def _skip_row_binary(self, num=1, check_n=None): # type: (int, int) -> None
		if num == 0: return
		self.f.seek(num * self.rowsize, 1)

	def _skip_row_text(self, num=1, check_n=None): # type: (int, int) -> None
		for i in range(num):
			v, st = self.readline(self.f).strip().split()
			try:
				n = int(v)
			except ValueError:
				raise Exception("broken format")
			if check_n is not None:
				if n != check_n:
					raise Exception("broken format")
				check_n += 1
			for j in range(1, self.col):
				st = self.readline(self.f)

	def _check_bulk_info(self): # type: () -> List[Tuple[int, int]]
		data_bulk = [] # type: List[Tuple[int,int]]
		data_pos = self.f.tell()
		first_data = self.get_row()[self.index]
		data_num = 1
		for i in range(1, self.row):
			v = self.get_row()[self.index]
			if v == first_data:
				if data_num == 1:
					if len(data_bulk) > 0:
						data_bulk[-1] = (data_bulk[-1][0], data_bulk[-1][1]+1)
				else:
					data_bulk.append((data_num, 0))
				data_num = 0
			data_num += 1
		if data_num != 1:
			data_bulk.append((data_num, 0))
		self.f.seek(data_pos)
		return data_bulk

	def get_bulk_lengths(self): # type: () -> Iterable[int]
		return (length for length, skip in self.data_bulk)
	
	def get_bulk(self, start, end, stride):
		# type: (int, int, int) -> Optional[np.ndarray]
		
		if end <= start:
			self.skip_row(sum(self.data_bulk[self.next_bulk]), check_n=0)
			self.next_bulk += 1
			return None
		
		length = int(math.ceil((end - start + 0.0) / stride))
		if self.is_complex:
			M = np.empty((length, len(self.var_using)), dtype='complex128')
		else:
			M = np.empty((length, len(self.var_using)), dtype='float64')
		
		data_no = 0
		# skip start
		if start > 0:
			self.skip_row(start, check_n=data_no)
			data_no += start

		if stride == 1: # special but ordinary case
			for i in range(length):
				data = self.get_row(check_n=(data_no + i))
				M[i,:] = data[self.var_using]
			data_no += length
		else:
			for i in range(length):
				data = self.get_row(check_n=data_no)
				data_no += 1
				M[i,:] = data[self.var_using]
				if i != length-1:
					self.skip_row(stride - 1, check_n=data_no)
					data_no += stride - 1
		
		# skip end
		row_num = sum(self.data_bulk[self.next_bulk])
		if data_no < row_num:
			self.skip_row(row_num - data_no, check_n=data_no)
		
		self.next_bulk += 1
		return M # type: ignore

class _FastDataReader(_DataReaderBase):
	def __init__(self, f, col, row, index, var_using, is_stepped):
		# type: (IO[bytes], int, int, int, List[int], bool) -> None
		
		self.f = f
		self.data_pos = f.tell()
		self.col = col
		self.row = row
		self.index = index
		self.var_using = var_using
		
		if is_stepped:
			self.data_bulk = self._check_bulk_info()
		else:
			self.data_bulk = [(self.row, 0)]
		self.next_bulk = 0
	
	def _check_bulk_info(self): # type: () -> List[Tuple[int,int]]
		self.f.seek(self.data_pos + 4 * self.row * self.index)
		index = np.array(struct.unpack(
			"<%dd" % self.row, self.f.read(8 * self.row)), dtype=float)
		self.f.seek(self.data_pos)
		
		data_bulk = [] # type: List[Tuple[int,int]]
		first_data = index[0]
		data_num = 1
		for v in index[1:]:
			if v == first_data:
				if data_num == 1:
					data_bulk[-1] = (data_bulk[-1][0], data_bulk[-1][1]+1)
				else:
					data_bulk.append((data_num, 0))
				data_num = 0
			data_num += 1
		if data_num != 1:
			data_bulk.append((data_num, 0))
		return data_bulk

	def get_bulk_lengths(self): # type: () -> Iterable[int]
		return (length for length, skip in self.data_bulk)

	def get_bulk(self, start, end, stride):
		# type: (int, int, int) -> Optional[np.ndarray]
		
		if end <= start:
			self.next_bulk += 1
			return None
		self.f.seek(self.data_pos)
		bulk_offset = 0
		for i in range(self.next_bulk):
			bulk_offset += sum(self.data_bulk[i])
		start += bulk_offset
		end += bulk_offset
		length = int(math.ceil((end - start + 0.0) / stride))
		
		M = np.empty((length, len(self.var_using)), dtype='float64')
		
		data_mask = np.zeros(self.row, dtype=bool)
		data_mask[np.array(range(start, end, stride))] = True
		
		for var_index in range(self.col):
			if var_index == self.index:
				fmt = "d"
				size = 8
			else:
				fmt = "f"
				size = 4
			buf = self.f.read(size * self.row)
			if var_index in self.var_using:
				var_pos = self.var_using.index(var_index)
				M[:,var_pos] = np.array(
					struct.unpack("<%d%s" % (self.row, fmt), buf),
					dtype=float)[data_mask]
		self.next_bulk += 1
		return M # type: ignore

def read_ltspice_raw(filename, vars=None, header_only=False,
					 start=0, end=None, length=None, stride=1):
	# type: (Text, List[Text], bool, Union[int,float], Union[int,float], int, int) -> Dict[Text,Any]
	"""Read simulation data of LTspice.
	Args:
		filename (str): filename of simulation data.
			Transient, AC, Operation result and fastacccess converted
			Transient data are supported.
			Gzipped datafile is also supported.
		vars (list[str], optional): read variables.
			If ``vars`` is None, all variables are read.
		headers_only (bool, optional): header only read mode.
		start (int or float, optional): start of data
		end (int or float, optional): end of data
		length (int, optional): read lenght of data
		stride (int, optional): reading stride of data
	Returns:
		dict: data
	
		Now supported data are:
		:variables: tuple(variables name, vairable type)
		:no. variables: num of variables
		:no. points: num of data points
		:offset: data start offset
		:date: simulation date
		:backannotation:
		:flags:
		:steps: step information (if stepped flag is exist)
		:values: numpy.ndarray (if stepped flag is not exist)
				 tuple of numpy.ndarray (if stepped flag is exist)
	"""
	
	is_firstline = True
	is_binary = None
	is_complex = False
	is_forward = False
	is_stepped = False
	is_fastaccess = False
	is_utf16le = False
	col = None
	row = None
	index_col = None
	var_list = [] # type: List[Tuple[Text,Text]]
	var_using = [] # type: List[int]
	result = {} # type: Dict[Text,Any]

	_to_string = None
	_readline = None

	if end is not None and length is not None:
		raise ValueError("cannot set 'end' and 'length' paramters at same time")
	stride = int(stride)
	if stride < 1:
		raise ValueError("'stride' parameter must be 1 or above")

	if filename.endswith(".gz"):
		_open = gzip.open # type: Callable[...,IO]
		basename = filename[:-3]
		logfile = os.path.splitext(basename)[0] + ".log.gz"
		if not os.path.exists(logfile):
			logfile = os.path.splitext(basename)[0] + ".log"
	else:
		_open = open
		logfile = os.path.splitext(filename)[0] + ".log"

	logdata = read_ltspice_log(logfile)

	with _open(filename, 'rb') as f:
		# check encoding is UTF-16LE or not
		xline = f.readline()
		is_utf16le = _check_utf16le(xline)
		if is_utf16le:
			xline += f.read(1) # add upper byte of "\n"
			_to_string = _to_string_utf16le
			_readline = _readline_utf16le
		else:
			_to_string = _to_string_lat1
			_readline = _readline_lat1
		line = _to_string(xline)

		# Read text part
		while line != u"":
			s = line.split(':', 1)
			if len(s) == 1:
				var, value = s[0], u""
			else:
				var, value = s
			var = var.lower()

			if var == "binary":
				is_binary = True
				break
			elif var == "values":
				is_binary = False
				break
			elif var == "variables":
				if col is None:
					raise Exception("invalid data")
				for i in range(col):
					s = _readline(f)
					if s == "":
						break
					ss = s.split()
					if vars is None or ss[1] in vars or ss[2] in INDEX_TYPES:
						if ss[2] in INDEX_TYPES:
							index_col = i
						var_list.append(tuple(ss[1:]))
						var_using.append(i)
			elif var == "no. variables":
				col = int(value.strip())
				result[var] = col
			elif var == "no. points":
				row = int(value.strip())
				result[var] = row
			elif var == "offset":
				result[var] = float(value.strip())
			elif var == "date":
				result[var] = _parse_date(value.strip())
			elif var == "backannotation":
				if var not in result:
					result[var] = []
				result[var].extend(value.strip().split())
			elif var == "flags":
				result[var] = tuple(value.strip().split())
				if 'complex' in result[var]:
					is_complex = True
				if 'forward' in result[var]:
					is_forward = True
				if 'stepped' in result[var]:
					is_stepped = True
				if 'fastaccess' in result[var]:
					is_fastaccess = True
			else:
				result[var] = _parse_any(value.strip())

			line = _readline(f)

		if logdata is not None:
			result["logdata"] = logdata
		result["variables"] = tuple(var_list)
		if header_only:
			result["values"] = None
			if is_stepped and logdata is not None and 'steps' in logdata:
				result["steps"] = logdata['steps']
			return result

		if col is None or row is None or index_col is None or is_binary is None:
			raise Exception("invalid data")
		if is_fastaccess:
			if not is_binary or is_complex:
				raise Exception(
					"invalid format, fastaccess is only for real binary") 
			reader = _FastDataReader(
				f, col, row, index_col, var_using, is_stepped) # type: _DataReaderBase
		else:
			reader = _RawDataReader(
				f, col, row, index_col, var_using,
				is_binary, is_complex, is_stepped, _readline)

		values = []
		for data_len in reader.get_bulk_lengths():
			xstart = (int(data_len * start)
					  if isinstance(start, float) else start)
			if xstart < 0:
				xstart = max(data_len + xstart, 0)

			max_length = (data_len - xstart) // stride
			if length is not None:
				xlength = (int(data_len * length)
						   if isinstance(length, float) else length)
				xlength = min(xlength, max_length)
				xend = xstart + (xlength - 1)*stride + 1
			elif end is None:
				xlength = max_length
				xend = data_len
			else:
				xend = int(data_len * end) if isinstance(end, float) else end
				if xend < 0:
					xend = data_len + xend
				xend = max(xend, xstart)
				xlength = (xend - xstart) // stride
			values.append(reader.get_bulk(xstart, xend, stride))

	if is_stepped:
		result["values"] = tuple(values)
		if (logdata is not None and 'steps' in logdata and
			len(logdata['steps']) == len(values)):
			result["steps"] = logdata['steps']
		else:
			result["steps"] = tuple([ ("", i) for i in range(len(values)) ])
	else:
		result["values"] = values[0]

	return result

def make_dataframe(data):
	import pandas as pd
	columns = [name for name, type_ in data['variables']]
	if "steps" in data:
		dfs = []
		for i, step in enumerate(data["steps"]):
			step_name = "STEP:{}=".format(step[0])
			step_val = step[1]
			d = data['values'][i]
			if d is not None:
				df = pd.DataFrame(d, columns=columns)
				df[step_name] = step_val
				dfs.append(df)
		df = pd.concat(dfs)
	else:
		df = pd.DataFrame(data['values'], columns=columns)
	return df

def find_variable(data, key):
	# type: (Dict, Union[Text,Tuple[Text,Text]]) -> Union[None,int,List[int]]
	"""Find variable index.
	Args:
		data (dict): data of LTspice output
		key (str or tuple[str,str]): finding variable
	Returns:
		None, int or list[int]: index of variable
		If variable is not found, this function returns None
	"""
	
	if isinstance(key, _basestring):
		result = [ i for i, item in enumerate(data['variables'])
				   if item[0] == key ]
	else:
		result = [ i for i, item in enumerate(data['variables'])
				   if item == key ]
	if len(result) == 0:
		return None
	elif len(result) == 1:
		return result[0]
	return result

def run(filename, remove_generated_netlist=True):
	# type: (Text, bool) -> None
	"""Run LTspice simulation.
	Args:
		filename (str): filename of ``.asc`` or ``.net``
		remove_generated_netlist (bool, optional):
			Remove generated netlist by this function.
			Default is True.  When argument filename is ``.net`` file,
			this argument is ignored.
	Returns:
		None
	"""
	
	filename = os.path.abspath(filename)
	dirname = os.path.split(filename)[0]
	convert_netlist = False
	orig_cwd = os.getcwd()
	if LTSPICE is None:
		raise Exception("LTspice is not found")
	else:
		ltspice = LTSPICE
	
	try:
		os.chdir(dirname)
		if filename.endswith(".asc"):
			convert_netlist = True
			netname = os.path.splitext(filename)[0] + ".net"
			if os.path.exists(netname):
				os.remove(netname)
			subprocess.call(ltspice + ['-netlist', filename ])
			if not os.path.exists(netname):
				raise Exception("Netfile creating error")
		else:
			netname = filename
		subprocess.call(ltspice + [ '-b', netname ])
	finally:
		try:
			if convert_netlist and remove_generated_netlist:
				os.remove(netname)
		except:
			pass
		os.chdir(orig_cwd)
