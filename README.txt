File Management Tool

A command-line program that lists directory contents.

Commands:
  L <path> List contents of a directory
  Q Quit the program

Options for L:
  -r          List recursively (includes subdirectories)
  -f          Show only files
  -s <name>   Find files with this exact name
  -e <ext>    Find files with this extension

Examples:
  L /home/user/documents
  L /home/user/documents -r
  L /home/user/documents -f
  L /home/user/documents -r -f
  L /home/user/documents -s notes.txt
  L /home/user/documents -e pdf
  L /home/user/documents -r -e txt

Author: Pranav