import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from declare_functions import available_functions
from functions.call_function import call_function

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

    i = 0
    while i < 20:
        i += 1
        
        try:
            final = generate_content(client, messages, verbose)
        except Exception as e:
            print(f'Error in generate_content: {e}')
            sys.exit(1)

        if final:
            print("Final response:")
            print(final)
            break
        if i == 20:
            print(f"Maximum iterations (20) reached.")
            sys.exit(1)

def generate_content(client, messages, verbose):
    res = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )

    if res.candidates:
        for candidate in res.candidates:
            messages.append(candidate.content)

    if verbose:
        print("Prompt tokens:", res.usage_metadata.prompt_token_count)
        print("Response tokens:", res.usage_metadata.candidates_token_count)
        
    if res.function_calls:
        for func_call in res.function_calls:
            result = call_function(func_call, verbose)
            messages.append(result)
            if not result.parts[0].function_response.response:
                raise ValueError("function call missing response")
            if verbose:
                print(f"-> {result.parts[0].function_response.response}")
    else:
        return res.text

if __name__ == "__main__":
    main()
