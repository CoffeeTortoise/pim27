import os

from fstring import f

from PIL import Image

from ..validators import (
	is_image,
	is_substr_in_str
)

from ..transformators import (
	get_raw_path,
	get_time_marked_line
)

from ..decorators import info

from ..constants import (
	ALL_FORMATS_C,
	MAX_PIXEL_COORDINATE
)

from ..argument_parser import (
	parse_pixel_x,
	parse_pixel_x1,
	parse_pixel_y,
	parse_pixel_y1,
	parse_delete_original,
	parse_search_for_substr,
	parse_ignore_case_substr
)


@info
def cut_image(
	in_path,
	x, x1,
	y, y1,
	delete_original
):
	dirname, bname = os.path.split(in_path)
	oname = get_time_marked_line(bname)
	out_path = os.path.join(
		dirname, f('cut_${oname}')
	)
	with Image.open(in_path) as img:
		if x1 == MAX_PIXEL_COORDINATE:
			x1 = img.width
		if y1 == MAX_PIXEL_COORDINATE:
			y1 = img.height
		crop = img.crop((x, y, x1, y1))
		crop.save(out_path)
	if delete_original:
		if os.path.isfile(out_path):
			os.remove(in_path)
			os.rename(out_path, in_path)
			return in_path
	return out_path


def cut_folder(
	target,
	x, x1,
	y, y1,
	delete_original,
	search_for_substr,
	ignore_case_substr
):
	if ignore_case_substr:
		search_for_substr = search_for_substr.lower()
	for root, dirs, files in os.walk(target):
		for f in files:
			if not is_image(f):
				continue
			filepath = os.path.join(root, f)
			if search_for_substr == ALL_FORMATS_C:
				cut_image(
					filepath,
					x, x1,
					y, y1,
					delete_original
				)
			else:
				fp = filepath.lower() if ignore_case_substr else filepath
				if is_substr_in_str(search_for_substr, fp):
					cut_image(
						filepath,
						x, x1,
						y, y1,
						delete_original
					)


def cut(
	target,
	x, x1,
	y, y1,
	delete_original,
	search_for_substr,
	ignore_case_substr
):
	if os.path.isdir(target):
		return cut_folder(
			target,
			x, x1,
			y, y1,
			delete_original,
			search_for_substr,
			ignore_case_substr
		)
	if os.path.isfile(target):
		if is_image(target):
			return cut_image(
				target,
				x, x1,
				y, y1,
				delete_original
			)


def cli_cut(parser_args):
	target_path = get_raw_path(parser_args.target_path)
	x, x1 = parse_pixel_x(parser_args), parse_pixel_x1(parser_args)
	if x == MAX_PIXEL_COORDINATE:
		x1, x = x, x1
	if x > x1 and x1 != MAX_PIXEL_COORDINATE:
		x1, x = x, x1
	y, y1 = parse_pixel_y(parser_args), parse_pixel_y1(parser_args)
	if y == MAX_PIXEL_COORDINATE:
		y1, y = y, y1
	if y > y1 and y1 != MAX_PIXEL_COORDINATE:
		y1, y = y, y1
	delete_original = parse_delete_original(parser_args)
	search_for_substr = parse_search_for_substr(parser_args)
	ignore_case_substr = parse_ignore_case_substr(parser_args)
	return cut(
		target_path,
		x, x1,
		y, y1,
		delete_original,
		search_for_substr,
		ignore_case_substr
	)
