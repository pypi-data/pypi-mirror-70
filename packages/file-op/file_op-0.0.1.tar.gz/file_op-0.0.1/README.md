# file_op

This package is to find the delimiter of any file.

## The file should have minimum 2 rows in it.

# How to install module

pip install file-op

## Module name

find_delimiter

## function to call

find_delimiter.find_delim(file_name,number_of_col)
### where
* file_name : Name of the file
* col : Number of columns in the file.
## How to call

import find_delimiter.find_delim.find_delim

delimiter = find_delim(file_name,number_of_col)

## Returns

### The function returns the delimiter of the file.
### If the delimiter is not found then it will return '-1'
### In case of any error, it will return '-2' and will print the error on console.

## The possible delimiter list

#### This module uses the possible delimiter list as below :

delim_list = [',', '"', '_', '$', '#', '@', '&', '*','%','\t',' ','|']

#### If you want include more delimiters, add using below 

import import find_delimiter.find_delim.delim_list

delim_list.append('YOUR-DELIMITER')

