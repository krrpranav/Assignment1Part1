"""
ICS 32 Assignment 1 Part 1
A simple file management tool that lists directory contents.
"""

from pathlib import Path


def main():
    """Main function to run the file management tool."""
    while True:
        user_input = input()

        parts = user_input.strip().split()

        if not parts:
            continue

        command = parts[0].upper()

        if command == "Q":
            break
        elif command == "L":
            # Implement list command
            print("List command not implemented yet")
        else:
            print("ERROR")


if __name__ == "__main__":
    main()
