import os
from config import MAX_FILE_CHARS

def get_file_content(working_directory, file_path):
    try:
        # Normalize paths
        abs_working = os.path.abspath(working_directory)
        target = os.path.abspath(os.path.join(working_directory, file_path))

        # Security: ensure target is inside working_directory
        # Using startswith is acceptable ONLY after absolute normalization
        if not target.startswith(abs_working + os.sep):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Check file existence
        if not os.path.isfile(target):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read with limit
        with open(target, "r", errors="surrogateescape") as f:
            content = f.read(MAX_FILE_CHARS + 1)

        # Truncate if necessary
        if len(content) > MAX_FILE_CHARS:
            content = content[:MAX_FILE_CHARS] + \
                f'\n[...File "{file_path}" truncated at {MAX_FILE_CHARS} characters]'

        return content

    except Exception as e:
        return f"Error: {e}"
