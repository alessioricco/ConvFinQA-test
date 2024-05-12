from openai import OpenAI
import re

client = OpenAI()

def query_openai_chat_completion(**openai_completion_params):
    """Function to send queries to OpenAI and receive the response."""
    try:
        response = client.chat.completions.create(
            **openai_completion_params
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("An error occurred:", e)
        return None

def query_openai_completion(**openai_completion_params):
    """
    Function to send queries to OpenAI and receive the response.

    Args:
        **openai_completion_params: Keyword arguments to be passed to the OpenAI completions.create() method.

    Returns:
        str: The text of the first choice in the response, stripped of leading and trailing whitespace.

    Raises:
        Exception: If an error occurs during the API call.

    """
    try:
        response = client.completions.create(
            **openai_completion_params
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print("An error occurred:", e)
        return None

def extract_float(string):
    """
    Extracts the first floating-point number from a given string.

    Args:
        string (str): The input string from which to extract the floating-point number.

    Returns:
        float or None: The first floating-point number found in the string, or None if no numbers found.

    Raises:
        None.

    """
    try:
        # Define the regular expression pattern to match floating-point numbers with optional sign
        string = string.replace(",", "")
        pattern = r'-?\d+\.\d+|-?\d+'
        # Use findall to extract all floating-point numbers from the string
        numbers = re.findall(pattern, string)
        # Return the first floating-point number found (or None if no numbers found)
        return float(numbers[0]) if numbers else None
    except:
        return string

def extractNumber(question, response):
    """
    Extracts the value representing the correct answer from the given question and response.

    Args:
        question (str): The question.
        response (str): The answer.

    Returns:
        float: The extracted value representing the correct answer.
    """
    prompt = f"""
    Given the following Question and Answer, extract only and exclusively the value representing the correct answer. Pay attention to the required format, if it's a percentage, or a value representing an increment, decrement or with a specific measure unit\n 
    Q:{question}\nA:{response}
    """
    
    params = {
        "model": "gpt-4-turbo",
        "max_tokens": 200 ,
        "temperature": 0.1,
        "messages": [
            {"role": "user", "content": prompt}
        ]  
    }
    value = query_openai_chat_completion(**params)
    return extract_float(value)

# Function to remove non-numeric characters except decimal point
def clean_string(s):
    # Remove everything except digits, minus sign, and decimal point
    return re.sub(r"[^\d\.-]", "", s)

def standardize_and_compare(str1, str2):
    """
    Standardizes two strings by removing non-numeric characters except decimal point,
    converts them to floats, and compares the resulting numbers for equality.

    Args:
        str1 (str): The first string to compare.
        str2 (str): The second string to compare.

    Returns:
        bool: True if the standardized and converted numbers are equal, False otherwise.
    """

    
    # Clean both strings
    # clean1 = clean_string(str(extract_float(str1)))
    # clean2 = clean_string(str(extract_float(str2)))
    
    # Convert to float
    try:
        
        clean1 = extract_float(clean_string(str(str1)))
        clean2 = extract_float(clean_string(str(str2)))
        
        num1 = float(clean1)
        num2 = float(clean2)
    except Exception as e:
        return False  # Return False if conversion to float fails
    
    # Compare numbers
    return num1 == num2