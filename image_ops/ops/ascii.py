import os

from fstring import f

from PIL import (
	Image,
	ImageDraw,
	ImageFont
)

from ..validators import (
	is_image,
	is_substr_in_str
)

from ..decorators import info

from ..constants import (
	ALL_FORMATS_C,
	PNG_COMPRESS,
	ASCII_CODE_MIN,
	ASCII_CODE_MAX,
	ASCII_TXT_FOLDER,
	ASCII_TXT_OUT_FORMAT,
	ASCII_IMAGE_OUT_FORMAT
)

from ..transformators import (
	get_raw_path,
	get_time_marked_line
)

from ..argument_parser import (
	parse_char_w,
	parse_char_h,
	parse_delete_original,
	parse_search_for_substr,
	parse_ignore_case_substr
)


def rgba_to_ascii(pixel):
	r, g, b, a = pixel
	brightness = .299 * r + .587 * g + .114 * b
	code = min(ASCII_CODE_MAX, int(brightness / (1. * 255 / ASCII_CODE_MAX)))
	code = int(code * 1. * a / 255)
	return chr(max(ASCII_CODE_MIN, code))


def get_ascii_matrix(image_path):
	with Image.open(image_path, mode='r') as image:
		if image.mode != 'RGBA':
			image = image.convert('RGBA')
		matrix = [[' ' for x in xrange(image.width)] for y in xrange(image.height)]
		pixels = list(image.getdata())
		for y in xrange(image.height):
			for x in xrange(image.width):
				pixel_index = y * image.width + x
				matrix[y][x] = rgba_to_ascii(pixels[pixel_index])
	return matrix


def create_ascii_txt(image_path):
	txt_folder = os.path.join(
		os.path.dirname(image_path), ASCII_TXT_FOLDER
	)
	if not os.path.exists(txt_folder):
		os.makedirs(txt_folder)
	bname = os.path.basename(image_path)
	i = bname.rfind(os.extsep)
	out_name = f('${bname[: i]}${os.extsep}${ASCII_TXT_OUT_FORMAT}')
	out_file = os.path.join(txt_folder, out_name)
	ascii_matrix = get_ascii_matrix(image_path)
	with open(out_file, 'w') as fi:
		fi.write('\n'.join(''.join(line) for line in ascii_matrix))
	return out_file


def create_ascii_image(txt_path, font, char_w, char_h):
	dirname = os.path.dirname(txt_path)
	timed_bname = get_time_marked_line(
		os.path.basename(txt_path)
	)
	out_name = (
		f('ascii_${timed_bname}')
		.replace(
			f('${os.extsep}${ASCII_TXT_OUT_FORMAT}'),
			f('${os.extsep}${ASCII_IMAGE_OUT_FORMAT}')
		)
	).strip()
	out_file = (
		os.path.join(dirname, out_name)
		.replace(
			f('${ASCII_TXT_FOLDER}${os.sep}'), ''
		)
	)
	with open(txt_path, 'r') as fi:
		ascii_art = fi.readlines()
	orig_w, orig_h = len(ascii_art[0]), len(ascii_art)
	img_w = int(orig_w * char_w)
	img_h = int(orig_h * char_h)
	img = Image.new('1', (img_w, img_h), 1)
	draw = ImageDraw.Draw(img)
	for y, line in enumerate(ascii_art):
		for x, char in enumerate(line):
			if char:
				draw.text((x * char_w, y * char_h), char, fill=0, font=font)
	if img.mode != 'RGBA':
		img = img.convert('RGBA')
	resized = img.resize(
		(orig_w, orig_h),
		resample=Image.LANCZOS
	)
	resized.save(
		out_file,
		compress_level=PNG_COMPRESS
	)
	return out_file


@info
def ascii_image(
	in_path,
	font,
	char_w, char_h,
	delete_original
):
	i = in_path.rfind(os.extsep)
	ext = in_path[i + 1: ]
	if ext != ASCII_TXT_OUT_FORMAT and not is_image(in_path):
		return
	if ext == ASCII_TXT_OUT_FORMAT:
		return create_ascii_image(txt_file, font, char_w, char_h)
	txt_file = create_ascii_txt(in_path)
	out_path = create_ascii_image(txt_file, font, char_w, char_h)
	if delete_original:
		if os.path.isfile(out_path):
			os.remove(in_path)
			os.rename(out_path, in_path)
			return in_path
	return out_path


def ascii_folder(
	folder,
	font,
	char_w, char_h,
	delete_original,
	search_for_substr,
	ignore_case_substr
):
	if ignore_case_substr:
		search_for_substr = search_for_substr.lower()
	for root, dirs, files in os.walk(folder):
		for f in files:
			filepath = os.path.join(root, f)
			if ASCII_TXT_FOLDER in filepath:
				continue
			if search_for_substr == ALL_FORMATS_C:
				ascii_image(
					filepath,
					font,
					char_w, char_h,
					delete_original
				)
			else:
				fp = filepath.lower() if ignore_case_substr else filepath
				if is_substr_in_str(search_for_substr, fp):
					ascii_image(
						filepath,
						font,
						char_w, char_h,
						delete_original
					)


def ascii(
	target,
	font,
	char_w, char_h,
	delete_original,
	search_for_substr,
	ignore_case_substr
):
	if os.path.isfile(target):
		return ascii_image(
			target,
			font,
			char_w, char_h,
			delete_original
		)
	if os.path.isdir(target):
		return ascii_folder(
			target,
			font,
			char_w, char_h,
			delete_original,
			search_for_substr,
			ignore_case_substr
		)


def cli_ascii(parser_args):
	target_path = get_raw_path(parser_args.target_path)
	char_w = parse_char_w(parser_args)
	char_h = parse_char_h(parser_args)
	if parser_args.fnt_path is None or get_raw_path(parser_args.fnt_path) == ALL_FORMATS_C:
		font = ImageFont.load_default()
	else:
		fnt_path = get_raw_path(parser_args.fnt_path)
		font = ImageFont.truetype(fnt_path, size=char_h)
	delete_original = parse_delete_original(parser_args)
	search_for_substr = parse_search_for_substr(parser_args)
	ignore_case_substr = parse_ignore_case_substr(parser_args)
	return ascii(
		target_path,
		font,
		char_w, char_h,
		delete_original,
		search_for_substr,
		ignore_case_substr
	)
