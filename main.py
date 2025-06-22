import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from declare_functions import available_functions

def main():
    load_dotenv()

    # create a list of arguments that don't start with --
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if len(args) < 1:
        print("Error: No prompt provided.")
        sys.exit(1)

    prompt = " ".join(args) # join arguments into a sentence
    verbose = "--verbose" in sys.argv

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    if verbose:
        print("User prompt:", prompt)
    generate_content(client, messages, verbose)

def generate_content(client, messages, verbose):
    res = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )

    if verbose:
        print("Prompt tokens:", res.usage_metadata.prompt_token_count)
        print("Response tokens:", res.usage_metadata.candidates_token_count)
    if res.function_calls:
        for func_call in res.function_calls:
            print(f'Calling function: {func_call.name}({func_call.args})')
    else:
        print(res.text)

if __name__ == "__main__":
    main()
