import os

from fstring import f

from PIL import (
	Image,
	ImageEnhance
)


from ..constants import ALL_FORMATS_C

from ..validators import (
	is_image,
	is_substr_in_str
)

from ..decorators import info

from ..transformators import (
	get_raw_path,
	get_time_marked_line
)

from ..argument_parser import (
	parse_enhance_mode,
	parse_enhance_factor,
	parse_delete_original,
	parse_search_for_substr,
	parse_ignore_case_substr
)


ENHANCERS = {
	'brightness': lambda i: ImageEnhance.Brightness(i),
	'contrast': lambda i: ImageEnhance.Contrast(i),
	'color': lambda i: ImageEnhance.Color(i),
	'sharpness': lambda i: ImageEnhance.Sharpness(i)
}


@info
def enhance_image(in_path, mode, factor, delete_original):
	dirname, bname = os.path.split(in_path)
	out_name = get_time_marked_line(bname)
	out_path = os.path.join(
		dirname, f('enhanced_${mode}_${out_name}')
	)
	with Image.open(in_path) as img:
		enhancer = ENHANCERS[mode](img)
		enhanced = enhancer.enhance(factor)
		enhanced.save(out_path)
	if delete_original:
		if os.path.exists(out_path):
			os.remove(in_path)
			os.rename(out_path, in_path)
			return in_path
	return out_path


def enhance_folder(
	folder,
	mode,
	factor,
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
				enhance_image(filepath, mode, factor, delete_original)
			else:
				fp = filepath.lower() if ignore_case_substr else filepath
				if is_substr_in_str(search_for_substr, fp):
					enhance_image(filepath, mode, factor, delete_original)


def enhance(
	target,
	mode,
	factor,
	delete_original,
	search_for_substr,
	ignore_case_substr
):
	if mode not in ENHANCERS:
		return
	if os.path.isfile(target):
		if is_image(target):
			return enhance_image(target, mode, factor, delete_original)
	if os.path.isdir(target):
		return enhance_folder(
			target,
			mode,
			factor,
			delete_original,
			search_for_substr,
			ignore_case_substr
		)


def cli_enhance(parser_args):
	target_path = get_raw_path(parser_args.target_path)
	mode = parse_enhance_mode(parser_args)
	factor = parse_enhance_factor(parser_args)
	delete_original = parse_delete_original(parser_args)
	search_for_substr = parse_search_for_substr(parser_args)
	ignore_case_substr = parse_ignore_case_substr(parser_args)
	return enhance(
		target_path,
		mode,
		factor,
		delete_original,
		search_for_substr,
		ignore_case_substr
	)
