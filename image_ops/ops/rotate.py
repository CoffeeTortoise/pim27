import os

from fstring import f

from PIL import Image

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
	parse_rotate_degree,
	parse_delete_original,
	parse_search_for_substr,
	parse_ignore_case_substr
)


@info
def rotate_image(in_path, degrees, delete_original):
	dirname = os.path.dirname(in_path)
	bname = os.path.basename(in_path)
	out_name = get_time_marked_line(bname)
	res_path = os.path.join(
		dirname, f('rotated_${degrees}_${out_name}')
	)
	with Image.open(in_path) as img:
		rotated = img.rotate(degrees, expand=True)
		rotated.save(res_path)
	if delete_original:
		if os.path.isfile(res_path):
			os.remove(in_path)
			os.rename(res_path, in_path)
			return in_path
	return res_path


def rotate_folder(
	folder,
	degrees,
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
				rotate_image(filepath, degrees, delete_original)
			else:
				fp = filepath.lower() if ignore_case_substr else filepath
				if is_substr_in_str(search_for_substr, fp):
					rotate_image(filepath, degrees, delete_original)


def rotate(
	target,
	degrees,
	delete_original,
	search_for_substr,
	ignore_case_substr
):
	if os.path.isfile(target):
		if is_image(target):
			return rotate_image(target, degrees, delete_original)
	if os.path.isdir(target):
		return rotate_folder(
			target,
			degrees,
			delete_original,
			search_for_substr,
			ignore_case_substr
		)


def cli_rotate(parser_args):
	target = get_raw_path(parser_args.target_path)
	rotate_degree = parse_rotate_degree(parser_args)
	delete_original = parse_delete_original(parser_args)
	search_for_substr = parse_search_for_substr(parser_args)
	ignore_case_substr = parse_ignore_case_substr(parser_args)
	return rotate(
		target,
		rotate_degree,
		delete_original,
		search_for_substr,
		ignore_case_substr
	)
