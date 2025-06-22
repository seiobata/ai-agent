import os
import os.path as path
from subprocess import run

def run_python_file(working_directory, file_path, args=None):
    work_dir = path.abspath(working_directory)
    file = path.abspath(path.join(work_dir, file_path))
    if not file.startswith(work_dir + os.sep):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not path.exists(file):
        return f'Error: File "{file_path}" not found.'
    extension = path.splitext(file)[1]
    if extension != ".py":
        return f'Error: "{file_path}" is not a Python file.'
    
    commands = ["python", file]
    if args:
        commands.extend(args)

    try:
        process = run(commands, text=True, timeout=30, capture_output=True, cwd=work_dir)
    except Exception as e:
        return f'Error: executing Python file: {e}'
    
    output = []
    if process.stdout:
        output.append(f"STDOUT:\n{process.stdout}")
    if process.stderr:
        output.append(f"STDERR:\n{process.stderr}")
    if process.returncode != 0:
        output.append(f"Process exited with code {process.returncode}")
    
    return "\n".join(output) if output else "No output produced."
