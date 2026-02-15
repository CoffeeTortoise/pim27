import os

from fstring import f

from PIL import Image

from random import randint

from ..decorators import info

from ..validators import (
	is_image,
	is_substr_in_str
)

from ..constants import (
	MIN_RARITY,
	MAX_RARITY,
	ALL_FORMATS_C
)

from ..transformators import (
	get_raw_path,
	get_time_marked_line
)

from ..argument_parser import (
	parse_rarity,
	parse_color_filler,
	parse_delete_original,
	parse_search_for_substr,
	parse_ignore_case_substr
)


def create_rarefacted(
	src_image,
	rarity,
	color_filler,
	out_path
):
	cofi = list(color_filler)
	if src_image.mode == 'RGBA' and len(cofi) < 4:
		cofi.append(255)
	if src_image.mode == 'RGB' and len(cofi) > 3:
		cofi = cofi[: 3]
	color_filler = tuple(cofi)
	rarefacted = Image.new(
		src_image.mode, src_image.size
	)
	for x in xrange(src_image.width):
		for y in xrange(src_image.height):
			cords = x, y
			n = randint(MIN_RARITY, MAX_RARITY)
			if n >= MIN_RARITY and n <= rarity:
				value = src_image.getpixel(cords)
				rarefacted.putpixel(cords, value)
			else:
				rarefacted.putpixel(cords, color_filler)
	rarefacted.save(out_path)
	return out_path


@info
def rarefaction_image(
	in_path,
	rarity,
	color_filler,
	delete_original
):
	dirname, bname = os.path.split(in_path)
	out_name = get_time_marked_line(bname)
	out_path = os.path.join(
		dirname, f('rarefaction_${out_name}')
	)
	with Image.open(in_path) as img:
		create_rarefacted(
			img, rarity, color_filler, out_path
		)
	if delete_original:
		if os.path.isfile(out_path):
			os.remove(in_path)
			os.rename(out_path, in_path)
			return in_path
	return out_path


def rarefaction_folder(
	folder,
	rarity,
	color_filler,
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
				rarefaction_image(
					filepath, rarity, color_filler, delete_original
				)
			else:
				fp = filepath.lower() if ignore_case_substr else filepath
				if is_substr_in_str(search_for_substr, fp):
					rarefaction_image(
						filepath, rarity, color_filler, delete_original
					)


def rarefaction(
	target,
	rarity,
	color_filler,
	delete_original,
	search_for_substr,
	ignore_case_substr
):
	if os.path.isfile(target):
		if is_image(target):
			return rarefaction_image(
				target, rarity, color_filler, delete_original
			)
	if os.path.isdir(target):
		return rarefaction_folder(
			target,
			rarity,
			color_filler,
			delete_original,
			search_for_substr,
			ignore_case_substr
		)


def cli_rarefaction(parser_args):
	target_path = get_raw_path(parser_args.target_path)
	delete_original = parse_delete_original(parser_args)
	search_for_substr = parse_search_for_substr(parser_args)
	ignore_case_substr = parse_ignore_case_substr(parser_args)
	rarity = parse_rarity(parser_args)
	color_filler = parse_color_filler(parser_args)
	return rarefaction(
		target_path,
		rarity,
		color_filler,
		delete_original,
		search_for_substr,
		ignore_case_substr
	)
