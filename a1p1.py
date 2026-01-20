"""
ICS 32 Assignment 1 Part 1
A simple file management tool that lists directory contents.
"""

from pathlib import Path


def list_directory(path_str):
    """List contents of a directory with files first, then directories."""
    path = Path(path_str)

    if not path.exists() or not path.is_dir():
        print("ERROR")
        return

    files = []
    directories = []

    # Separate files and directories
    for item in path.iterdir():
        if item.is_file():
            files.append(item)
        elif item.is_dir():
            directories.append(item)

    # Sort each list
    files.sort()
    directories.sort()

    # Print files first, then directories
    for f in files:
        print(f)
    for d in directories:
        print(d)


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
            if len(parts) < 2:
                print("ERROR")
            else:
                list_directory(parts[1])
        else:
            print("ERROR")


if __name__ == "__main__":
    main()
