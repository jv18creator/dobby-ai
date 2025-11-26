# tests.py

from functions.write_file import write_file

def run_case(working_directory, file_path, content, header):
    result = write_file(working_directory=working_directory, file_path=file_path, content=content)
    print(header)
    print(result)
    print()


if __name__ == "__main__":
    run_case("calculator", "lorem.txt", "wait, this isn't lorem ipsum", 'Result for write_file("calculator", "lorem.txt", "wait, this isn\'t lorem ipsum"):')
    run_case("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet", 'Result for write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"):')
    run_case("calculator", "/tmp/temp.txt", "this should not be allowed", 'Result for write_file("calculator", "/tmp/temp.txt", "this should not be allowed"):')
