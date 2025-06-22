import os
import os.path as path

def write_file(working_directory, file_path, content):
    work_dir = path.abspath(working_directory)
    file = path.abspath(path.join(work_dir, file_path))
    if not file.startswith(work_dir + os.sep):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        os.makedirs(path.dirname(file), exist_ok=True)
        with open(file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'
