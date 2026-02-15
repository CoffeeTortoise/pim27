from .decorators import cached

from .constants import (
	ALL_FORMATS_C,
	DEFAULT_KX,
	DEFAULT_KY,
	DEFAULT_RARITY,
	OPS_SEPARATOR,
	DEFAULT_KEEP_W,
	DEFAULT_KEEP_H,
	DEFAULT_CHAR_W,
	DEFAULT_CHAR_H,
	DEFAULT_FLIP_MODE,
	DEFAULT_COLOR_TOOL,
	DEFAULT_IGNORE_CASE,
	DEFAULT_ROTATE_DEGREE,
	DEFAULT_DELETE_ORIGINAL,
	DEFAULT_ENHANCE_MODE,
	DEFAULT_ENHANCE_FACTOR,
	DEFAULT_PIXEL_X,
	DEFAULT_PIXEL_X1,
	DEFAULT_PIXEL_Y,
	DEFAULT_PIXEL_Y1,
	DEFAULT_PIXEL_COLOR,
	MAX_PIXEL_COORDINATE
)

from .transformators import (
	get_raw_format,
	get_int_from_str,
	get_float_from_str,
	get_color_from_str,
	get_rid_of_quotes,
	get_rid_of_brackets,
	get_signed_int_from_str,
	get_signed_float_from_str,
	force_correct_ops_sep,
	force_correct_pixel_color_sep
)


def parse_rarity(parser_args):
	if parser_args.rarity is None or parser_args.rarity == ALL_FORMATS_C:
		return DEFAULT_RARITY
	return get_int_from_str(parser_args.rarity)


def parse_enhance_mode(parser_args):
	if parser_args.enhance_mode is None or parser_args.enhance_mode == ALL_FORMATS_C:
		return DEFAULT_ENHANCE_MODE
	return get_rid_of_quotes(parser_args.enhance_mode.lower())


def parse_enhance_factor(parser_args):
	if parser_args.enhance_factor is None or parser_args.enhance_factor == ALL_FORMATS_C:
		return DEFAULT_ENHANCE_FACTOR
	return get_signed_float_from_str(parser_args.enhance_factor)


def parse_color_from(parser_args):
	if parser_args.color_from is None or parser_args.color_from == ALL_FORMATS_C:
		return DEFAULT_PIXEL_COLOR
	return get_color_from_str(parser_args.color_from)


def parse_color_filler(parser_args):
	if parser_args.color_filler is None or parser_args.color_filler == ALL_FORMATS_C:
		return DEFAULT_PIXEL_COLOR
	return get_color_from_str(parser_args.color_filler)


def parse_color_to(parser_args):
	if parser_args.color_to is None or parser_args.color_to == ALL_FORMATS_C:
		return DEFAULT_PIXEL_COLOR
	return get_color_from_str(parser_args.color_to)


def parse_pixel_x(parser_args):
	if parser_args.pixel_x is None or parser_args.pixel_x == ALL_FORMATS_C:
		return DEFAULT_PIXEL_X
	n = get_signed_int_from_str(parser_args.pixel_x)
	if n == MAX_PIXEL_COORDINATE:
		return n
	return abs(n)


def parse_pixel_x1(parser_args):
	if parser_args.pixel_x1 is None or parser_args.pixel_x1 == ALL_FORMATS_C:
		return DEFAULT_PIXEL_X1
	n = get_signed_int_from_str(parser_args.pixel_x1)
	if n == MAX_PIXEL_COORDINATE:
		return n
	return abs(n)


def parse_pixel_y(parser_args):
	if parser_args.pixel_y is None or parser_args.pixel_y == ALL_FORMATS_C:
		return DEFAULT_PIXEL_Y
	n = get_signed_int_from_str(parser_args.pixel_y)
	if n == MAX_PIXEL_COORDINATE:
		return n
	return abs(n)


def parse_pixel_y1(parser_args):
	if parser_args.pixel_y1 is None or parser_args.pixel_y1 == ALL_FORMATS_C:
		return DEFAULT_PIXEL_Y1
	n = get_signed_int_from_str(parser_args.pixel_y1)
	if n == MAX_PIXEL_COORDINATE:
		return n
	return abs(n)


def parse_operation(parser_args):
	ops = force_correct_ops_sep(
		get_rid_of_quotes(
			get_rid_of_brackets(parser_args.operation)
		).replace(' ', '')
	).strip()
	for o in ops.split(OPS_SEPARATOR):
		yield o.strip()


def parse_char_w(parser_args):
	if parser_args.char_w is None or parser_args.char_w == ALL_FORMATS_C:
		return DEFAULT_CHAR_W
	return abs(
		get_int_from_str(parser_args.char_w)
	)


def parse_char_h(parser_args):
	if parser_args.char_h is None or parser_args.char_h == ALL_FORMATS_C:
		return DEFAULT_CHAR_H
	return abs(
		get_int_from_str(parser_args.char_h)
	)


def parse_flip_mode(parser_args):
	if parser_args.flip_mode is None or parser_args.flip_mode == ALL_FORMATS_C:
		return DEFAULT_FLIP_MODE
	return get_rid_of_quotes(parser_args.flip_mode)


def parse_rotate_degree(parser_args):
	if parser_args.rotate_degree is None or parser_args.rotate_degree == ALL_FORMATS_C:
		return DEFAULT_ROTATE_DEGREE
	a = get_float_from_str(parser_args.rotate_degree)
	if a > 360:
		return divmod(a, 360)[1]
	if a < -360:
		v = divmod(abs(a), 360)[1]
		return -v
	return a


def parse_color_tool(parser_args):
	if parser_args.color_tool is None or parser_args.color_tool == ALL_FORMATS_C:
		return DEFAULT_COLOR_TOOL
	return get_rid_of_quotes(parser_args.color_tool)


def parse_delete_original(parser_args):
	if parser_args.delete_original is None or parser_args.delete_original == ALL_FORMATS_C:
		return DEFAULT_DELETE_ORIGINAL
	return get_int_from_str(parser_args.delete_original)


def parse_result_format(parser_args):
	if parser_args.result_format is None:
		return ALL_FORMATS_C
	return get_raw_format(parser_args.result_format)


def parse_search_for_substr(parser_args):
	if parser_args.search_for_substr is None:
		return ALL_FORMATS_C
	return get_rid_of_quotes(parser_args.search_for_substr)


def parse_ignore_case_substr(parser_args):
	if parser_args.ignore_case_substr is None or parser_args.ignore_case_substr == ALL_FORMATS_C:
		return DEFAULT_IGNORE_CASE
	return get_int_from_str(parser_args.ignore_case_substr)


def parse_target_format(parser_args):
	if parser_args.target_format is None:
		return ALL_FORMATS_C
	return get_raw_format(parser_args.target_format)


def parse_width(parser_args):
	if parser_args.width is None or parser_args.width == ALL_FORMATS_C:
		return 0
	return get_int_from_str(parser_args.width)


def parse_height(parser_args):
	if parser_args.height is None or parser_args.height == ALL_FORMATS_C:
		return 0
	return get_int_from_str(parser_args.height)


def parse_keepw(parser_args):
	if parser_args.keep_w is None or parser_args.keep_w == ALL_FORMATS_C:
		return DEFAULT_KEEP_W
	return get_int_from_str(parser_args.keep_w)


def parse_keeph(parser_args):
	if parser_args.keep_h is None or parser_args.keep_h == ALL_FORMATS_C:
		return DEFAULT_KEEP_H
	return get_int_from_str(parser_args.keep_h)


def parse_kx(parser_args):
	if parser_args.kx is None or parser_args.kx == ALL_FORMATS_C:
		return DEFAULT_KX
	return get_float_from_str(parser_args.kx)


def parse_ky(parser_args):
	if parser_args.ky is None or parser_args.ky == ALL_FORMATS_C:
		return DEFAULT_KY
	return get_float_from_str(parser_args.ky)
