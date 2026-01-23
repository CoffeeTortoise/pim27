import time

from collections import OrderedDict

from fstring import f

from .constants import CACHE_FILL_K


def cached(cache_size):
	cache = OrderedDict()

	def store(func):

		def wrapper(*args, **kwargs):
			key = hash(args) + hash(tuple(kwargs))
			if key in cache:
				return cache[key]
			if len(cache) >= cache_size:
				diff = cache_size - int(cache_size * CACHE_FILL_K)
				for _ in xrange(diff):
					cache.popitem(last=False)
			cache[key] = func(*args, **kwargs)
			return cache[key]
		return wrapper
	return store


def info(func):

	def wrapper(*args, **kwargs):
		fname, fp = func.__name__, args[0]
		try:
			start = time.time()
			res = func(*args, **kwargs)
			end = time.time()
			dt = end - start
			print f('Function ${fname} processed file ${fp} in ${round(dt, 4)} seconds.\nResult: ${res}\n')
		except Exception as e:
			print f('Function ${fname} failed to process file ${fp}.\nReason:\n\t${str(e)}\n')
		else:
			return res
	return wrapper
