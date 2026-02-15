import os

import sys

import time

from fstring import f


ME = sys.executable

MY_NAME = (
	os.path.basename(ME)
	.strip()
	.split(os.extsep)
)[-2].strip()

CWD = os.path.dirname(ME) if hasattr(sys, 'frozen') else os.getcwd()

AVAILABLE_FORMATS = set(
	[
		'png', 'jpg', 'jpeg',
		'bmp', 'ico', 'tiff',
		'tif', 'tga', 'webp'
	]
)

RGBA_FORMATS = set(
	[
		'png', 'tiff', 'tif',
		'tga', 'webp'
	]
)

BUILD_DAY = '14 February, 2026'

TODAY = time.ctime(time.time())

MIN_RARITY = 0

MAX_RARITY = 10000

DEFAULT_RARITY = MAX_RARITY

ASCII_CODE_MAX = 126

ASCII_CODE_MIN = 32

ASCII_TXT_FOLDER = f('${MY_NAME}_ascii_txt_out_files')

ASCII_IMAGE_OUT_FORMAT = 'png'

ASCII_TXT_OUT_FORMAT = 'txt'

ALL_FORMATS_C = '*'

CACHE_FILL_K = .9

MAX_CACHE_SIZE = 256

OPS_SEPARATOR = ','

DEFAULT_FORMAT = 'png'

DEFAULT_DELETE_ORIGINAL = 0

DEFAULT_PIXEL_COLOR = 0, 0, 0, 255

MIN_PIXEL_COORDINATE = 0

MAX_PIXEL_COORDINATE = -1

PIXEL_COLOR_SEP = ','

DO_NOT_CHANGE_COLOR = 'XXXX'

DEFAULT_PIXEL_X = MIN_PIXEL_COORDINATE

DEFAULT_PIXEL_Y = MIN_PIXEL_COORDINATE

DEFAULT_PIXEL_X1 = MAX_PIXEL_COORDINATE

DEFAULT_PIXEL_Y1 = MAX_PIXEL_COORDINATE

DEFAULT_KX = -999

DEFAULT_KY = -999

JPG_OPTIMIZE = True

JPG_PROGRESSIVE = True

JPG_QUALITY = 99

PNG_COMPRESS = 9

WEBP_QUALITY = 100

WEBP_LOSSLESS = True

WEBP_PROGRESSIVE = True

DEFAULT_COLOR_TOOL = 'invert'

DEFAULT_FLIP_MODE = 'left_right'

DEFAULT_ENHANCE_MODE = 'contrast'

DEFAULT_ENHANCE_FACTOR = 1

DEFAULT_ROTATE_DEGREE = 0

DEFAULT_CHAR_W = 10

DEFAULT_CHAR_H = 11

DEFAULT_KEEP_W = 0

DEFAULT_KEEP_H = 0

DEFAULT_IGNORE_CASE = 0
