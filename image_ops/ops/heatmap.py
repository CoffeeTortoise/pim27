import os

from fstring import f

from PIL import (
	Image,
	ImageEnhance
)

from ..decorators import info

from ..validators import (
	is_image,
	is_substr_in_str
)

from ..constants import ALL_FORMATS_C

from ..transformators import (
	get_raw_path,
	get_time_marked_line
)

from ..argument_parser import (
	parse_delete_original,
	parse_search_for_substr,
	parse_ignore_case_substr
)


def create_heatmap(src_image, out_path):
	heatmap = src_image.convert('L')
	heatmap = heatmap.point(lambda p: p * 1.5)
	colored_heatmap = Image.new(
		src_image.mode, heatmap.size
	)
	for x in xrange(heatmap.width):
		for y in xrange(heatmap.height):
			cords = x, y
			value = heatmap.getpixel(cords)
			if value < 128:
				color = [0, int(value * 2), 255]
			else:
				color = [
					int((value - 128) * 2), 0, 0
				]
			if src_image.mode == 'RGBA':
				color.append(255)
			colored_heatmap.putpixel(cords, tuple(color))
	enhancer = ImageEnhance.Contrast(colored_heatmap)
	res = enhancer.enhance(1.5)
	res.save(out_path)
	return out_path


@info
def heatmap_image(in_path, delete_original):
	dirname, bname = os.path.split(in_path)
	out_name = get_time_marked_line(bname)
	out_path = os.path.join(
		dirname, f('heatmap_${out_name}')
	)
	with Image.open(in_path) as img:
		create_heatmap(img, out_path)
	if delete_original:
		if os.path.isfile(out_path):
			os.remove(in_path)
			os.rename(out_path, in_path)
			return in_path
	return out_path


def heatmap_folder(
	folder,
	delete_original,
	search_for_substr,
	ignore_case_substr
):
	if ignore_case_substr:
		search_for_substr = search_for_substr.lower()
	for root, dirs, files in os.walk(folder):
		for f in files:
			if not is_image(f):
				continue
			filepath = os.path.join(root, f)
			if search_for_substr == ALL_FORMATS_C:
				heatmap_image(filepath, delete_original)
			else:
				fp = filepath.lower() if ignore_case_substr else filepath
				if is_substr_in_str(search_for_substr, fp):
					heatmap_image(filepath, delete_original)


def heatmap(
	target,
	delete_original,
	search_for_substr,
	ignore_case_substr
):
	if os.path.isfile(target):
		if is_image(target):
			return heatmap_image(target, delete_original)
	if os.path.isdir(target):
		return heatmap_folder(
			target,
			delete_original,
			search_for_substr,
			ignore_case_substr
		)


def cli_heatmap(parser_args):
	target_path = get_raw_path(parser_args.target_path)
	delete_original = parse_delete_original(parser_args)
	search_for_substr = parse_search_for_substr(parser_args)
	ignore_case_substr = parse_ignore_case_substr(parser_args)
	return heatmap(
		target_path,
		delete_original,
		search_for_substr,
		ignore_case_substr
	)
