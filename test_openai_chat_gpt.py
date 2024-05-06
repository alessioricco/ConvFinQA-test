from openai import OpenAI
import re
import dataframe
from utils import extract_float, extractNumber, standardize_and_compare, query_openai_completion

client = OpenAI()



def _format_table(table_data):
    """ Format the table data into a readable string.

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
        str: The combined document as a string.
    """
    document = f"**Filename**: {data['id']}\n\n"
    document += "**Pre-Text Summary**:\n" + " ".join(data["pre_text"]) + "\n\n"
    document += _format_table(data["table"]) + "\n"
    document += "**Post-Text Analysis**:\n" + " ".join(data["post_text"]) + "\n\n"
    return document

def query_function(df, session_id, experiment, test_id, questions, item):
    """
    Perform a series of queries using OpenAI ChatGPT to answer a list of questions based on a given document.

    Args:
        df (pandas.DataFrame): The DataFrame to store the results of the queries.
        session_id (str): The session ID for tracking purposes.
        experiment (dict): A dictionary containing the experiment parameters.
        test_id (str): The ID of the test.
        questions (list): A list of tuples containing the questions and their corresponding answers.
        item (str): The document item to query.

    Returns:
        pandas.DataFrame: The updated DataFrame with the results of the queries.
    """
    document = _create_document(item)

    previous_questions = []
    question_index = 0
    for question, answer in questions:
           
        context = f"""
You are a financial analyst reviewing a dataset of financial information. 
You are tasked with answering questions based on the following content structured in three parts: pre-text, table, and post-text
{document}
"""   

        question_prompt = f"""
{question}

Answer this question just with the required value. 
If it's required a portion, it means it's a percentage
"""
           
        messages=[
            {"role": "system", "content": f"{context}"}
            # {"role": "assistant", "content": f"given the following document structured in three parts: pre-text, table, and post-text/n{document}"},
        ]
        
        current_question = [
            {"role": "user", "content": f"{question_prompt}"},   
        ]

        chat = messages + previous_questions + current_question
   
        openai_completion_params = {
            "model": experiment["model"],
            "max_tokens": experiment["max_tokens"] ,
            "temperature": experiment["temperature"],
            "messages": chat
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
        
        # previous_questions.append({"role": "assistant", "content": f"Previous answered questions: {question}. Answer:{response}."})
        previous_questions.append({"role": "user", "content": f"{question}"})
        previous_questions.append({"role": "assistant", "content": f"{response}"})
        question_index += 1
        
    return df