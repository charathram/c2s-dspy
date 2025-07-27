import argparse
import dotenv
import dspy
import os
from typing import List
from models import CodeSummary
from logging_config import get_default_logger, PerformanceLogger
from neo4j_client import Neo4jClient, Neo4jConnectionError, Neo4jQueryError

from utils import read_code_file, get_all_files
#from openai import AzureOpenAI

# Initialize logger
logger = get_default_logger()


class ExtractDataAccessObjects(dspy.Signature):
    """
    List of all external data access objects referenced in the source code.

    An external data access object is a separate file that contains data definitions and is referenced in the main code, but it is not defined in the code itself. Database files which are directly referenced in the code are NOT considered data access objects.
    """

    code = dspy.InputField(desc="Source code text to analyze for data access objects")
    daos: List[str] = dspy.OutputField(desc="list of data access objects found in the code")

class GenerateCodeSummary(dspy.Signature):
    """
    Generates a summary of the code.
    """

    code = dspy.InputField(desc="Source code text to analyze")
    filepath = dspy.InputField(desc="Filepath of the source code")
    summary: CodeSummary = dspy.OutputField(desc="Summary of the code")

def main():
    dotenv.load_dotenv()
    logger.debug("Environment variables loaded")

    with Neo4jClient.from_env() as client:
        if client.health_check():
            logger.debug("Neo4j connection is healthy")
        else:
            logger.debug("Neo4j connection is not healthy")

    deployment = os.environ["AZURE_DEPLOYMENT"]
    logger.info(f"Using Azure deployment: {deployment}")

    lm = dspy.LM(f"azure/{deployment}", cache=False)
    dspy.configure(lm=lm)
    logger.debug("DSPy configured with Azure LM")

    gen_summary = dspy.ChainOfThought(GenerateCodeSummary)
    extract_daos = dspy.ChainOfThought(ExtractDataAccessObjects)

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Analyze code using DSPy")

    # Create mutually exclusive group for file or directory
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument(
        "-f", "--file",
        default="sample_inputs/sample_code.cbl",
        help="Path to the code file to analyze (default: sample_inputs/sample_code.cbl)"
    )
    input_group.add_argument(
        "-d", "--dir",
        help="Path to a directory containing code files to analyze"
    )
    args = parser.parse_args()

    # Handle directory or file input
    if args.dir:
        logger.info(f"Starting code analysis for directory: {args.dir}")
        for filepath in get_all_files(args.dir):
            logger.info(f"Starting code analysis for file: {filepath}")
            # Read code from filesystem
            code = read_code_file(filepath)
            if code is None:
                logger.error("Failed to read code file, exiting")
                return
            logger.debug(f"Code file read successfully, length: {len(code)} characters")

            # Generate code summary
            with PerformanceLogger() as summary_perf:
                summary_perf.start("code_summary_generation")
                summary = gen_summary(code=code, filepath=filepath)

                logger.info("Code Summary:")
                logger.info(summary.summary.__dict__)
                with Neo4jClient.from_env() as client:
                    client.upsert(summary.summary.filename, summary.summary.suggested_classification, summary.summary.__dict__)


        # Extract data access objects
        # with PerformanceLogger() as extract_perf:
        #     extract_perf.start("dao_extraction")
        #     daos_result = extract_daos(code=code)

        # if hasattr(daos_result, 'daos'):
        #     logger.info("List of Data Access Objects:")
        #     logger.debug(f"DAOs type: {type(daos_result.daos)}")
        #     logger.debug(f"Reasoning: {daos_result.reasoning}")
        #     logger.info(f"Found DAOs: {daos_result.daos}")
        # else:
        #     logger.warning(f"Unexpected result format: {daos_result}")

        # logger.info("Code analysis completed successfully")

    # dspy.inspect_history()


if __name__ == "__main__":
    main()
