import os
import pandas as pandas
from modules import loadData, logger
import multiprocessing

if __name__ == '__main__':
	p = multiprocessing.Pool(3)
	logger.info('Getting file names...')
	fnames = loadData.get_fnames()
	logger.info('Reading in json files...')
	l_df = p.map(loadData.read_data, fnames)
	logger.info('Read successful!')
	logger.info('Separating nested JSON objects...')
	p.starmap(loadData.clean_tables, l_df)
	logger.info('Added dataframes to database!')
	del l_df
