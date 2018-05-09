import os
import sys
import subprocess

def get_dir_contents(d):
    filtered_files = []
    files = os.listdir(d)
    a = sys.argv
    print(a)
    last_arg = ""
    cmd = ""
    cmd_extra = []
    file_extensions = []
    for arg in a:
        if (arg == "-fe"):
            last_arg = "-fe"
        elif (arg == "-c"):
            last_arg = "-c"
        elif (arg == "-ce"):
            last_arg = "-ce"
        else:
            if (last_arg == "-fe"):
                file_extensions.append(arg)
            elif (last_arg == "-c"):
                cmd = arg
            elif (last_arg == "-ce"):
                cmd_extra.append(arg)
    file_extensions = ".".join(file_extensions)
    print(cmd)
    print(cmd_extra)
    print(file_extensions)
    for file in files:
        if (file[-2:]) in file_extensions and file != "watcher.py":
            filtered_files.append(file)
    return filtered_files

def main():
    done = False
    first_check = get_dir_contents('.')
    while (not done):
        done = True
        second_check = get_dir_contents('.')
        if (first_check != second_check):
            first_check = second_check
            ''' RUN ROUTINES '''

if __name__ == "__main__":
    main()