import os
import os.path as path

def get_files_info(working_directory, directory=None):
    work_dir = path.abspath(working_directory)
    current_dir = work_dir
    if directory:
        current_dir = path.abspath(path.join(work_dir, directory))
    if not (current_dir == work_dir or current_dir.startswith(work_dir + os.sep)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not path.isdir(current_dir):
        return f'Error: "{directory}" is not a directory'

    try:
        content = []
        for item in os.listdir(current_dir):
            size = path.getsize(path.join(current_dir, item))
            is_dir = path.isdir(path.join(current_dir, item))
            content.append(f"- {item}: file_size={size} bytes, is_dir={is_dir}")
        return "\n".join(content)
    except Exception as e:
        return f'Error: {e}'
