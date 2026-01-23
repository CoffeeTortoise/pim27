import os

from fstring import f

from PIL import Image

from ..decorators import info

from ..validators import (
	is_image,
	is_image_rgba,
	is_substr_in_str
)

from ..transformators import (
	get_raw_path,
	rename_if_misspelled
)

from ..constants import (
	DEFAULT_FORMAT,
	ALL_FORMATS_C,
	JPG_QUALITY,
	JPG_OPTIMIZE,
	JPG_PROGRESSIVE,
	PNG_COMPRESS,
	WEBP_QUALITY,
	WEBP_LOSSLESS,
	WEBP_PROGRESSIVE
)

from ..argument_parser import (
	parse_result_format,
	parse_target_format,
	parse_delete_original,
	parse_search_for_substr,
	parse_ignore_case_substr
)


@info
def convert_image(
	in_path,
	res_format,
	delete_original
):
	i = in_path.rfind(os.extsep)
	if res_format == ALL_FORMATS_C:
		res_format = DEFAULT_FORMAT
	result_path = f('${in_path[: i]}.${res_format}')
	if os.path.isfile(result_path):
		return result_path
	in_path = rename_if_misspelled(in_path, i)
	with Image.open(in_path) as img:
		if is_image_rgba(result_path):
			img = img.convert('RGBA')
		else:
			img = img.convert('RGB')
		if res_format == 'jpg':
			img.save(
				result_path,
				quality=JPG_QUALITY,
				progressive=JPG_PROGRESSIVE,
				optimize=JPG_OPTIMIZE
			)
		elif res_format == 'webp':
			img.save(
				result_path,
				quality=WEBP_QUALITY,
				progressive=WEBP_PROGRESSIVE,
				lossless=WEBP_LOSSLESS
			)
		elif res_format == 'png':
			img.save(
				result_path,
				compress_level=PNG_COMPRESS
			)
		else:
			img.save(result_path)
	if delete_original:
		if os.path.isfile(result_path):
			os.remove(in_path)
	return result_path


def convert_folder(
	folder,
	target_format,
	res_format,
	delete_original,
	search_for_substr,
	ignore_case_substr
):
	if ignore_case_substr:
		search_for_substr = search_for_substr.lower()
	for root, dirs, files in os.walk(folder):
		for f in files:
			ext = is_image(f)
			if not ext:
				continue
			filepath = os.path.join(root, f)
			fp = filepath.lower() if ignore_case_substr else filepath
			if search_for_substr != ALL_FORMATS_C and not is_substr_in_str(search_for_substr, fp):
				continue
			if target_format == ALL_FORMATS_C:
				convert_image(filepath, res_format, delete_original)
			else:
				if ext == target_format:
					convert_image(filepath, res_format, delete_original)


def convert(
	target_path,
	target_format,
	res_format,
	delete_original,
	search_for_substr,
	ignore_case_substr
):
	if os.path.isfile(target_path):
		if is_image(target_path):
			return convert_image(target_path, res_format, delete_original)
	if os.path.isdir(target_path):
		return convert_folder(
			target_path,
			target_format,
			res_format,
			delete_original,
			search_for_substr,
			ignore_case_substr
		)


def cli_convert(parser_args):
	target_path = get_raw_path(parser_args.target_path)
	target_format = parse_target_format(parser_args)
	result_format = parse_result_format(parser_args)
	delete_original = parse_delete_original(parser_args)
	search_for_substr = parse_search_for_substr(parser_args)
	ignore_case_substr = parse_ignore_case_substr(parser_args)
	return convert(
		target_path,
		target_format,
		result_format,
		delete_original,
		search_for_substr,
		ignore_case_substr
	)
