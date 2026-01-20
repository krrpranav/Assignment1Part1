"""
ICS 32 Assignment 1 Part 1
A simple file management tool that lists directory contents.
"""

from pathlib import Path


def get_contents(directory, recursive=False):
    """Get files and directories from a path."""
    files = []
    directories = []

    try:
        for item in directory.iterdir():
            if item.is_file():
                files.append(item)
            elif item.is_dir():
                directories.append(item)
                # BUG: When recursive, we print subdirectory contents immediately
                # This messes up the order - should collect all first then sort
                if recursive:
                    sub_files, sub_dirs = get_contents(item, recursive=True)
                    # Printing here instead of collecting - wrong!
                    for sf in sub_files:
                        print(sf)
    except (PermissionError, FileNotFoundError):
        pass

    return sorted(files), sorted(directories)


def list_directory(path_str, options):
    """List contents of a directory with options."""
    path = Path(path_str)

    if not path.exists() or not path.is_dir():
        print("ERROR")
        return

    recursive = "r" in options
    files_only = "f" in options

    files, directories = get_contents(path, recursive=recursive)

    for f in files:
        print(f)

    if not files_only:
        for d in directories:
            print(d)


def parse_options(parts):
    """Parse command options from input parts."""
    options = []
    for part in parts[2:]:
        if part.startswith("-"):
            for char in part[1:]:
                options.append(char)
    return options


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
                options = parse_options(parts)
                list_directory(parts[1], options)
        else:
            print("ERROR")


if __name__ == "__main__":
    main()
