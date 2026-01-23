import os

from fstring import f

from PIL import Image

from ..decorators import info

from ..validators import (
	is_image,
	is_substr_in_str
)

from ..transformators import (
	get_raw_path,
	get_time_marked_line
)

from ..constants import (
	DEFAULT_KX,
	DEFAULT_KY,
	ALL_FORMATS_C
)

from ..argument_parser import (
	parse_kx,
	parse_ky,
	parse_width,
	parse_height,
	parse_keepw,
	parse_keeph,
	parse_delete_original,
	parse_search_for_substr,
	parse_ignore_case_substr
)


@info
def resize_image(
	in_path,
	width, height,
	keep_w, keep_h,
	delete_original
):
	dirname = os.path.dirname(in_path)
	bname = os.path.basename(in_path)
	out_name = get_time_marked_line(bname)
	out_path = os.path.join(
		dirname, f('resized_${out_name}')
	)
	with Image.open(in_path) as img:
		w, h = img.size
		if keep_w and not keep_h:
			kwh = 1. * w / h
			height = 1. * width / kwh
		if keep_h and not keep_w:
			khw = 1. * h / w
			width = 1. * height / khw
		kx = abs(1. * width / w)
		ky = abs(1. * height / h)
		res_w, res_h = int(w * kx), int(h * ky)
		resized = img.resize(
			(res_w, res_h),
			resample=Image.LANCZOS
		)
		resized.save(out_path)
	if delete_original:
		if os.path.isfile(out_path):
			os.remove(in_path)
			os.rename(out_path, in_path)
			return in_path
	return out_path


def resize_folder(
	folder,
	width, height,
	keep_w, keep_h,
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
				resize_image(
					filepath,
					width, height,
					keep_w, keep_h,
					delete_original
				)
			else:
				fp = filepath.lower() if ignore_case_substr else filepath
				if is_substr_in_str(search_for_substr, fp):
					resize_image(
						filepath,
						width, height,
						keep_w, keep_h,
						delete_original
					)


def resize(
	target,
	width, height,
	keep_w, keep_h,
	delete_original,
	search_for_substr,
	ignore_case_substr
):
	if os.path.isfile(target):
		if not is_image(target):
			return
		return resize_image(
			target,
			width, height,
			keep_w, keep_h,
			delete_original
		)
	if os.path.isdir(target):
		return resize_folder(
			target,
			width, height,
			keep_w, keep_h,
			delete_original,
			search_for_substr,
			ignore_case_substr
		)


@info
def scale_image(
	in_path,
	kx, ky,
	keep_w, keep_h,
	delete_original
):
	dirname = os.path.dirname(in_path)
	bname = os.path.basename(in_path)
	out_name = get_time_marked_line(bname)
	out_path = os.path.join(
		dirname, f('resized_${out_name}')
	)
	with Image.open(in_path) as img:
		w, h = img.size
		width, height = abs(w * kx), abs(h * ky)
		if keep_w and not keep_h:
			kwh = 1. * w / h
			height = 1. * width / kwh
		if keep_h and not keep_w:
			khw = 1. * h / w
			width = 1. * height / khw
		resized = img.resize(
			(int(width), int(height)),
			resample=Image.LANCZOS
		)
		resized.save(out_path)
	if delete_original:
		if os.path.isfile(out_path):
			os.remove(in_path)
			os.rename(out_path, in_path)
			return in_path
	return out_path


def scale_folder(
	folder,
	kx, ky,
	keep_w, keep_h,
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
				scale_image(
					filepath,
					kx, ky,
					keep_w, keep_h,
					delete_original
				)
			else:
				fp = filepath.lower() if ignore_case_substr else filepath
				if is_substr_in_str(search_for_substr, fp):
					scale_image(
						filepath,
						kx, ky,
						keep_w, keep_h,
						delete_original
					)


def scale(
	target,
	kx, ky,
	keep_w, keep_h,
	delete_original,
	search_for_substr,
	ignore_case_substr
):
	if os.path.isfile(target):
		if not is_image(target):
			return
		return scale_image(
			target,
			kx, ky,
			keep_w, keep_h,
			delete_original
		)
	if os.path.isdir(target):
		return scale_folder(
			target,
			kx, ky,
			keep_w, keep_h,
			delete_original,
			search_for_substr,
			ignore_case_substr
		)


def cli_resize(parser_args):
	target_path = get_raw_path(parser_args.target_path)
	width = parse_width(parser_args)
	height = parse_height(parser_args)
	keep_w = parse_keepw(parser_args)
	keep_h = parse_keeph(parser_args)
	delete_original = parse_delete_original(parser_args)
	search_for_substr = parse_search_for_substr(parser_args)
	ignore_case_substr = parse_ignore_case_substr(parser_args)
	kx, ky = parse_kx(parser_args), parse_ky(parser_args)
	if kx == DEFAULT_KX and ky == DEFAULT_KY:
		return resize(
			target_path,
			width, height,
			keep_w, keep_h,
			delete_original,
			search_for_substr,
			ignore_case_substr
		)
	return scale(
		target_path,
		kx, ky,
		keep_w, keep_h,
		delete_original,
		search_for_substr,
		ignore_case_substr
	)
