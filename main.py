import dotenv
import dspy
import os
from logging_config import get_default_logger, PerformanceLogger
#from openai import AzureOpenAI

# Initialize logger
logger = get_default_logger()

def main():
    logger.info("Starting c2s-dspy main example")

    with PerformanceLogger() as perf:
        perf.start("main_example")

        dotenv.load_dotenv()
        logger.debug("Environment variables loaded")

        deployment = os.environ["AZURE_DEPLOYMENT"]
        logger.info(f"Using Azure deployment: {deployment}")

        lm = dspy.LM(f"azure/{deployment}")
        dspy.configure(lm=lm)
        logger.debug("DSPy configured with Azure LM")

        response = dspy.ChainOfThought("question -> answer: str")

        question = "I want to visit the capital of United States. I am a pilot and flight instructor. What should I see?"
        logger.debug(f"Asking question: {question}")

        result = response(question=question)
        logger.info(f"Response received: {result}")

    logger.info("Main example completed successfully")

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
