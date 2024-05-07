# Project Title

This is an LLM driven prototype that can run through the ConvFinQA dataset (https://github.com/czyssrs/ConvFinQA) and provide answers to the queries for the subset. 

It's made of two parts:
one is the software that is generating the answers from one of the training files
the other is a Jupyter Notebook for analysing the results

the ConvFinQA dataset must be stored in the ./data folder

## Getting Started

```python

git clone https://github.com/alessioricco/ConvFinQA-test.git
cd ConvFinQA-test.git
pip install -r requirements.txt
```


### Executing program

* setup the `.env` file with your OpenAI key.
* Run the script `main.py`.

## Functionality

#Main.py Overview
The main.py script is the entry point of our application. It primarily handles the processing of test items and the reading of large JSON files.

#Processing Test Items
The script processes each test item by calling a query function specified in the experiment dictionary. The experiment["query_function"] is expected to be a function that takes in several parameters including a DataFrame df, a session_id, the experiment dictionary, a test_id, a list of questions, and an item. The function is expected to return a DataFrame.

The questions are extracted from a list of question-answer pairs (qa_list), with each question and its corresponding answer forming a tuple.

#Reading Large JSON Files
The read_large_json function is a generator that reads a large JSON file one item at a time. This is particularly useful when dealing with large datasets that cannot fit into memory all at once. The function takes in a file name as a parameter, opens the file, loads the JSON data, and yields each item in the data one at a time.

#Script Execution
The if __name__ == "__main__": line at the end of the script ensures that the code is only executed when the script is run directly (e.g., python main.py), and not when it's imported as a module. The specific code to be executed when the script is run directly is not shown in the provided excerpt.

#test_openai_completion_gpt.py Overview
The test_openai_completion_gpt.py script is part of our testing suite, specifically designed to test the performance of OpenAI's GPT models on a set of predefined questions and answers.

#Querying OpenAI's GPT Models
The script constructs a dictionary of parameters for querying an OpenAI GPT model. These parameters include the model name, the prompt (question), the maximum number of tokens in the response, the stop sequence, and the temperature (a parameter that controls the randomness of the model's output).

The script then calls the _query_openai_completion function with these parameters to get a response from the model.

#Refining and Comparing the Response
If the refine_result flag in the experiment dictionary is set to True, the script refines the model's response using the extractNumber function. This function is expected to extract a number from the response.

#The script then standardizes and compares the refined response (or the original response if no refinement was done) with the expected answer using the standardize_and_compare function. This function is expected to return a boolean value indicating whether the response and the answer are the same.

#Logging the Results
The script logs the test ID, the question, the given answer, the model's response, the refined response (if any), and whether the response was correct. It does this by appending a new row to a DataFrame df.

The DataFrame is then updated with the new row using the dataframe.append_data function.