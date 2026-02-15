import os

import argparse

from fstring import f

from image_ops.constants import (
	BUILD_DAY,
	ALL_FORMATS_C,
	DEFAULT_KX,
	DEFAULT_KY,
	DEFAULT_FORMAT,
	DEFAULT_KEEP_W,
	DEFAULT_KEEP_H,
	DEFAULT_CHAR_W,
	DEFAULT_CHAR_H,
	OPS_SEPARATOR,
	MIN_RARITY,
	MAX_RARITY,
	DEFAULT_RARITY,
	ASCII_TXT_FOLDER,
	ASCII_TXT_OUT_FORMAT,
	ASCII_IMAGE_OUT_FORMAT,
	AVAILABLE_FORMATS,
	DEFAULT_FLIP_MODE,
	DEFAULT_COLOR_TOOL,
	DEFAULT_IGNORE_CASE,
	DEFAULT_ROTATE_DEGREE,
	DEFAULT_DELETE_ORIGINAL,
	DEFAULT_ENHANCE_MODE,
	DEFAULT_ENHANCE_FACTOR,
	DEFAULT_PIXEL_X,
	DEFAULT_PIXEL_X1,
	DEFAULT_PIXEL_Y,
	DEFAULT_PIXEL_Y1,
	PIXEL_COLOR_SEP,
	DEFAULT_PIXEL_COLOR,
	DO_NOT_CHANGE_COLOR,
	MAX_PIXEL_COORDINATE
)

from image_ops.argument_parser import parse_operation

from image_ops.ops.rarefaction import cli_rarefaction

from image_ops.ops.resize import cli_resize

from image_ops.ops.convert import cli_convert

from image_ops.ops.rotate import cli_rotate

from image_ops.ops.heatmap import cli_heatmap

from image_ops.ops.ascii import cli_ascii

from image_ops.ops.show import cli_show

from image_ops.ops.pixel import cli_pixel

from image_ops.ops.cut import cli_cut

from image_ops.ops.enhance import (
	ENHANCERS,
	cli_enhance
)

from image_ops.ops.color import (
	TOOLS,
	cli_color
)

from image_ops.ops.flip import (
	FLIP_MODES,
	cli_flip
)


OPS = {
	'rarefaction': cli_rarefaction,
	'heatmap': cli_heatmap,
	'convert': cli_convert,
	'resize': cli_resize,
	'color': cli_color,
	'rotate': cli_rotate,
	'pixel': cli_pixel,
	'flip': cli_flip,
	'ascii': cli_ascii,
	'enhance': cli_enhance,
	'show': cli_show,
	'cut': cli_cut
}

OPS_STR = ', '.join(OPS.keys())

FORMATS_STR = ', '.join(AVAILABLE_FORMATS)

COLOR_TOOLS_STR = ', '.join(TOOLS.keys())

FLIP_MODES_STR = ', '.join(FLIP_MODES.keys())

ENHANCE_MODES_STR = ', '.join(ENHANCERS.keys())

DEFAULT_PIXEL_COLOR_STR = PIXEL_COLOR_SEP.join(str(e) for e in DEFAULT_PIXEL_COLOR)


def test():

	test_dir = 'test_images'
	test_files = [
		os.path.join(test_dir, f) for f in os.listdir(test_dir)
	]
	test_file = '0.bmp'


def main():
	parser = argparse.ArgumentParser(
		description=f(
			'''
				cli-utility for doing some stuff with images.
				created ${BUILD_DAY} by CoffeeTortoise(https://github.com/CoffeeTortoise) using python27,
				just because I wanted cli-utility with Pillow library functionality.
			'''
		)
	)

	parser.add_argument(
		'-op', '--operation', type=str, required=True,
		help=f(
			'''
			Mode, operation(or group operations in brackets, where separator ${OPS_SEPARATOR}) with image.
			Not images are ignored.
			${ALL_FORMATS_C} means not specified.
			Available operations:\n\t${OPS_STR}. show operation shows only 1 image.
			Avaliable formats: ${FORMATS_STR}.
			Argument type: string.
			Arguments only for convert: target_format, result_format.
			Arguments only for resize: width, height, keep_w, keep_h, kx, ky.
			Arguments only for color: color_tool.
			Arguments only for flip: flip_mode.
			Arguments only for enhance: enhance_mode, enhance_factor.
			Arguments only for rotate: rotate_degree.
			Arguments only for pixel: color_from, color_to. Also pixel can be used for
			copying images.
			Arguments only for rarefaction: rarity(less rarity = more color filler pixels), color_filler.
			Arguments for pixel and cut: pixel_x, pixel_x1, pixel_y, pixel_y1.
			Arguments only for ascii: fnt_path, char_w, char_h. Also ascii can accept ${ASCII_TXT_OUT_FORMAT}
			format files as a target and output file always ${ASCII_IMAGE_OUT_FORMAT}. Also in ascii, paths
			which contain substring ${ASCII_TXT_FOLDER} are ingored(this folder is for mid-result ${ASCII_TXT_OUT_FORMAT} files).
			Arguments for resize, color, rotate and flip: search_for_substr, ignore_case_substr.
			'''
		)
	)

	parser.add_argument(
		'-tp', '--target_path', type=str, required=True,
		help=
		'''
		Path to the target. Target can be file or directory.
		Argument type: string.
		'''
	)

	parser.add_argument(
		'-ra', '--rarity', type=str, required=False,
		help=f(
			'''
			Rarity k. Value between ${MIN_RARITY} and ${MAX_RARITY} inclusive.
			By default: ${DEFAULT_RARITY}.
			Argument type: unsigned integer.
			'''
		)
	)

	parser.add_argument(
		'-em', '--enhance_mode', type=str, required=False,
		help=f(
			'''
			Enhance mode. Available modes: ${ENHANCE_MODES_STR}.
			By default: ${DEFAULT_ENHANCE_MODE}.
			Argument type: string.
			'''
		)
	)

	parser.add_argument(
		'-ef', '--enhance_factor', type=str, required=False,
		help=f(
			'''
			Just enhance factor. By default: ${DEFAULT_ENHANCE_FACTOR}.
			Argument type: float.
			'''
		)
	)

	parser.add_argument(
		'-do', '--delete_original', type=str, required=False,
		help=f(
			'''
			Determines what to do with the original: delete(1) or
			keep(0). By default: ${DEFAULT_DELETE_ORIGINAL}.
			Argument type: integer(0 or 1).
			'''
		)
	)

	parser.add_argument(
		'-sfs', '--search_for_substr', type=str, required=False,
		help=f(
			'''
			Specifies the substring, which target filepath must have.
			Substring can contain ${ALL_FORMATS_C}, in that case ${ALL_FORMATS_C}
			is a separator for group of substrings.
			By default: ${ALL_FORMATS_C}.
			Argument type: string.
			'''
		)
	)

	parser.add_argument(
		'-ics', '--ignore_case_substr', type=str, required=False,
		help=f(
			'''
			Determines, whether to ignore(1) case if search_for_substr specified or
			not (0). By default: ${DEFAULT_IGNORE_CASE}.
			Argument type: string.
			'''
		)
	)

	parser.add_argument(
		'-fnt', '--fnt_path', type=str, required=False,
		help=
		'''
		Path to the truetype font. If not specified, default font will be used.
		Argument type: string.
		'''
	)

	parser.add_argument(
		'-ct', '--color_tool', type=str, required=False,
		help=f(
			'''
			Tool which will be applied to the image.
			Available tools: ${COLOR_TOOLS_STR}. By default: ${DEFAULT_COLOR_TOOL}.
			Argument type: str.
			'''
		)
	)

	parser.add_argument(
		'-cw', '--char_w', type=str, required=False,
		help=f(
			'''
			Character width, positive.
			Default value: ${DEFAULT_CHAR_W}.
			Argument type: integer.
			'''
		)
	)

	parser.add_argument(
		'-ch', '--char_h', type=str, required=False,
		help=f(
			'''
			Character height, positive.
			Default value: ${DEFAULT_CHAR_H}.
			Argument type: integer.
			'''
		)
	)

	parser.add_argument(
		'-px', '--pixel_x', type=str, required=False,
		help=f(
			'''
			Start x position x, positive. Default value: ${DEFAULT_PIXEL_X}.
			${MAX_PIXEL_COORDINATE} means end.
			Argument type: integer.
			'''
		)
	)

	parser.add_argument(
		'-px1', '--pixel_x1', type=str, required=False,
		help=f(
			'''
			End x position x, positive. Default value: ${DEFAULT_PIXEL_X1}.
			${MAX_PIXEL_COORDINATE} means end.
			Argument type: integer.
			'''
		)
	)

	parser.add_argument(
		'-py', '--pixel_y', type=str, required=False,
		help=f(
			'''
			Start y position y, positive. Default value: ${DEFAULT_PIXEL_Y}.
			${MAX_PIXEL_COORDINATE} means end.
			Argument type: integer.
			'''
		)
	)

	parser.add_argument(
		'-py1', '--pixel_y1', type=str, required=False,
		help=f(
			'''
			End y position y, positive. Default value: ${DEFAULT_PIXEL_Y1}.
			${MAX_PIXEL_COORDINATE} means end.
			Argument type: integer.
			'''
		)
	)

	parser.add_argument(
		'-cof', '--color_from', type=str, required=False,
		help=f(
			'''
			RGB or RGBA initial color in brackets(example: (0,0,0) or (0,0,0,255)), where separator ${PIXEL_COLOR_SEP}.
			By default: ${DEFAULT_PIXEL_COLOR_STR}. If you don\'t want to change color, set it ${DO_NOT_CHANGE_COLOR}.
			Argument type: str or tuple of integers.
			'''
		)
	)

	parser.add_argument(
		'-cot', '--color_to', type=str, required=False,
		help=f(
			'''
			RGB or RGBA result color in brackets(example: (0,0,0) or (0,0,0,255)), where separator ${PIXEL_COLOR_SEP}.
			By default: ${DEFAULT_PIXEL_COLOR_STR}. If you don\'t want to change color, set it ${DO_NOT_CHANGE_COLOR}.
			Argument type: str or tuple of integers.
			'''
		)
	)

	parser.add_argument(
		'-cofi', '--color_filler', type=str, required=False,
		help=f(
			'''
			RGB or RGBA color in brackets(example: (0,0,0) or (0,0,0,255)), where separator ${PIXEL_COLOR_SEP}.
			By default: ${DEFAULT_PIXEL_COLOR_STR}.
			Argument type: str or tuple of integers.
			'''
		)
	)

	parser.add_argument(
		'-rd', '--rotate_degree', type=str, required=False,
		help=f(
			'''
			The angle in degrees by which the image will be rotated, absolute value
			between 0 and 360. By default: ${DEFAULT_ROTATE_DEGREE}.
			Argument type: float.
			'''
		)
	)

	parser.add_argument(
		'-fp', '--flip_mode', type=str, required=False,
		help=f(
			'''
			Mode in which image will be flipped. Available modes: ${FLIP_MODES_STR}.
			Default value: ${DEFAULT_FLIP_MODE}.
			Argument type: string.
			'''
		)
	)

	parser.add_argument(
		'-kx', type=str, required=False,
		help=f(
			'''
			Width k for scaling images.
			Default value: ${DEFAULT_KX}. If value default, will be ommited.
			Argument type: float.
			'''
		)
	)

	parser.add_argument(
		'-ky', type=str, required=False,
		help=f(
			'''
			Height k for scaling images.
			Default value: ${DEFAULT_KY}. If value default, will be ommited.
			Argument type: float.
			'''
		)
	)

	parser.add_argument(
		'-wi', '--width', type=str, required=False,
		help=
		'''
		Result width, can be ommited if keep_w=0.
		Argument type: integer(greater than 0).
		'''
	)

	parser.add_argument(
		'-he', '--height', type=str, required=False,
		help=
		'''
		Result height, can be ommited if keep_h=0.
		Argument type: integer(greater than 0).
		'''
	)

	parser.add_argument(
		'-kw', '--keep_w', type=str, required=False,
		help=f(
			'''
			Determines, whether to keep(1) the width to height
			ratio or not(0). Cannot be used if keep_h=1.
			Default value: ${DEFAULT_KEEP_W}.
			Argument type: integer(0 or 1).
			'''
		)
	)

	parser.add_argument(
		'-kh', '--keep_h', type=str, required=False,
		help=f(
			'''
			Determines, whether to keep(1) the height to width
			ratio or not(0). Cannot be used if keep_w=1.
			Default value: ${DEFAULT_KEEP_H}.
			Argument type: integer(0 or 1).
			'''
		)
	)

	parser.add_argument(
		'-tf', '--target_format', type=str, required=False,
		help=f(
			'''
			Target file extension. If target is a file, ignored.
			If not specified or ${ALL_FORMATS_C}, targets are
			all images. Argument type: string.
			'''
		)
	)

	parser.add_argument(
		'-rf', '--result_format', type=str, required=False,
		help=f(
			'''
			Result file extension. If not specified or
			${ALL_FORMATS_C}, result file extension will be
			${DEFAULT_FORMAT}. Argument type: str.
			'''
		)
	)

	args = parser.parse_args()
	for op in parse_operation(args):
		if op not in OPS:
			continue
		OPS[op](args)


if __name__ == '__main__':
	main()
