
import os

def get_files_info(working_directory, directory="."):
    
    try:
        abs_working = os.path.abspath(working_directory)
        target = os.path.abspath(os.path.join(working_directory, directory))

        if not (target == abs_working or target.startswith(abs_working + os.sep)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.exists(target) or not os.path.isdir(target):
            return f'Error: "{directory}" is not a directory'
        
        lines = []
        for name in sorted(os.listdir(target)):
            full = os.path.join(target, name)
            try:
                st = os.stat(full)
                size = st.st_size
                is_dir = os.path.isdir(full)
                lines.append(f' - {name}: file_size={size} bytes, is_dir={is_dir}')
            except Exception as e:
                return f'Error: {e}'

        return "\n".join(lines)
        
    except Exception as e:
        return f'Error: {e}'