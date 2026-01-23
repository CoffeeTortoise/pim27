import os

import time

from fstring import f

from .decorators import cached

from .constants import (
	MAX_CACHE_SIZE,
	OPS_SEPARATOR,
	PIXEL_COLOR_SEP,
	DO_NOT_CHANGE_COLOR
)


@cached(MAX_CACHE_SIZE)
def force_correct_ops_sep(str_ops):
	return (
		str_ops
		.replace(' ', OPS_SEPARATOR)
		.replace('.', OPS_SEPARATOR)
		.replace('/', OPS_SEPARATOR)
		.replace('\\', OPS_SEPARATOR)
		.replace(':', OPS_SEPARATOR)
		.replace(';', OPS_SEPARATOR)
		.replace('-', OPS_SEPARATOR)
		.replace('+', OPS_SEPARATOR)
		.replace('|', OPS_SEPARATOR)
		.replace('^', OPS_SEPARATOR)
		.replace('>', OPS_SEPARATOR)
		.replace('<', OPS_SEPARATOR)
	)


@cached(MAX_CACHE_SIZE)
def force_correct_pixel_color_sep(str_ops):
	return (
		str_ops
		.replace(' ', PIXEL_COLOR_SEP)
		.replace('.', PIXEL_COLOR_SEP)
		.replace('/', PIXEL_COLOR_SEP)
		.replace('\\', PIXEL_COLOR_SEP)
		.replace(':', PIXEL_COLOR_SEP)
		.replace(';', PIXEL_COLOR_SEP)
		.replace('-', PIXEL_COLOR_SEP)
		.replace('+', PIXEL_COLOR_SEP)
		.replace('|', PIXEL_COLOR_SEP)
		.replace('^', PIXEL_COLOR_SEP)
		.replace('>', PIXEL_COLOR_SEP)
		.replace('<', PIXEL_COLOR_SEP)
	)


@cached(MAX_CACHE_SIZE)
def get_rid_of_quotes(str_):
	return (
		str_
		.replace('\'', '')
		.replace('\"', '')
	).strip()


@cached(MAX_CACHE_SIZE)
def get_rid_of_brackets(str_):
	return (
		str_
		.replace('[', '')
		.replace(']', '')
		.replace('(', '')
		.replace(')', '')
		.replace('{', '')
		.replace('}', '')
	).strip()


@cached(MAX_CACHE_SIZE)
def rename_if_misspelled(filepath, extsep_pos):
	ext = filepath[extsep_pos + 1: ].lower().strip()
	if ext == 'jpeg':
		new_path = filepath.replace('.jpeg', '.jpg')
	if ext == 'tif':
		new_path = filepath.replace('.tif', '.tiff')
	if ext == 'jpeg' or ext == 'tif':
		os.rename(filepath, new_path)
		filepath = new_path
	return filepath


@cached(MAX_CACHE_SIZE)
def get_signed_float_from_str(str_):
	return float(
		get_rid_of_brackets(
			get_rid_of_quotes(str_)
		)
		.replace(',', '.')
		.replace('_', '')
		.replace(' ', '')
		.strip()
	)


def get_signed_int_from_str(str_):
	return int(
		get_signed_float_from_str(str_)
	)


def get_float_from_str(str_):
	return max(
		abs(get_signed_float_from_str(str_)),
		0
	)


def get_int_from_str(str_):
	return int(
		get_float_from_str(str_)
	)


@cached(MAX_CACHE_SIZE)
def get_color_from_str(color):
	if color.strip() == DO_NOT_CHANGE_COLOR:
		return DO_NOT_CHANGE_COLOR
	c = [
		min(
			255, abs(get_int_from_str(p))
		)
		for p in force_correct_pixel_color_sep(
			get_rid_of_quotes(
				get_rid_of_brackets(color)
			).replace(' ', '')
		).split(PIXEL_COLOR_SEP)
		if p
	]
	diff = 3 - len(c)
	if diff > 0:
		c.extend([255] * diff)
	return tuple(c)


def get_time_marked_line(line):
	prefix = (
		time.ctime(
			time.time()
		)
		.replace(' ', '_')
		.replace(':', '_')
	).strip()
	return f('${prefix}_${line}')


@cached(MAX_CACHE_SIZE)
def get_raw_path(filepath):
	if filepath.startswith('\'') or filepath.startswith('\"'):
		start = 1
	else:
		start = 0
	if filepath.endswith('\'') or filepath.endswith('\"'):
		end = -1
	else:
		end = len(filepath)
	return os.path.normpath(
		filepath[start : end].strip()
	)


@cached(MAX_CACHE_SIZE)
def get_raw_format(file_format):
	i = 1 if file_format.startswith(os.extsep) else 0
	j = -1 if file_format.endswith(os.extsep) else len(file_format)
	ext = file_format[i : j].strip()
	if ext == 'jpeg':
		ext = 'jpg'
	if ext == 'tif':
		ext = 'tiff'
	return ext.replace('.', '')
