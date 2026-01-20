"""
ICS 32 Assignment 1 Part 1
A simple file management tool that lists directory contents.
"""

from pathlib import Path


def list_directory(path_str):
    """List contents of a directory."""
    path = Path(path_str)

    if not path.exists() or not path.is_dir():
        print("ERROR")
        return

    # This just prints everything in whatever order iterdir gives (TO BE FIXED)
    # Not sorting files before directories as required
    for item in sorted(path.iterdir()):
        print(item)


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
