import pandas as pd
import json
from pandas.io.json import json_normalize
import glob
from settings import DATA_DIR
import sqlite3

def get_fnames(regexp='yelp*.json'):
	"""
	Returns list of data file names

	regexp: str of file names to search for
	"""
	return glob.glob(DATA_DIR + '/' + regexp)


def read_data(fname):
	"""
	Converts json file into pandas DataFrame.

	Returns tuple with pandas DataFrame, table name, table name to be used as parent table name.

	fname: string of file name to read data from
	"""
	data = []
	with open(fname) as f:
		for line in f:
			data.append(json.loads(line))
	df = pd.DataFrame(data)
	return (df, df.loc[0, 'type'], df.loc[0, 'type'])

def _fix_dtype(x):
	"""
	Helper function to clean pandas Series into sql object types 
	or dictionaries to turn into pandas DataFrame. 
	Removes empty dictionaries and converts lists to strings.

	Returns updated pandas Series.

	x: lambda argument
	"""
    if isinstance(x, dict):
        if bool(x):
            return x
        else:
            return pd.np.nan
    elif isinstance(x, list):
    	if bool(x):
    		return ','.join(map(str, x))
    	else:
    		return pd.np.nan
    else:
        return x

def clean_series(series):
	"""
	Updates series by removing empty dictionaries 
	and converting lists to strings.

	Returns updated pandas Series object in same shape
	as original input pandas Series object.

	series: pandas Series object
	"""
	series = series.map(lambda x: _fix_dtype(x))
	return series

def find_dictionary(series):
	"""
	Checks for dictionary values in series.

	Returns masked pandas Series object. 

	series: pandas Series object
	"""
	series = series.dropna()
	return series[series.map(lambda x: isinstance(x, dict))]
	
def read_nested_data(series):
	"""
	Returns pandas DataFrame object from series whose values are dictionaries

	series: pandas Series with values that are dictionaries
	"""
	s = series.dropna()#### drop all values that are not dictionaries 
	idx = s.index
	df = json_normalize(list(s))
	df.index = idx
	return df

def clean_tables(df, fname, parent):
	"""
	Replaces dictionaries in pandas DataFrame with "nested"
	Creates tables from values that are dictionaries
	Saves DataFrame to sqlite3 database

	df: pandas DataFrame object
	fname: string of file name or column name
	parent: string of parent DataFrame name
	"""
	for col in df.columns:
		df[col] = clean_series(df[col])
		s_nest = find_dictionary(df[col])
		if len(s_nest) > 0:
			tbl = read_nested_data(s_nest)
			df.loc[tbl.index, col] = 'nested'
			clean_tables(tbl, col, fname)
		else:
			pass
	f = fname + '_' + parent if parent != fname else fname
	if 'type' not in df.columns:
		df['type'] = parent
	if df.columns.str.lower().duplicated().sum() > 0:
		df.columns = df.columns.str.lower()
		df = df.T.reset_index().drop_duplicates(subset='index', 
			take_last=True)
		df = df.set_index('index').T
		df.columns.name = None
	# ls.append((f, df))
	# return None
	
	try:
		print (f)
		df.to_sql(name=f, con=sqlite3.connect(DATA_DIR + '/yelp.db',
			timeout=60.0), if_exists='replace')
	except Exception as inst:
		print ('did not create table %s. %s' % (f, type(inst)))
	return None