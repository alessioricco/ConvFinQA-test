import pandas as pd

def initialize_dataframe():
    # Define the structure of the DataFrame with the appropriate columns
    columns = ['Question ID', 'Session', 'Simulation', 'Question index', 'Question', 'Given Answer', 'Model Answer', 'Processed Answer', 'Correct']
    # Create an empty DataFrame with these columns
    df = pd.DataFrame(columns=columns)
    return df

def append_data(df, new_data):
    """
    Appends a new row of data to the DataFrame.

    Parameters:
    - df (DataFrame): The existing DataFrame.
    - new_data (dict): A dictionary containing the new data to append.

    Returns:
    - DataFrame: The updated DataFrame with the new data appended.
    """
    # Convert the new_data dictionary to a DataFrame
    new_df = pd.DataFrame(new_data, index=[0])
    # Append the new DataFrame to the existing one without resetting the index
    updated_df = pd.concat([df, new_df], ignore_index=True)
    return updated_df
