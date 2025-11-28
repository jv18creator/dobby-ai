import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    try:
        # Normalize paths
        abs_working = os.path.abspath(working_directory)
        target = os.path.abspath(os.path.join(working_directory, file_path))

        # Security: ensure target is inside working_directory
        if not target.startswith(abs_working + os.sep):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Check if file exists
        if not os.path.exists(target):
            return f'Error: File "{file_path}" not found.'

        # Check if file ends with .py
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        # Execute the Python file
        completed_process = subprocess.run(
            ["python", target] + args,
            cwd=abs_working,
            capture_output=True,
            text=True,
            timeout=30
        )

        # Format the output
        stdout = completed_process.stdout
        stderr = completed_process.stderr
        exit_code = completed_process.returncode

        # Build the result string
        result_parts = []

        if stdout:
            result_parts.append(f"STDOUT:\n{stdout}")

        if stderr:
            result_parts.append(f"STDERR:\n{stderr}")

        if exit_code != 0:
            result_parts.append(f"Process exited with code {exit_code}")

        if not result_parts:
            return "No output produced."

        return "\n".join(result_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"
