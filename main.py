import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from config import system_prompt

load_dotenv()
api_key = os.environ.get('GEMINI_API_KEY')

client = genai.Client(api_key=api_key)

def main():
    print("sys.argv", sys.argv)
    if len(sys.argv) < 2:
        print("Error: Missing content argument. Please provide content as the first argument.")
        sys.exit(1)

    content = sys.argv[1]

    if not content.strip():
        print("Error: Provided content is empty. Please provide non-empty content.")
        sys.exit(1)

    messages = [
        types.Content(role="user", parts=[types.Part(text=content)])
    ]

    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )

    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Reads and returns the content of a specified file, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the file to read, relative to the working directory.",
                ),
            },
            required=["file_path"],
        ),
    )
    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Executes a Python file with optional command-line arguments, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the Python file to execute, relative to the working directory.",
                ),
                "args": types.Schema(
                    type=types.Type.ARRAY,
                    description="Optional command-line arguments to pass to the Python script.",
                    items=types.Schema(type=types.Type.STRING),
                ),
            },
            required=["file_path"],
        ),
    )
    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Writes content to a specified file, creating directories if needed, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the file to write, relative to the working directory.",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content to write to the file.",
                ),
            },
            required=["file_path", "content"],
        ),
    )

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt))
    if '--verbose' in sys.argv:
        print("Verbose mode enabled")
        print(f"User prompt: {content}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    # print(response.text)
    if response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if part.function_call:
                print(f"Calling function: {part.function_call.name}({part.function_call.args})")


if __name__ == "__main__":
    main()