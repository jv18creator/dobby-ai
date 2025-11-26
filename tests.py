# run_cases.py

from functions.get_file_content import get_file_content

def run_case(working_directory, file_path, header):
    result = get_file_content(working_directory=working_directory, file_path=file_path)
    print(header)
    if isinstance(result, str) and result.startswith('Error:'):
        print(result)
    else:
        for line in result.splitlines():
            print(line)
    print()


if __name__ == "__main__":
    run_case("calculator", "main.py", 'Result for "calculator/main.py":')
    run_case("calculator", "pkg/calculator.py", 'Result for "calculator/pkg/calculator.py":')
    run_case("calculator", "/bin/cat", 'Result for "/bin/cat" (should be an error):')
    run_case("calculator", "pkg/does_not_exist.py", 'Result for "calculator/pkg/does_not_exist.py" (should be an error):')
