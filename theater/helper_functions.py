import os

def read_actor_description(file_name):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    directory_path = os.path.join(current_directory, "static", "theater", "actor_descriptions")
    file_path = os.path.join(directory_path, str(file_name) + ".txt")
    print(file_path)
    try:
        with open(file_path, 'r') as file:
            paragraph_content = file.read()
        return paragraph_content
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"An error occurred: {e}"