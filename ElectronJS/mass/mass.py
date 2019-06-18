## System modules
import sys, json, os
from pathlib import Path as pt
import traceback

## Data analysis
import numpy as np

def main(*args):
	try:
		received_files = args[0][0].split(',')
		mass, counts = [], []

		for filepath in received_files:
			massfile = pt(filepath)
			mass_temp, counts_temp = np.genfromtxt(massfile).T

			mass.append(mass_temp)
			counts.append(counts_temp)

		mass = np.array(mass, dtype=np.float).tolist()
		counts = np.array(counts, dtype=np.float).tolist()

		data = dict(mass=mass, counts=counts, filename=massfile.stem)
		dataJson = json.dumps(data)
		print(dataJson)

	except Exception:
		err = traceback.format_exc()
		print(f"\nError occured:\n\n{err}\n\nEND FILE")

if __name__=="__main__":
	args = sys.argv[1:]
	main(args)