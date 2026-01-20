"""
ICS 32 Assignment 1 Part 1
A simple file management tool that lists directory contents.

Commands:
    L - List the contents of a directory
    Q - Quit the program

Options for L command:
    -r  Output directory content recursively
    -f  Output only files, excluding directories
    -s  Output only files that match a given file name
    -e  Output only files that match a given file extension
"""

from pathlib import Path


def get_contents(directory, recursive=False):
    """
    Get files and directories from a path.

    Returns:
        Tuple of (files, directories) as sorted lists.
    """
    files = []
    directories = []

    try:
        for item in directory.iterdir():
            if item.is_file():
                files.append(item)
            elif item.is_dir():
                directories.append(item)

        files.sort()
        directories.sort()

        if recursive:
            for subdir in list(directories):
                sub_files, sub_dirs = get_contents(subdir, recursive=True)
                files.extend(sub_files)
                directories.extend(sub_dirs)

    except (PermissionError, FileNotFoundError):
        pass

    return files, directories


def filter_by_name(paths, name):
    """Filter to only files matching exact name."""
    return [p for p in paths if p.name == name]


def filter_by_extension(paths, extension):
    """Filter to only files with given extension."""
    # Fixed: Now handles both 'txt' and '.txt' formats
    if not extension.startswith("."):
        extension = "." + extension
    return [p for p in paths if p.suffix == extension]


def list_directory(path_str, options, option_param):
    """List contents of a directory with options."""
    path = Path(path_str)

    if not path.exists() or not path.is_dir():
        print("ERROR")
        return

    recursive = "r" in options
    files_only = "f" in options
    search_name = "s" in options
    search_ext = "e" in options

    files, directories = get_contents(path, recursive=recursive)

    if search_name and option_param:
        files = filter_by_name(files, option_param)
        files_only = True

    if search_ext and option_param:
        files = filter_by_extension(files, option_param)
        files_only = True

    for f in sorted(files):
        print(f)

    if not files_only:
        for d in sorted(directories):
            print(d)


def parse_input(parts):
    """Parse options and option parameter from input."""
    options = []
    option_param = ""

    i = 2
    while i < len(parts):
        part = parts[i]
        if part.startswith("-"):
            opt = part[1:]
            for char in opt:
                options.append(char)
            if opt in ["s", "e"] and i + 1 < len(parts):
                i += 1
                option_param = parts[i]
        i += 1

    return options, option_param


def main():
    """Main function to run the file management tool."""
    while True:
        try:
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
                    options, option_param = parse_input(parts)
                    list_directory(parts[1], options, option_param)
            else:
                print("ERROR")

        except EOFError:
            break


if __name__ == "__main__":
    main()
