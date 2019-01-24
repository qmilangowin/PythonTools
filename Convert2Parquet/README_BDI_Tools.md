

## Convert2parquet

A python script for converting CSV files to Parquet format. See `python3 convert2parquet.py -h` for help.
Currently it supports only single file conversions. I'll update the script with multiple-file conversions when time permits


***Environment Preparation***

Ensure that PyArrow is installed: pip3 install pyarrow. A better way is to use Anaconda.

If using Anaconda, create a conda isolated enviroment to ensure Pandas, etc. is installed:

<code>`conda create -n <name-of-your-environment> python=3.7 anaconda`</code> </br>
<code>`conda activate <name-of-your-environment>`</code> </br>
<code>`conda install pyarrow -c conda-forge`</code> </br>
<code>`conda install -c anaconda boto3`</code></br>

Then activate your environment by:

<code>`source activate <name-of-your-environment>`</code></br>

To exit your env: </br>
<code>`source deactivate` </code></br>

Alternatively, you can install the conda environment using the `parquet_conda_env` requirements/package file.  
See: [https://conda.io/docs/index.html](https://conda.io/docs/index.html) for more info. 

Some caveats using Pandas/PyArrow with Parquet files:


Duplicate column names and non-string columns names are not supported.
Index level names, if specified, must be strings.
Categorical dtypes can be serialized to parquet, but will de-serialize as object dtype.
Non supported types include Period and actual Python object types. These will raise a helpful error message on an attempt at serialization.

See pandas docs for more info: [pandas.pydata.org](https://pandas.pydata.org)