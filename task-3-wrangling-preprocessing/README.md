# Task 3: Data Wrangling/preprocessing

## Data Preprocessing tasks for each subteam
 - Data Cleaning
 - Feature Selection
 - Data Transforms

## schemas.json
A schema-like JSON describing the characteristics of the final consolidated dataset.
Each key is referred to a input field (e.g. "country"), and has the following values:
* ```dtype```: the primitive data type, like *int*, *boolean*, *float*, *string* ...
* ```MLtype```: The data will be categorized into 4 basic types from a Machine Learning perspective: numerical data, categorical data, time-series data, and text. To clarify the distinction with the *dtype* property, think about *numerical* data: they can be *int*, or they can be *string*. If you're unsure about this field, a good reference to start is [Statistical data type](https://en.wikipedia.org/wiki/Statistical_data_type) and [Data Types From A Machine Learning Perspective](https://towardsdatascience.com/data-types-from-a-machine-learning-perspective-with-examples-111ac679e8bc#:~:text=Most%20data%20can%20be%20categorized,-series%20data%2C%20and%20text.).
* ```description```: a short description about the variable/field, aimed to quickly help to understand what's about and how to use it.
* ```enum```: a list of possible values for categorical features.

## Final datasets

The final tagged data is available from the `All_data_sources_merged_updated.csv` file.
