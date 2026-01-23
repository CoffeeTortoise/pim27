import os

from fstring import f

from PIL import Image

from ..validators import (
	is_image,
	is_substr_in_str
)

from ..constants import (
	ALL_FORMATS_C,
	DO_NOT_CHANGE_COLOR,
	MAX_PIXEL_COORDINATE
)

from ..transformators import (
	get_raw_path,
	get_time_marked_line
)

from ..argument_parser import (
	parse_color_to,
	parse_color_from,
	parse_pixel_x,
	parse_pixel_x1,
	parse_pixel_y,
	parse_pixel_y1,
	parse_delete_original,
	parse_search_for_substr,
	parse_ignore_case_substr
)

from ..decorators import info


def get_image_matrix(
	img,
	x, x1,
	y, y1,
	color_from, color_to
):
	if x1 == MAX_PIXEL_COORDINATE:
		x1 = img.width
	if y1 == MAX_PIXEL_COORDINATE:
		y1 = img.height
	pixels = list(img.getdata())
	if (
		color_from == DO_NOT_CHANGE_COLOR
		or
		color_to == DO_NOT_CHANGE_COLOR
	):
		return [
			[pixels[i * img.width + j] for j in xrange(img.width)] for i in xrange(img.height)
		]
	res = [[None for _ in xrange(img.width)] for _ in xrange(img.height)]
	for i in xrange(img.height):
		for j in xrange(img.width):
			pixel_index = i * img.width + j
			if pixels[pixel_index] == color_from and (j >= x and j < x1) and (i >= y and i < y1):
				res[i][j] = color_to
			else:
				res[i][j] = pixels[pixel_index]
	return res


def resize_color_tuple(mode, color):
	if color == DO_NOT_CHANGE_COLOR:
		return DO_NOT_CHANGE_COLOR
	if mode != 'RGBA':
		color = color[: 3]
	else:
		if len(color) == 3:
			cf = []
			cf.extend(color)
			cf.append(255)
			color = tuple(cf)
		if len(color) > 4:
			color = color[: 4]
	return color


@info
def pixel_image(
	in_path,
	x, x1,
	y, y1,
	color_from, color_to,
	delete_original
):
	dirname = os.path.dirname(in_path)
	basename = os.path.basename(in_path)
	oname = get_time_marked_line(basename)
	out_path = os.path.join(
		dirname, f('pixel_${oname}')
	)
	with Image.open(in_path) as img:
		img_mode = img.mode
		color_from = resize_color_tuple(img_mode, color_from)
		color_to = resize_color_tuple(img_mode, color_to)
		m = get_image_matrix(
			img,
			x, x1,
			y, y1,
			color_from, color_to
		)
	w, h = len(m[0]), len(m)
	res = Image.new(img_mode, (w, h))
	for y in xrange(h):
		for x in xrange(w):
			res.putpixel((x, y), m[y][x])
	res.save(out_path)
	if delete_original:
		if os.path.isfile(out_path):
			os.remove(in_path)
			os.rename(out_path, in_path)
			return in_path
	return out_path


def pixel_folder(
	target,
	x, x1,
	y, y1,
	color_from, color_to,
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
				pixel_image(
					filepath,
					x, x1,
					y, y1,
					color_from, color_to,
					delete_original
				)
			else:
				fp = filepath.lower() if ignore_case_substr else filepath
				if is_substr_in_str(search_for_substr, fp):
					pixel_image(
						filepath,
						x, x1,
						y, y1,
						color_from, color_to,
						delete_original
					)


def pixel(
	target,
	x, x1,
	y, y1,
	color_from, color_to,
	delete_original,
	search_for_substr,
	ignore_case_substr
):
	if os.path.isfile(target):
		if is_image(target):
			return pixel_image(
				target,
				x, x1,
				y, y1,
				color_from, color_to,
				delete_original
			)
	if os.path.isdir(target):
		return pixel_folder(
			target,
			x, x1,
			y, y1,
			color_from, color_to,
			delete_original,
			search_for_substr,
			ignore_case_substr
		)


def cli_pixel(parser_args):
	target_path = get_raw_path(parser_args.target_path)
	color_to = parse_color_to(parser_args)
	color_from = parse_color_from(parser_args)
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
	return pixel(
		target_path,
		x, x1,
		y, y1,
		color_from, color_to,
		delete_original,
		search_for_substr,
		ignore_case_substr
	)
