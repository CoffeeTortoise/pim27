import os

from PIL import Image

from ..validators import is_image

from ..transformators import get_raw_path


def show_image(image_path):
	with Image.open(image_path) as img:
		img.show()
	return image_path


def show(target):
	if os.path.isfile(target):
		if is_image(target):
			return show_image(target)


def cli_show(parser_args):
	target_path = get_raw_path(parser_args.target_path)
	return show(target_path)
