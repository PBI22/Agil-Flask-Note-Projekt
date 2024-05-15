"""
This module provides functionality to evaluate pylint scores against a specified threshold. 
It reads scores from a pylint report file and determines if any module scores fall below the given
threshold. If scores are below the threshold, it lists those modules and exits with an error.
If all scores meet or exceed the threshold, it confirms all scores are satisfactory.

Usage:
    Run the script with a threshold value as an argument.
    Example: python eval_pylint_scores.py 8.0
"""

import re
import sys


def main():
    """
    Main function for evaluating pylint scores.

    This function takes a threshold value as a command line argument and evaluates 
    the pylint scores of modules based on the threshold. It reads the pylint report file,
    extracts the scores, and checks if any module scores are below the threshold.
    If there are modules below the threshold, it prints the number of modules and their scores.
    If all module scores are above the threshold, it prints a message indicating that 
    all module scores are above the threshold.

    Parameters:
    - None

    Returns:
    - None

    Raises:
    - FileNotFoundError: If the pylint report file is not found.

    Usage:
    - python eval_pylint_scores.py <threshold>

    Example:
    - python eval_pylint_scores.py 8.0
    """
    if len(sys.argv) != 2:
        print("Usage: python eval_pylint_scores.py <threshold>")
        sys.exit(1)

    try:
        threshold = float(sys.argv[1])
    except ValueError:
        print("Error: Threshold must be a number.")
        sys.exit(1)

    try:
        with open("pylint_testreport.txt", "r", encoding="utf-8") as file:
            content = file.read()

        print(content)  # Print the entire pylint report -> on purpose Sune & Dauer ;o)

        scores = re.findall(r"Your code has been rated at ([-0-9.]+)/10", content)
        below_threshold = [float(score) for score in scores if float(score) < threshold]

        if below_threshold:
            print(
                f"There are {len(below_threshold)} Modules with scores below the threshold of {threshold}: {below_threshold}"
            )
            sys.exit(1)

        print(f"All module scores are above the threshold of {threshold}.")

    except FileNotFoundError:
        print(
            "Pylint report file not found. Ensure pylint was run and 'pylint_testreport.txt' was generated."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
