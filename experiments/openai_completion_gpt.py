import dataframe
from openai import OpenAI
from utils import extract_float, extractNumber, standardize_and_compare, query_openai_completion

client = OpenAI()


def _format_table(table_data):
    """
    Format the table data into a readable string.

    Args:
        table_data (list): A list of lists representing the table data.

    Returns:
        str: A formatted string representing the table.

    """
    table_str = "**Financial Data Overview**:\n"
    headers = table_data[0]
    table_str += "| " + " | ".join(headers) + " |\n"
    for row in table_data[1:]:
        table_str += "| " + " | ".join(row) + " |\n"
    return table_str

def _create_document(data):
    """
    Combine all parts of the data into a single document.

    Args:
        data (dict): A dictionary containing the data for creating the document.

    Returns:
        str: The combined document.

    """
    document = f"**Filename**: {data['id']}\n\n"
    document += "**Pre-Text Summary**:\n" + " ".join(data["pre_text"]) + "\n\n"
    document += _format_table(data["table"]) + "\n"
    document += "**Post-Text Analysis**:\n" + " ".join(data["post_text"]) + "\n\n"
    return document

def query_function(df, session_id, experiment, test_id, questions, item):
    """
    Executes a series of questions and answers using OpenAI's completion model.
    
    Args:
        df (pandas.DataFrame): The DataFrame to store the results.
        session_id (str): The session ID for tracking purposes.
        experiment (dict): The experiment configuration.
        test_id (int): The ID of the test.
        questions (list): A list of tuples containing the questions and their corresponding answers.
        item: The item to query.
    
    Returns:
        pandas.DataFrame: The updated DataFrame with the results.
    """
    document = _create_document(item)
    context = """
    Initial information based on the dataset provided, including pre-text, tables reformatted for clarity, etc.
    """
    question_index = 0
    previous_questions = ""
    for question, answer in questions:
        
        prompt = f"{context}{document}{previous_questions}{question}Answer:"
   
        openai_completion_params = {
            "model": experiment["model"],
            "prompt": prompt,
            "max_tokens": experiment["max_tokens"] ,
            "stop": ["\n"],
            "temperature": experiment["temperature"]
        }
        
        response = query_openai_completion(**openai_completion_params)
        extract_number = response
        if experiment.get("refine_result", False):
            extract_number = extractNumber(question, response)
        
        same_value = standardize_and_compare(str(answer), str(extract_number))
        
        print(f"TestId: {test_id}\nQuestion: {question}\nAnswer: {response}\n ({extract_number} --> {answer} : {same_value}) \n\n")
        
        df_row = {
            'Question ID': test_id,
            'Session': session_id,
            'Simulation': experiment['name'],
            'Question index': question_index,
            'Question': question,
            'Given Answer': str(answer),
            'Model Answer': response,
            'Processed Answer': extract_number,
            'Correct': same_value
        }
        df = dataframe.append_data(df,df_row)        
        
        previous_questions += f"Previous Question:{question}\nAnswer:{response}\n\n" 
        question_index += 1
        
    return df