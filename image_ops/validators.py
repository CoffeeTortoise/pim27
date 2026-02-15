import os

from .constants import (
	RGBA_FORMATS,
	AVAILABLE_FORMATS,
	MAX_CACHE_SIZE,
	ALL_FORMATS_C
)

from .decorators import cached


@cached(MAX_CACHE_SIZE)
def is_image(filepath):
	i = filepath.rfind(os.extsep)
	ext = filepath[i + 1: ].lower().strip()
	if ext in AVAILABLE_FORMATS:
		return ext
	return ''


@cached(MAX_CACHE_SIZE)
def is_image_rgba(filepath):
	i = filepath.rfind(os.extsep)
	ext = filepath[i + 1: ].lower().strip()
	if ext in RGBA_FORMATS:
		return ext
	return ''


@cached(MAX_CACHE_SIZE)
def is_substr_in_str(substr, str_):
	if ALL_FORMATS_C in substr:
		return all(
			part in str_
			for part in substr.split(ALL_FORMATS_C)
			if part
		)
	return substr in str_
