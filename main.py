import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    load_dotenv()

    if len(sys.argv) < 2:
        print("Error: No prompt provided.")
        sys.exit(1)
    prompt = " ".join(sys.argv[1:])

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    res = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages
    )

    print(res.text)
    print("Prompt tokens:", res.usage_metadata.prompt_token_count)
    print("Response tokens:", res.usage_metadata.candidates_token_count)

if __name__ == "__main__":
    main()
