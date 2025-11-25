from functions.get_files_info import get_files_info

def run_case(working_directory, directory, header):
    result = get_files_info(working_directory=working_directory, directory=directory)
    print(header)
    if isinstance(result, str) and result.startswith('Error:'):
        print(f"{result}")
    else:
        for line in result.splitlines():
            print(line)

    print()


if __name__ == "__main__":
    run_case("calculator", ".", "Result for current directory:")
    run_case("calculator", "pkg", "Result for 'pkg' directory:")
    run_case("calculator", "/bin", "Result for '/bin' directory:")
    run_case("calculator", "../", "Result for '../' directory:")