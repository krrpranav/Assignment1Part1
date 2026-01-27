# a1.py
#
# NAME: Pranav
# EMAIL: pkumar4@uci.edu
# STUDENT ID: 63767742
#
# ICS 32 - Assignment 1 Part 2
#

from pathlib import Path


def list_directory(path, recursive, files_only, search_name, search_ext):
    """
    List the contents of a directory.

    Files are printed first, then directories.
    Both are sorted alphabetically.

    Parameters:
        path: Path object of the directory to list
        recursive: If True, recursively list subdirectories
        files_only: If True, only print files (not directories)
        search_name: If set, only print files matching this exact name
        search_ext: If set, only print files with this extension
    """
    # Try to get directory contents
    try:
        items = list(path.iterdir())
    except (PermissionError, FileNotFoundError, NotADirectoryError):
        return

    # Separate files and directories
    files = []
    dirs = []

    for item in items:
        if item.is_file():
            files.append(item)
        elif item.is_dir():
            dirs.append(item)

    # Sort alphabetically for consistent output
    files.sort()
    dirs.sort()

    # Normalize extension if provided
    normalized_ext = None
    if search_ext is not None:
        if search_ext.startswith("."):
            normalized_ext = search_ext
        else:
            normalized_ext = "." + search_ext

    # Print files that match the filters
    for file in files:
        # Check filename filter
        if search_name is not None and file.name != search_name:
            continue

        # Check extension filter
        if normalized_ext is not None and file.suffix != normalized_ext:
            continue

        print(file)

    # Print directories and recurse if needed
    for directory in dirs:
        # Print directory path unless files_only is set
        if not files_only:
            print(directory)

        # Recurse into subdirectory if recursive mode is on
        if recursive:
            list_directory(directory, recursive, files_only, search_name, search_ext)


def parse_list_options(parts):
    """
    Parse the options for the L command.

    Supported options:
        -r  Recursive listing
        -f  Files only (exclude directories)
        -s  Search by filename (requires parameter)
        -e  Filter by extension (requires parameter)

    Parameters:
        parts: List of input tokens

    Returns:
        Tuple of (options_list, option_parameter, has_error)
    """
    options = []
    option_param = None
    error = False

    # Start parsing from index 2 (after command and path)
    i = 2

    while i < len(parts):
        part = parts[i]

        # Check if this is an option flag
        if part.startswith("-"):
            # Process each character in the option
            for char in part[1:]:
                options.append(char)

                # -s and -e require a parameter
                if char in ["s", "e"]:
                    # Check if next token exists and is not another option
                    if i + 1 < len(parts) and not parts[i + 1].startswith("-"):
                        i += 1
                        option_param = parts[i]
                    else:
                        error = True

        i += 1

    return options, option_param, error


def handle_list(parts):
    """
    Handle the L (list) command.

    Usage: L <directory> [options]

    Lists the contents of the specified directory.
    """
    # Check for minimum required parts
    if len(parts) < 2:
        print("ERROR")
        return

    # Parse options from input
    options, option_param, error = parse_list_options(parts)

    # Check for parsing errors
    if error:
        print("ERROR")
        return

    # Get the directory path
    path = Path(parts[1])

    # Validate the path exists and is a directory
    if not path.exists() or not path.is_dir():
        print("ERROR")
        return

    # Extract option flags
    recursive = "r" in options
    files_only = "f" in options
    search_name = option_param if "s" in options else None
    search_ext = option_param if "e" in options else None

    # Using -s or -e implies files only
    if search_name is not None or search_ext is not None:
        files_only = True

    # Execute the directory listing
    list_directory(path, recursive, files_only, search_name, search_ext)


def handle_create(parts):
    """
    Handle the C (create) command.

    Usage: C <directory> -n <filename>

    Creates a new .dsu file in the specified directory.
    The .dsu extension is automatically appended.
    """
    # Check for minimum required parts: C <dir> -n <name>
    if len(parts) < 4:
        print("ERROR")
        return

    # Get the directory path
    directory = Path(parts[1])

    # Validate directory exists
    if not directory.exists() or not directory.is_dir():
        print("ERROR")
        return

    # Validate -n option is present
    if parts[2] != "-n":
        print("ERROR")
        return

    # Get the filename
    filename = parts[3]

    # Create the new .dsu file
    try:
        new_file = directory / (filename + ".dsu")
        new_file.touch()
        print(new_file)
    except (PermissionError, OSError):
        print("ERROR")


def handle_delete(parts):
    """
    Handle the D (delete) command.

    Usage: D <filepath>

    Deletes the specified .dsu file.
    Only .dsu files can be deleted with this command.
    """
    # Check for correct number of parts
    if len(parts) != 2:
        print("ERROR")
        return

    # Get the file path
    file_path = Path(parts[1])

    # Validate file has .dsu extension
    if file_path.suffix != ".dsu":
        print("ERROR")
        return

    # Validate file exists
    if not file_path.exists() or not file_path.is_file():
        print("ERROR")
        return

    # Delete the file
    try:
        file_path.unlink()
        print(f"{file_path} DELETED")
    except (PermissionError, OSError):
        print("ERROR")


def handle_read(parts):
    """
    Handle the R (read) command.

    Usage: R <filepath>

    Reads and prints the contents of the specified .dsu file.
    Prints EMPTY if the file has no content.
    """
    # Check for correct number of parts
    if len(parts) != 2:
        print("ERROR")
        return

    # Get the file path
    file_path = Path(parts[1])

    # Validate file has .dsu extension
    if file_path.suffix != ".dsu":
        print("ERROR")
        return

    # Validate file exists
    if not file_path.exists() or not file_path.is_file():
        print("ERROR")
        return

    # Read the file contents
    try:
        content = file_path.read_text()

        # Check if file is empty
        if content == "":
            print("EMPTY")
        else:
            # Print each line of content
            for line in content.splitlines():
                print(line)
    except (PermissionError, OSError):
        print("ERROR")


def main():
    """
    Main function to run the file management tool.

    Continuously reads user input and executes commands
    until the user enters Q to quit.
    """
    while True:
        # Read user input
        try:
            user_input = input()
        except EOFError:
            break

        # Parse input into parts
        parts = user_input.strip().split()

        # Skip empty input
        if not parts:
            continue

        # Get the command (case-insensitive)
        command = parts[0].upper()

        # Execute the appropriate command
        if command == "Q":
            break
        elif command == "L":
            handle_list(parts)
        elif command == "C":
            handle_create(parts)
        elif command == "D":
            handle_delete(parts)
        elif command == "R":
            handle_read(parts)
        else:
            print("ERROR")


if __name__ == "__main__":
    main()
