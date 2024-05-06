# Project Title

This project processes data from a large JSON file using a selected experiment.
results are available in the /output folder
data are stored in the /data folder (please unzip the file)

## Description

The main script reads a large JSON file, applies an experiment to each item in the JSON file, and stores the results in a dataframe. The dataframe is then saved to a CSV file.

## Getting Started

### Dependencies

* Python 3.x
* pandas
* uuid
* datetime
* json

### Installing

* Clone the repository to your local machine.
* Install the required Python packages.

### Executing program

* Run the script `main.py`.

## Functionality

The script `main.py` performs the following steps:

1. Initializes a new dataframe.
2. Generates a unique session ID.
3. Selects an experiment based on the `SELECTED_EXPERIMENT_NAME` variable.
4. Reads items from a large JSON file located at `DATA_PATH`.
5. Applies the selected experiment to each item in the JSON file.
6. Stores the results in the dataframe.
7. Saves the dataframe to a CSV file in the `output` directory.

The `processItem` function is used to apply the experiment to each item. This function calls the `query_function` defined in the experiment.

The `read_large_json` function is used to read items from the large JSON file. This function yields each item in the JSON file one at a time, which allows it to handle very large files.

## Authors

[Alessio Ricco]

