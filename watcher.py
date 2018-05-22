import os
import sys
import subprocess
import itertools

'''
TODO
    [X] Correctly parse cmd args
    [X] (In turn) correctly parse extra_cmd arg
'''

class AppConfig:

    def __init__(self, fe, cmd, extra_cmds, files, jobs, di):
        self.fe = fe
        self.cmd = cmd
        self.extra_cmds = extra_cmds
        self.files = files
        self.current_file = ""
        self.max_jobs = jobs
        self.delete_input = di

    def run_cmd(self):
        concatted = []
        new_cmd = ""
        for e_cmd in self.extra_cmds:
            try:
                concatted.append(e_cmd % self.current_file)
            except TypeError:
                concatted.append(e_cmd)
        for e_cmd in concatted:
            os.system(e_cmd)
        try:
            new_cmd = self.cmd % self.current_file
        except TypeError:
            new_cmd = self.cmd
        os.system(new_cmd)
        if (self.delete_input):
            os.system("rm %s" % self.current_file)
    
    def __eq__(self, other):
        return self.fe == other.fe and self.cmd == other.cmd and self.extra_cmds == other.extra_cmds and self.files == other.files

def get_file_ext(file_name):
    return "".join(reversed(list(itertools.takewhile(lambda x: x != ".", reversed(file_name)))))

def get_dir_contents(d):
    filtered_files = []
    files = os.listdir(d)
    a = sys.argv
    last_arg = ""
    cmd = ""
    cmd_extra = []
    file_extensions = []
    job_nums = 1000
    di = False
    for arg in a:
        if (arg == "-fe"):
            last_arg = "-fe"
        elif (arg == "-c"):
            last_arg = "-c"
        elif (arg == "-ce"):
            last_arg = "-ce"
        elif (arg == "-jc"):
            last_arg = "-jc"
        elif (arg == "-di"):
            last_arg = "-di"
        else:
            if (last_arg == "-fe"):
                file_extensions.append(arg)
            elif (last_arg == "-c"):
                cmd = arg
            elif (last_arg == "-ce"):
                cmd_extra.append(arg)
            elif (last_arg == "-jc"):
                job_nums = int(arg)
            elif (last_arg == "di"):
                di = True
    file_extensions = ".".join(file_extensions)
    for file in files:
        if get_file_ext(file) in file_extensions and file != "watcher.py":
            filtered_files.append(file)
    return AppConfig(file_extensions, cmd, cmd_extra, filtered_files, job_nums, di)

def main():
    done = False
    jobs = 0
    first_check = get_dir_contents('.')
    while (not done):
        second_check = get_dir_contents('.')
        if (first_check.files != second_check.files):
            second_check.current_file = [item for item in second_check.files if item not in first_check.files][0]
            print([item for item in second_check.files if item not in first_check.files])
            first_check = second_check
            ''' RUN ROUTINES '''
            first_check.run_cmd()
            jobs += 1
            if first_check.max_jobs == jobs:
                done = True

if __name__ == "__main__":
    main()