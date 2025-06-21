import os
import os.path as path

def get_file_content(working_directory, file_path):
    work_dir = path.abspath(working_directory)
    file = path.abspath(path.join(work_dir, file_path))
    if not file.startswith(work_dir + os.sep):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not path.isfile(file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    MAX_CHARS = 10000

    try:
        with open(file, "r") as f:
            content = f.read(MAX_CHARS + 1)
            if len(content) > MAX_CHARS:
                content = (
                    content[:MAX_CHARS] + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
            return content
    except Exception as e:
        return f'Error: {e}'
