# convert stars to 1, 0, -1
# convert text using Bag of 
# fill in missing data
# join subtables with main tables 
# fill in nan with series
# find correlation with target variables
# find correlation in columns
# PCA? mainly for unsupervised learning
# merge tables
from sqlalchemy import create_engine
from settings import DATA_DIR
import pandas as pd
from multiprocessing import Pool
# from sklearn.preprocessing import LabelEncoder, OneHotEncoder

def _stars_to_target(x):
	"""
	Helper function to create target variable based on stars
	"""
	if x <= 2: #negative
		return -1
	elif x == 3: #neutral
		return 0
	else: #positive
		return 1

def create_target(df):
	"""
	create target variable in reviews table
	"""	
	df['target'] = df['stars'].map(lambda x: _stars_to_target(x))
	return df

def bag_of_words(df, col):
	"""
	Return pandas DataFrame object with bag of words dataframe
	"""
	series = df[col]
	wrds 
	return wrds

def bag_of_ngrams(df, col):
	"""
	Return pandas DataFrame object with bag of words dataframe
	"""
	series = df[col]
	ngrams
	return ngrams

def read_db(tbl):
	return pd.read_sql_table(tbl, engine, index_col='index')


if __name__ == "__main__":
	p = Pool(3)
	#figure out how to use pool with create engine
	engine = create_engine("sqlite:///" + DATA_DIR + '/yelp.db')
	engine.connect()
	main_tables = filter(lambda x: '_' not in x, engine.table_names())
	l_df = p.map(read_db, main_tables)
	create_target(l_df[2])