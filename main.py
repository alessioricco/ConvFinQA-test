import json
import uuid

from pandas import DataFrame
# import test_openai_completion_davinci
import test_openai_completion_gpt
import test_openai_chat_gpt
import dataframe
import datetime

file_name = 'train.json'
DATA_PATH = f'data/{file_name}'

experiments = [
    {
        "max_iterations":100,
        "name":"completion-gpt3.5",
        "model":"gpt-3.5-turbo-instruct",
        "completion":True,
        "temperature":0.1,
        "max_tokens":100,
        "refine_result":True,
        "query_function":test_openai_completion_gpt.query_function
    },
    {
        "max_iterations":0,
        "name":"chat-gpt4",
        "model":"gpt-4-turbo",
        "completion":False,
        "temperature":0.1,
        "max_tokens":100,
        "refine_result":True,
        "query_function":test_openai_chat_gpt.query_function
    }
]

# SELECTED_EXPERIMENT_NAME = "completion-gpt3.5"
SELECTED_EXPERIMENT_NAME = "chat-gpt4"

# SELECTED_ID = "Single_HIG/2004/page_122.pdf-2"
SELECTED_ID = None

def getExperiment(name:str):
    """
    Retrieve an experiment by its name.

    Args:
        name (str): The name of the experiment to retrieve.

    Returns:
        dict or None: The experiment dictionary if found, None otherwise.
    """
    for exp in experiments:
        if exp['name'] == name:
            return exp
    return None

def processItem(df:DataFrame, session_id:str, experiment:dict, item:dict) -> DataFrame:
    """
    Process an item by building a list of questions/answers, performing a query on a DataFrame,
    and returning the updated DataFrame.

    Args:
        df (DataFrame): The DataFrame to be queried.
        session_id (str): The session ID for the query.
        experiment (dict): The experiment details.
        item (dict): The item details.

    Returns:
        DataFrame: The updated DataFrame after performing the query.
    """
        
    # build the list of questions/answers
    qa_list = []
    if "qa" in item:
        qa_list.append(item['qa'])
    else:
        i = 0
        while f"qa_{i}" in item:
            qa_list.append(item[f"qa_{i}"])
            i += 1

    annotation = item['annotation']
    test_id = item['id']

    # questions
    print(f"\n\nProcessing item {test_id}")
    questions = [(qa['question'], qa['answer']) for qa in qa_list]
    # call the query function for the given test
    df = experiment["query_function"](df, session_id, experiment, test_id, questions, item)
    return df


def read_large_json(file_name:str):
    """
    Read a large JSON file and yield each item.

    Args:
        file_name (str): The path to the JSON file.

    Yields:
        dict: Each item in the JSON file.

    """
    with open(file_name, 'r') as file:
        data = json.load(file)
        for item in data:
            yield item


if __name__ == "__main__":
    
    df = dataframe.initialize_dataframe()
    
    session_id = uuid.uuid4().hex
    experiment = getExperiment(SELECTED_EXPERIMENT_NAME).copy()
    max_iterations = experiment['max_iterations'] if "max_iterations" in experiment else 999999999
    
    if not experiment:
        print("Experiment not found")
        exit()
    
    # todo: validate experiment params

    # for each item in the json file, run the processItem function 
    iteration = 0
    for item in read_large_json(DATA_PATH):
        if max_iterations != 0 and iteration > max_iterations:
            break
        if SELECTED_ID and item['id'] != SELECTED_ID:
            continue
        df = processItem(df, session_id,experiment,item)
        iteration += 1
    
    # Saving dataframe on the ./output folder
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df.to_csv(f"output/{experiment['name']}-{datetime.datetime.now()}.csv", index=False)