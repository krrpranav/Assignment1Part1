# a1.py
#
# NAME: Pranav
# EMAIL: pkumar4@uci.edu
# STUDENT ID: 63767742

from pathlib import Path


def list_directory(path, recursive, files_only, search_name, search_ext):
    """List directory contents."""
    try:
        items = list(path.iterdir())
    except (PermissionError, FileNotFoundError, NotADirectoryError):
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
            list_directory(d, recursive, files_only, search_name, search_ext)


def parse_options(parts):
    """Parse options from input parts."""
    options = []
    option_param = None
    error = False

    i = 2
    while i < len(parts):
        part = parts[i]
        if part.startswith("-"):
            for char in part[1:]:
                options.append(char)
                if char in ["s", "e"]:
                    if i + 1 < len(parts) and not parts[i + 1].startswith("-"):
                        i += 1
                        option_param = parts[i]
                    else:
                        error = True
        i += 1

    return options, option_param, error


def handle_list(parts):
    """Handle L command."""
    if len(parts) < 2:
        print("ERROR")
        return

    options, option_param, error = parse_options(parts)

    if error:
        print("ERROR")
        return

    path = Path(parts[1])

    if not path.exists() or not path.is_dir():
        print("ERROR")
        return

    recursive = "r" in options
    files_only = "f" in options
    search_name = option_param if "s" in options else None
    search_ext = option_param if "e" in options else None

    if search_name is not None or search_ext is not None:
        files_only = True

    list_directory(path, recursive, files_only, search_name, search_ext)


def handle_create(parts):
    """Handle C command."""
    if len(parts) < 4:
        print("ERROR")
        return

    directory = Path(parts[1])

    if not directory.exists() or not directory.is_dir():
        print("ERROR")
        return

    if parts[2] != "-n":
        print("ERROR")
        return

    filename = parts[3]

    try:
        new_file = directory / (filename + ".dsu")
        new_file.touch()
        print(new_file)
    except (PermissionError, OSError):
        print("ERROR")


def handle_delete(parts):
    """Handle D command."""
    if len(parts) != 2:
        print("ERROR")
        return

    file_path = Path(parts[1])

    if file_path.suffix != ".dsu":
        print("ERROR")
        return

    if not file_path.exists() or not file_path.is_file():
        print("ERROR")
        return

    try:
        file_path.unlink()
        print(f"{file_path} DELETED")
    except (PermissionError, OSError):
        print("ERROR")


def handle_read(parts):
    """Handle R command."""
    if len(parts) != 2:
        print("ERROR")
        return

    file_path = Path(parts[1])

    if file_path.suffix != ".dsu":
        print("ERROR")
        return

    if not file_path.exists() or not file_path.is_file():
        print("ERROR")
        return

    try:
        content = file_path.read_text()

        if content == "":
            print("EMPTY")
        else:
            for line in content.splitlines():
                print(line)
    except (PermissionError, OSError):
        print("ERROR")


def main():
    """Main function."""
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
