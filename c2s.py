import argparse
import dotenv
import dspy
import os
from typing import List
from models import CodeSummary
#from openai import AzureOpenAI


class ExtractExternalCopyBooks(dspy.Signature):
    """
    List of all external copybooks referenced in the source code.

    An external copybook is a separate file that contains data definitions and is referenced in the main code using the COPY statement but it is not defined in the code itself.
    """

    code = dspy.InputField(desc="Source code text to analyze for data models")
    copybooks: List[str] = dspy.OutputField(desc="list of Copybooks found in the code")


def read_code_file(file_path="sample_code.cbl"):
    """Read code from filesystem and return its contents."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: {file_path} not found. Please ensure the file exists in the current directory.")
        return None
    except IOError as e:
        print(f"Error reading file {file_path}: {e}")
        return None


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Analyze code using DSPy")
    parser.add_argument(
        "-f", "--file",
        default="sample_code.cbl",
        help="Path to the code file to analyze (default: sample_code.cbl)"
    )
    args = parser.parse_args()
    code_file_path = args.file
    dotenv.load_dotenv()

    deployment = os.environ["AZURE_DEPLOYMENT"]

    lm = dspy.LM(f"azure/{deployment}", cache=False)
    dspy.configure(lm=lm)
    response = dspy.ChainOfThought("code -> summary: CodeSummary")
    extract_models = dspy.ChainOfThought(ExtractExternalCopyBooks)

    # The simple signature below works well, but I prefer a class-based
    # signature so that I can control the outputs better.
    # extract_models = dspy.ChainOfThought("code -> copybooks: List[str]")

    # Read code from filesystem
    code = read_code_file(code_file_path)
    if code is None:
        return

    print("Code Summary:")
    summary = response(code=code)
    print(summary.summary)
    print(f"\n{'#'*80}\n")

    print("Copybooks Found:")
    models_result = extract_models(code=code)

    if hasattr(models_result, 'copybooks'):
        print(type(models_result.copybooks))
        print(models_result.copybooks)
    else:
        print(models_result)
    print(f"\n{'#'*80}\n")

    # dspy.inspect_history()


if __name__ == "__main__":
    main()
