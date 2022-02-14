# %%
import csv
import datetime

import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
%matplotlib widget
# %matplotlib inline

def get_formatted_data(path: str):
	data: list[datetime.datetime, int] = []
	with open(path) as f:
		reader = csv.reader(f)
		reader.__next__()
		for row in reader:
			if not row[0]:
				continue

			date = row[0]
			tabs = int(row[1])


			formatted_date = datetime.datetime.strptime(date, '%B %d, %Y')
			# data.append([formatted_date.strftime('%d%m%y'), tabs])
			data.append([formatted_date, tabs])

	return data


def create_plot(data: list[datetime.datetime, int]):
	date = [d[0] for d in data]
	tabs = [d[1] for d in data]
	 
	# X_Y_Spline = make_interp_spline(date, tabs)
	
	# Returns evenly spaced numbers
	# over a specified interval.
	# X_ = np.linspace(date.min(), date.max(), 500)
	# Y_ = X_Y_Spline(X_)

	plt.plot(date, tabs)
	# plt.step(date, tabs, where = 'pre', label = 'vert_first')
	# plt.step(date, tabs, where = 'post', label = 'flat_first')
	plt.xlabel('Date')
	plt.ylabel('Tabs')
	plt.show()

def main():
	data = get_formatted_data('./data.csv')
	create_plot(data)


if __name__ == '__main__':
	main()