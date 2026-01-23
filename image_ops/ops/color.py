import os

from fstring import f

from PIL import (
	Image,
	ImageFilter,
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
	parse_color_tool,
	parse_delete_original,
	parse_search_for_substr,
	parse_ignore_case_substr
)


def invert(in_path, out_path):
	with Image.open(in_path) as img:
		inverted = Image.eval(img, lambda x: 255 - x)
		inverted.save(out_path)
	return out_path


def gray(in_path, out_path):
	with Image.open(in_path) as img:
		gray = img.convert('L')
		gray.save(out_path)
	return out_path


def blur(in_path, out_path):
	with Image.open(in_path) as img:
		w, h = img.size
		r = max(1, int(0.05 * w), int(0.05 * h))
		blur = img.filter(ImageFilter.BoxBlur(radius=r))
		blur.save(out_path)
	return out_path


def sharp(in_path, out_path):
	with Image.open(in_path) as img:
		sharp = img.filter(ImageFilter.SHARPEN)
		sharp.save(out_path)
	return out_path


def smooth(in_path, out_path):
	with Image.open(in_path) as img:
		smooth = img.filter(ImageFilter.SMOOTH)
		smooth.save(out_path)
	return out_path


def uncanny(in_path, out_path):
	with Image.open(in_path) as img:
		enhancer = ImageEnhance.Contrast(img)
		img = enhancer.enhance(2.1)
		enhancer = ImageEnhance.Brightness(img)
		img = enhancer.enhance(.6)
		img = img.filter(ImageFilter.BLUR)
		img.save(out_path)
	return out_path


def contours(in_path, out_path):
	with Image.open(in_path) as img:
		gray = img.convert('L')
		edges = gray.filter(ImageFilter.FIND_EDGES)
		inv = Image.eval(edges, lambda x: 255 - x)
		inv.save(out_path)
	return out_path


def black_white1(in_path, out_path):
	with Image.open(in_path) as img:
		gray = img.convert('L')
		threshold = 109
		bw_img = gray.point(lambda x: 255 if x < threshold else 0)
		bw_img.save(out_path)
	return out_path


def black_white2(in_path, out_path):
	with Image.open(in_path) as img:
		gray = img.convert('L')
		threshold = 114
		bw_img = gray.point(lambda x: 255 if x > threshold else 0)
		bw_img.save(out_path)
	return out_path


def gray_emboss(in_path, out_path):
	with Image.open(in_path) as img:
		gray = img.convert('L')
		gray_smooth = gray.filter(ImageFilter.SMOOTH)
		embossed = gray_smooth.filter(ImageFilter.EMBOSS)
		enhancer = ImageEnhance.Contrast(embossed)
		enhanced = enhancer.enhance(3)
		sharpened = enhanced.filter(ImageFilter.SHARPEN)
		sharpened.save(out_path)
	return out_path


def one_bit(in_path, out_path):
	with Image.open(in_path) as img:
		bit = img.convert('1')
		bit.save(out_path)
	return out_path


def eight_bit(in_path, out_path):
	with Image.open(in_path) as img:
		bit = img.convert('P')
		bit.save(out_path)
	return out_path


TOOLS = {
	'invert': invert,
	'gray': gray,
	'blur': blur,
	'sharp': sharp,
	'smooth': smooth,
	'uncanny': uncanny,
	'contours': contours,
	'one_bit': one_bit,
	'eight_bit': eight_bit,
	'black_white1': black_white1,
	'black_white2': black_white2,
	'gray_emboss': gray_emboss
}


@info
def color_image(in_path, tool, delete_original):
	dirname = os.path.dirname(in_path)
	bname = os.path.basename(in_path)
	out_name = get_time_marked_line(bname)
	out_path = os.path.join(
		dirname, f('colored_${tool}_${out_name}')
	)
	TOOLS[tool](in_path, out_path)
	if delete_original:
		if os.path.isfile(out_path):
			os.remove(in_path)
			os.rename(out_path, in_path)
			return in_path
	return out_path


def color_folder(
	folder,
	tool,
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
				color_image(filepath, tool, delete_original)
			else:
				fp = filepath.lower() if ignore_case_substr else filepath
				if is_substr_in_str(search_for_substr, fp):
					color_image(filepath, tool, delete_original)


def color(
	target,
	tool,
	delete_original,
	search_for_substr,
	ignore_case_substr
):
	if tool not in TOOLS:
		return
	if os.path.isfile(target):
		if is_image(target):
			return color_image(target, tool, delete_original)
	if os.path.isdir(target):
		return color_folder(
			target,
			tool,
			delete_original,
			search_for_substr,
			ignore_case_substr
		)


def cli_color(parser_args):
	target_path = get_raw_path(parser_args.target_path)
	color_tool = parse_color_tool(parser_args)
	delete_original = parse_delete_original(parser_args)
	search_for_substr = parse_search_for_substr(parser_args)
	ignore_case_substr = parse_ignore_case_substr(parser_args)
	return color(
		target_path,
		color_tool,
		delete_original,
		search_for_substr,
		ignore_case_substr
	)
