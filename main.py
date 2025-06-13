import dotenv
import dspy
import os
from . import models
#from openai import AzureOpenAI

def main():
    print("Hello from c2s-dspy!")
    dotenv.load_dotenv()

    deployment = os.environ["AZURE_DEPLOYMENT"]


    lm = dspy.LM(f"azure/{deployment}")
    dspy.configure(lm=lm)
    response = dspy.ChainOfThought("question -> answer: str")
    print(response(question="I want to visit the capital of United States. Iam a pilot and flight instructor. What should I see?"))

# def aoai_test():
#     dotenv.load_dotenv()
#     api_version = os.getenv("AZURE_API_VERSION")
#     azure_endpoint = os.getenv("AZURE_API_BASE")
#     api_key = os.getenv("AZURE_API_KEY")
#     deployment="gpt-4o"

#     client = AzureOpenAI(
#         api_version=api_version,
#         azure_endpoint=azure_endpoint,
#         api_key=api_key
#     )

#     response = client.chat.completions.create(
#         messages=[
#             {
#                 "role": "system",
#                 "content": "You are a helpful assistant.",
#             },
#             {
#                 "role": "user",
#                 "content": "I am going to Paris, what should I see?",
#             }
#         ],
#         max_tokens=4096,
#         temperature=1.0,
#         top_p=1.0,
#         model=deployment
#     )

#     print(response.choices[0].message.content)


if __name__ == "__main__":
#aoai_test()
    main()
