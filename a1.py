# a1.py

# NAME: Pranav
# EMAIL: pkumar4@uci.edu
# STUDENT ID: 63767742

"""
ICS 32 Assignment 1
A file management tool for working with directories and .dsu files.
"""

from pathlib import Path


def list_directory(
    path, recursive=False, files_only=False, search_name=None, search_ext=None
):
    """Print directory contents with depth-first traversal."""
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

    files.sort()
    dirs.sort()

    for f in files:
        if search_name is not None and f.name != search_name:
            continue
        if search_ext is not None:
            ext = search_ext if search_ext.startswith(".") else "." + search_ext
            if f.suffix != ext:
                continue
        print(f)

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
    """Parse options and parameters from input."""
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

    if search_name is not None or search_ext is not None:
        files_only = True

    list_directory(
        path,
        recursive=recursive,
        files_only=files_only,
        search_name=search_name,
        search_ext=search_ext,
    )


def execute_create_command(parts):
    """Execute the C command to create a new .dsu file."""
    if len(parts) < 2:
        print("ERROR")
        return

    directory = Path(parts[1])

    if not directory.exists() or not directory.is_dir():
        print("ERROR")
        return

    filename = None
    i = 2
    while i < len(parts):
        if parts[i] == "-n" and i + 1 < len(parts):
            filename = parts[i + 1]
            break
        i += 1

    if filename is None:
        print("ERROR")
        return

    new_file = directory / (filename + ".dsu")
    new_file.touch()
    print(new_file)


def execute_delete_command(parts):
    """Execute the D command to delete a .dsu file."""
    if len(parts) < 2:
        print("ERROR")
        return

    file_path = Path(parts[1])

    # BUG: Not checking if file has .dsu extension
    if not file_path.exists() or not file_path.is_file():
        print("ERROR")
        return

    file_path.unlink()
    print(f"{file_path} DELETED")


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
        elif command == "C":
            execute_create_command(parts)
        elif command == "D":
            execute_delete_command(parts)
        else:
            print("ERROR")


if __name__ == "__main__":
    main()
