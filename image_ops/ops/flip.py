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
	parse_flip_mode,
	parse_delete_original,
	parse_search_for_substr,
	parse_ignore_case_substr
)


def flip_top_bottom(in_path, out_path):
	with Image.open(in_path) as img:
		flipped = img.transpose(Image.FLIP_TOP_BOTTOM)
		flipped.save(out_path)
	return out_path


def flip_left_right(in_path, out_path):
	with Image.open(in_path) as img:
		flipped = img.transpose(Image.FLIP_LEFT_RIGHT)
		flipped.save(out_path)
	return out_path


FLIP_MODES = {
	'top_bottom': flip_top_bottom,
	'left_right': flip_left_right
}


@info
def flip_image(in_path, flip_mode, delete_original):
	dirname = os.path.dirname(in_path)
	bname = os.path.basename(in_path)
	out_name = get_time_marked_line(bname)
	out_path = os.path.join(
		dirname, f('flipped_${flip_mode}_${out_name}')
	)
	FLIP_MODES[flip_mode](in_path, out_path)
	if delete_original:
		if os.path.isfile(out_path):
			os.remove(in_path)
			os.rename(out_path, in_path)
			return in_path
	return out_path


def flip_folder(
	folder,
	flip_mode,
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
				flip_image(filepath, flip_mode, delete_original)
			else:
				fp = filepath.lower() if ignore_case_substr else filepath
				if is_substr_in_str(search_for_substr, fp):
					flip_image(filepath, flip_mode, delete_original)


def flip(
	target,
	flip_mode,
	delete_original,
	search_for_substr,
	ignore_case_substr
):
	if flip_mode not in FLIP_MODES:
		return
	if os.path.isfile(target):
		if is_image(target):
			return flip_image(target, flip_mode, delete_original)
	if os.path.isdir(target):
		return flip_folder(
			target,
			flip_mode,
			delete_original,
			search_for_substr,
			ignore_case_substr
		)


def cli_flip(parser_args):
	target_path = get_raw_path(parser_args.target_path)
	flip_mode = parse_flip_mode(parser_args)
	delete_original = parse_delete_original(parser_args)
	search_for_substr = parse_search_for_substr(parser_args)
	ignore_case_substr = parse_ignore_case_substr(parser_args)
	return flip(
		target_path,
		flip_mode,
		delete_original,
		search_for_substr,
		ignore_case_substr
	)
