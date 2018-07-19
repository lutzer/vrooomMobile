import argparse
import math

from pythonosc import dispatcher
from pythonosc import osc_server

import xgboost as xgb
import numpy as np

OSC_LISTENER = "127.0.0.1"
OSC_PORT = 6449

bst = xgb.Booster()

def print_input_handler(unused_addr, *args):
	try:
		# print(len(args))
		data = np.array(args).reshape(1,1600)
		input = xgb.DMatrix(data)
		prediction = bst.predict(input)
		print(prediction)
	except ValueError: pass

if __name__ == "__main__":

	once = False

	# load model
	bst.load_model('bst.model')

	# listen to processing
	dispatcher = dispatcher.Dispatcher()
	dispatcher.map("/wek/inputs", print_input_handler)

	# start osc server
	server = osc_server.ThreadingOSCUDPServer(
		(OSC_LISTENER, OSC_PORT), dispatcher)
	print("Serving on {}".format(server.server_address))
	server.serve_forever()
