import json
import os
from pathlib import Path

param = {
    'alpha': [0.1, 0.2, 0.3, 0.4, 0.5],
    'beta': [0.5, 0.6, 0.7, 0.8, 0.9],
    'iterations': [100, 200, 300, 400, 500],
}

def save_dict_to_json(param):
    """
    Converts a dictionary to JSON format and saves it to a file in the specified directory.

    Args:
        param (dict): The dictionary to be converted to JSON.
        directory (str): The directory where the file will be saved.
        filename (str): The name of the file to save the JSON data.

    Returns:
        None
    """
    directory = Path(__file__).parent.resolve() / "parameters"
    filename = "parameters.json"

    try:
        # Ensure the directory exists
        os.makedirs(directory, exist_ok=True)

        # Combine directory and filename to get the full path
        file_path = os.path.join(directory, filename)

        # Write the JSON data to the file
        with open(file_path, 'w') as json_file:
            json.dump(param, json_file, indent=4)
        print(f"Dictionary has been successfully saved to {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")






if __name__ == '__main__':
    save_dict_to_json(param)
