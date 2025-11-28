# tests.py

from functions.run_python_file import run_python_file

def run_case(working_directory, file_path, args, header):
    result = run_python_file(working_directory=working_directory, file_path=file_path, args=args)
    print(header)
    print(result)
    print()


if __name__ == "__main__":
    run_case("calculator", "main.py", [], 'Result for run_python_file("calculator", "main.py"):')
    run_case("calculator", "main.py", ["3 + 5"], 'Result for run_python_file("calculator", "main.py", ["3 + 5"]):')
    run_case("calculator", "tests.py", [], 'Result for run_python_file("calculator", "tests.py"):')
    run_case("calculator", "../main.py", [], 'Result for run_python_file("calculator", "../main.py"):')
    run_case("calculator", "nonexistent.py", [], 'Result for run_python_file("calculator", "nonexistent.py"):')
    run_case("calculator", "lorem.txt", [], 'Result for run_python_file("calculator", "lorem.txt"):')
