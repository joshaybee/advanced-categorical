import unittest

import pandas as pd
import numpy as np
from adegorical import adegorical as ad

small_unique = 10
medium_unique = 40
large_unique = 100
insane_unique = 1000

count_multiplier = 10

categorical_data_simple = ['yellow', 'red', 'yellow','red', 'magenta']
categorical_data_small_unique_small_count = [str(x) for x in range(small_unique)] + [str(x*2) for x in range(int(small_unique/2))] + [str(x*3) for x in reversed(range(int(small_unique/3)))]
categorical_data_medium_unique_small_count = [str(x) for x in range(medium_unique)] + [str(x*2) for x in range(int(medium_unique/2))] + [str(x*3) for x in reversed(range(int(medium_unique/3)))]
categorical_data_large_unique_small_count = [str(x) for x in range(large_unique)] + [str(x*2) for x in range(int(large_unique/2))] + [str(x*3) for x in reversed(range(int(large_unique/3)))]

categorical_data_small_unique_large_count = categorical_data_small_unique_small_count * count_multiplier
categorical_data_medium_unique_large_count = categorical_data_medium_unique_small_count * count_multiplier
categorical_data_large_unique_large_count = categorical_data_large_unique_small_count * count_multiplier

test_datasets = [categorical_data_small_unique_large_count, categorical_data_medium_unique_large_count, categorical_data_large_unique_large_count,
				 categorical_data_small_unique_small_count, categorical_data_medium_unique_small_count, categorical_data_large_unique_small_count]


class Help(unittest.TestCase):
	"""
	Ensures the help function has all the encoding methods available
	"""

	encoding_types = ['dummy', 'binary', 'simple_contrast', 'simple_regression', 'backward_difference_contrast', 'forward_difference_contrast', 'simple_helmert']

	def test_help_list(self):
		adegorical_help_types = ad.help()
		self.assertEqual(len(self.encoding_types), len(adegorical_help_types))


class DataType(unittest.TestCase):
	"""
	Checks that methods return the data type given 
	for all encoding methods
	"""
	
	encoding_methods = ad.help()

	def test_pandas_series_output(self):
		pandas_series = pd.Series(categorical_data_simple)
		for encoding_method in self.encoding_methods:
			encoded_results_pandas = ad.get_categorical(pandas_series, encoding=encoding_method)
			self.assertTrue(isinstance(encoded_results_pandas, pd.DataFrame))

	def test_numpy_array_output(self):
		numpy_array = np.array(categorical_data_simple)
		for encoding_method in self.encoding_methods:
			encoded_results_numpy = ad.get_categorical(numpy_array, encoding=encoding_method)
			self.assertTrue(isinstance(encoded_results_numpy, np.ndarray))
				

	def test_list_output(self):
		python_list = categorical_data_simple
		for encoding_method in self.encoding_methods:
			encoded_results_list = ad.get_categorical(python_list, encoding=encoding_method)	
			self.assertTrue(isinstance(encoded_results_list, list))


class DummyEncoding(unittest.TestCase):
	"""
	Test cases for dummy variable encoding.
	Checks that the correct number of columns are returned for dummy encoded objects. 
	n-1 columns should be returned where n is the number of unique variables.
	"""
	def test_dummy_list_column_size(self):

		for test_dataset in test_datasets:
			unique_variables = len(set(test_dataset))
			test_dataset_column_count = unique_variables - 1
			encoded_results_column_count = len(ad.get_categorical(test_dataset, encoding='dummy')[0])
			self.assertEqual(test_dataset_column_count, encoded_results_column_count)

	def test_dummy_pandas_column_size(self):

		for test_dataset in test_datasets:
			unique_variables = len(set(test_dataset))
			test_dataset_column_count = unique_variables - 1
			test_dataset_pandas = pd.Series(test_dataset)
			encoded_results_column_count = ad.get_categorical(test_dataset_pandas, encoding='dummy').shape[1]
			self.assertEqual(test_dataset_column_count, encoded_results_column_count)

	def test_dummy_numpy_column_size(self):

		for test_dataset in test_datasets:
			unique_variables = len(set(test_dataset))
			test_dataset_column_count = unique_variables - 1
			test_dataset_numpy = np.array(test_dataset)
			encoded_results_column_count = len(ad.get_categorical(test_dataset_numpy, encoding='dummy')[0])
			self.assertEqual(test_dataset_column_count, encoded_results_column_count)


class InputCheck(unittest.TestCase):
	"""Checks edge cases to make sure proper handling is administrated"""

	encoding_methods = ad.help()

	def test_dummy_list_zero_len_dataset(self):
		zero_dataset = []

		for encoding_method in self.encoding_methods:
			self.assertRaises(ad.OutOfRangeError, ad.get_categorical, zero_dataset, encodoing=encoding_method)

	def test_dummy_numpy_zero_len_dataset(self):
		zero_dataset = []

		for encoding_method in self.encoding_methods:
			self.assertRaises(ad.OutOfRangeError, ad.get_categorical, zero_dataset, encodoing=encoding_method)
			
	def test_dummy_pandas_zero_len_dataset(self):
		zero_dataset = []

		for encoding_method in self.encoding_methods:
			self.assertRaises(ad.OutOfRangeError, ad.get_categorical, zero_dataset, encodoing=encoding_method)
	
	def test_dummy_list_one_len_dataset(self):
		one_dataset = ['len_of_one']

		for encoding_method in self.encoding_methods:
			self.assertRaises(ad.OutOfRangeError, ad.get_categorical, one_dataset, encodoing=encoding_method)

	def test_dummy_numpy_one_len_dataset(self):
		one_dataset = ['len_of_one']

		for encoding_method in self.encoding_methods:
			self.assertRaises(ad.OutOfRangeError, ad.get_categorical, one_dataset, encodoing=encoding_method)
			
	def test_dummy_pandas_one_len_dataset(self):
		one_dataset = ['len_of_one']

		for encoding_method in self.encoding_methods:
			self.assertRaises(ad.OutOfRangeError, ad.get_categorical, one_dataset, encodoing=encoding_method)


if __name__ == '__main__':
    unittest.main()