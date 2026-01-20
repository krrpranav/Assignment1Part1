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


def list_directory(
    path, recursive=False, files_only=False, search_name=None, search_ext=None
):
    """
    Print directory contents with depth-first traversal.

    Order: files first, then directories (no alphabetical sorting - uses filesystem order).
    If recursive: after printing a directory, immediately print its contents.
    """
    try:
        items = list(path.iterdir())
    except (PermissionError, FileNotFoundError):
        return

    files = []
    dirs = []

    for item in items:
        if item.is_file():
            files.append(item)
        elif item.is_dir():
            dirs.append(item)

    # Print files (with filters if specified)
    for f in files:
        if search_name is not None and f.name != search_name:
            continue
        if search_ext is not None:
            ext = search_ext if search_ext.startswith(".") else "." + search_ext
            if f.suffix != ext:
                continue
        print(f)

    # Print each directory, then recurse into it if recursive mode
    for d in dirs:
        if not files_only:
            print(d)
        if recursive:
            list_directory(
                d,
                recursive=True,
                files_only=files_only,
                search_name=search_name,
                search_ext=search_ext,
            )


def parse_input(parts):
    """
    Parse options and parameters from input.

    Returns: (options, option_param, error)
    """
    options = []
    option_param = None
    error = False

    i = 2
    while i < len(parts):
        part = parts[i]
        if part.startswith("-"):
            opt_chars = part[1:]
            for char in opt_chars:
                options.append(char)
                # -s and -e require a parameter
                if char in ["s", "e"]:
                    if i + 1 < len(parts) and not parts[i + 1].startswith("-"):
                        i += 1
                        option_param = parts[i]
                    else:
                        error = True
        i += 1

    return options, option_param, error


def execute_list_command(path_str, options, option_param, error):
    """Execute the L command."""
    if error:
        print("ERROR")
        return

    path = Path(path_str)

    if not path.exists() or not path.is_dir():
        print("ERROR")
        return

    recursive = "r" in options
    files_only = "f" in options
    search_name = option_param if "s" in options else None
    search_ext = option_param if "e" in options else None

    # -s and -e imply files only
    if search_name is not None or search_ext is not None:
        files_only = True

    list_directory(
        path,
        recursive=recursive,
        files_only=files_only,
        search_name=search_name,
        search_ext=search_ext,
    )


def main():
    """Main function to run the file management tool."""
    while True:
        try:
            user_input = input()
        except EOFError:
            break

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
                options, option_param, error = parse_input(parts)
                execute_list_command(parts[1], options, option_param, error)
        else:
            print("ERROR")


if __name__ == "__main__":
    main()
