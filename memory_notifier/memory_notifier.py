# -*- coding: utf-8 -*-
#! /usr/bin/python3

import time, logging, pathlib, argparse, urllib, json
import http.client as hcl

app_name = pathlib.Path(__file__).stem
logging_format = f"%(asctime)s [%(levelname)s:%(name)s] - %(message)s -> %(pathname)s, line %(lineno)d, in %(funcName)s"
logger = logging.getLogger(app_name)

def memory_in_percent(numerator='MemAvailable:', denominator='MemTotal:'):
	with open('/proc/meminfo') as fd:
		while True:
			fd.seek(0)
			for ln in fd:
				if numerator in ln:
					num = ln.split()
				elif denominator in ln:
					den = ln.split()
			assert num[2] == den[2]
			yield 100 * int(num[1]) / int(den[1])

def main(args):
	logging_level = logging.DEBUG if args.verbose else logging.WARNING
	logging.basicConfig( level=logging_level, format=logging_format)			# Logging configuration
	url = urllib.parse.urlsplit(args.url)									# Split url
	g_mem = iter(memory_in_percent())
	while True:
		memory_use_percent = 100 - next(g_mem)						# Memory usage as a percentage
		if memory_use_percent > args.threshold:
			msg = f'{memory_use_percent}% memory usage detected!'			# Notification message
			try:
				connection = hcl.HTTPConnection(url.netloc)
				connection.request('PUT', url.path, 
					json.dumps({'message': msg}),
					{'Content-type': 'application/json'} )				# Sending an HTTP request to the API
			except (ConnectionError, hcl.HTTPException, OSError):
				logger.exception(msg)
			else:
				logger.info(f'{msg}, {connection.getresponse().read()}')
				connection.close()
		else:
			logger.info(f'Normal memory usage detected! {memory_use_percent}')
		time.sleep(args.interval)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog=app_name, description='Memory usage HTTP notifier', epilog=f'For more details see {app_name}(1).')
	parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Be verbose')
	parser.add_argument('-t', '--threshold', metavar='%', type=float, default=10, help='Percentage memory usage threshold for sending a notification')
	parser.add_argument('-i', '--interval', metavar='<secs>', type=int, default=10, help='Interval for checking the amount of memory used')
	parser.add_argument('url', nargs='?', type=str, default='http://localhost:8080/memory/use', help='Notification URL')
	try:
		main(parser.parse_args())
	except KeyboardInterrupt:
		pass
	
