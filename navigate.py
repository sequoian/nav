"""
Create shortcut aliases for quick command line navigation.
Note: The included batch file should be called to run this script, since python files
cannot change a user's current working directory.
"""

import json
import sys
import argparse

# File to store the key-value pairs
FILE_PATH = "alias.json"


def nav(directory):
    """
    Output directory to tmp file.
    The batch file calling this script will read the file, delete it, and change directories.
    """
    with open("tmp", "w") as json_file:
        json_file.write(directory)

    sys.exit()


def run():
    """ Run the application """
    # Configure argument parser
    parser = argparse.ArgumentParser(prog="nav", description="Navigate to a \
                                     directory using an alias")
    parser.add_argument("cwd", type=str, help=argparse.SUPPRESS)
    parser.add_argument("-l", "--list", action="store_true", help="List aliases")  
    group = parser.add_mutually_exclusive_group()
    group.add_argument("alias", type=str, nargs="?", help="The alias for a directory")
    group.add_argument("-s", "--set", type=str, action="store",
                       help="Set alias to current directory")
    group.add_argument("-r", "--remove", type=str, action="store", help="Remove alias")

    # Parse arguments
    try:
        args = parser.parse_args()
    except SystemExit:
        # Nav back to cwd
        nav(sys.argv[1])

    # Read data from file, or create a new file if it does not exist
    try:
        with open(FILE_PATH, "r") as json_file:
            try:
                data = json.load(json_file)
            except ValueError:
                data = {}
    except FileNotFoundError:
        with open(FILE_PATH, "w+") as json_file:
            data = {}

    # Handle command
    if args.list:
        # List aliases
        for alias in sorted(data):
            print(alias + ": " + data[alias])
    elif args.set:
        # Set alias and save file
        with open(FILE_PATH, "w") as json_file:
            data[args.set] = args.cwd
            json.dump(data, json_file)
            print("'{}' added to nav".format(args.set))
    elif args.remove:
        # Remove alias and save file
        with open(FILE_PATH, "w") as json_file:
            try:
                del data[args.remove]
                json.dump(data, json_file)
                print("'{}' removed from nav".format(args.remove))
            except KeyError:
                json.dump(data, json_file)
                print("nav: error: That alias does not exist")
    elif args.alias:
        if args.alias in data:
            # Navigate to directory pointed to by the alias
            nav(data[args.alias])
        else:
            print("nav: error: That alias does not exist")
    else:
        # Incorrect usage
        parser.print_usage()

    # Go back to current directory
    nav(args.cwd)


if __name__ == '__main__':
    run()
