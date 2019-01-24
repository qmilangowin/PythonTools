#!/usr/bin/env python3

"""
Ensure that PyArrow is installed: pip3 install pyarrow. A better way is to use Anaconda.

If using Anaconda, create a conda isolated enviroment to ensure Pandas, etc. is installed:
conda create -n <name-of-your-environment> python=3.7 anaconda
conda activate <name-of-your-environment> 
conda install pyarrow -c conda-forge
conda install -c anaconda boto3

Then activate your environment by:

source activate <name-of-your-environment>

To exit your env: source deactivate 

Below script uses Pandas and PyArrow: Some caveats using Pandas/PyArrow with Parquet files:


Duplicate column names and non-string columns names are not supported.
Index level names, if specified, must be strings.
Categorical dtypes can be serialized to parquet, but will de-serialize as object dtype.
Non supported types include Period and actual Python object types. These will raise a helpful error message on an attempt at serialization.

See pandas docs for more info: pandas.pydata.org


"""

import os
import sys
import threading
import boto3
import argparse
import pandas as pd
import traceback
parser = argparse.ArgumentParser()

BUCKET=""

class csvParquetConverter():

	def __init__(self,filename):
		self.filename = filename
		self.parquet_file = self.filename.replace(".csv",".parquet")

	def __str__(self):
		return "Displaying File: {}".format(self.filename)

	def convert(self):
		try: 
			print("Converting file: {}".format(self.filename))
			df=pd.read_csv(self.filename,low_memory=False)
			df.to_parquet(self.parquet_file)
		except Exception:
			print("Could not open CSV file. \nSee below for more info: \n")
			print(traceback.format_exc())


class ParquetFileViewer():

	def __init__(self,filename):
		self.filename=filename

	def __str__(self):
		return "Displaying File: {}".format(self.filename)

	def viewParquetFull(self):
		try: 
			parquet = pd.read_parquet(self.filename)
			return parquet
		except Exception:
			print("Could not open Parquet file. \nSee below for more info: \n")
			print(traceback.format_exc())

	def viewParquetRange(self,range=10):
		try: 
			parquet = pd.read_parquet(self.filename)
			return parquet.head(range)
		except Exception:
			print("Could not open Parquet file. \nSee below for more info: \n")
			print(traceback.format_exc())

class ProgressPercentage():

	def __init__(self, filename):
		self._filename = filename
		self._size = float(os.path.getsize(filename))
		self._seen_so_far = 0
		self._lock = threading.Lock()
	def __call__(self, bytes_amount):
		with self._lock:
			self._seen_so_far += bytes_amount
			percentage = (self._seen_so_far / self._size) * 100
			sys.stdout.write(
			"\r%s  %s / %s  (%.2f%%)" % (
			self._filename, self._seen_so_far, self._size,
			percentage))
			sys.stdout.flush()


class S3Uploader():

	def __init__(self,filename):
		self.filename=filename

	def upload(self, bucket=BUCKET):
		try: 
			s3=boto3.client('s3')
			s3.upload_file(
				self.filename,bucket,self.filename,
				Callback=ProgressPercentage(self.filename))
		except Exception:
			print("Could not upload file \nSee below for more info: \n")
			print(traceback.format_exc())


def main():


	parser.add_argument('-csv',dest='csv_filename',nargs='?', help="usage: convert2parquet.py -f <filename.csv> - converts the CSV to Parquet", type=str)
	parser.add_argument('-vph',dest='parquet_filename_h',nargs='?',help="usage: csv2parquet.py -vph <filename.parquet> - displays dataframe.head()", type=str)
	parser.add_argument('-vpf',dest='parquet_filename_f',nargs='?',help="usage: csv2parquet.py -vpf <filename.parquet> - displays the condensed file", type=str)
	parser.add_argument('-s3f',dest='parquet_filename_s3',nargs='?',help="usage: csv2parquet.py -s3 <filename.parquet> - uploads file to default s3 bucket: qlik-bdi-internal-data", type=str)
	parser.add_argument('-s3bucket',dest='s3bucket',nargs=2,help="usage:  python3 convert2parquet.py  -s3bucket <bucket_name>  <file_name> - uploads file to s3 bucket of your choice", type=str)

	args=parser.parse_args()
	csv_file=args.csv_filename
	view_parquet_head=args.parquet_filename_h
	view_parquet_full=args.parquet_filename_f
	filename_s3 = args.parquet_filename_s3
	s3bucket = args.s3bucket

	if csv_file:
		csv=csvParquetConverter(csv_file)
		csv.convert()
	elif view_parquet_head:
		parquet=ParquetFileViewer(view_parquet_head)
		print(parquet.viewParquetRange())
	elif view_parquet_full:
		parquet=ParquetFileViewer(view_parquet_full)
		print(parquet.viewParquetFull())
	elif filename_s3:
		s3_upload=S3Uploader(filename_s3)
		s3_upload.upload()
	elif s3bucket:
		s3bucket,filename_s3 = s3bucket
		s3_upload=S3Uploader(filename_s3)
		s3_upload.upload(s3bucket)
	else:
		print("Type convert2parquet -h for usage")



if __name__ == "__main__":
	main()