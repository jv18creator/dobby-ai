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

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
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