import pandas as pd
import json
from pandas.io.json import json_normalize
import glob
from settings import DATA_DIR

def get_fnames(regexp='yelp*.json'):
	"""
	Returns list of data file names

	regexp: str of file names to search for
	"""
	return glob.glob(DATA_DIR + '/' + regexp)

def read_data(fname):
	"""
	Returns pandas DataFrame object containing data from yelp json file

	fname: file name to read data from
	"""
	data = []
	with open(fname) as f:
		for line in f:
			data.append(json.loads(line))
	df = pd.DataFrame(data)
	return df

def find_dictionary(df):
	"""
	Returns column names with 

	df: pandas DataFrame object containing dictionary values as column values
	"""
	return df.columns[df.apply(lambda x: isinstance(x[0], dict))]

def read_nested_data(series):
	"""
	Returns pandas DataFrame object from series whose values are dictionaries

	series: pandas Series whose values are dictionaries
	"""
	return json_normalize(list(series))