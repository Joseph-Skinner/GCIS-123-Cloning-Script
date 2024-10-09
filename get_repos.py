#!/usr/bin/env python3

import subprocess
import os
import csv

DATA_FILE = '/Users/josephskinner/scripts/RIT/GCIS123/cloning/data/classroom_roster.csv'
CLASSROOM_LINK = 'git@github.com:GCIS-123-Fall2024/unit$%-'


def get_student_links(unit_number):
    with open(DATA_FILE) as file:
        reader = csv.reader(file)
        ret_links = []
        next(reader) 
        for line in reader:
            student_username = line[1]
            formatted_url = CLASSROOM_LINK + student_username
            formatted_url = formatted_url.replace('$%', unit_number)
            ret_links.append(formatted_url)
    return ret_links

def get_repos():
    current_dir = os.getcwd()
    unit_number = input('Unit#: ')
    student_links = get_student_links(unit_number)
    for repo in student_links:
        print(repo+'\n')
        subprocess.run(['git', 'clone', repo],
                       cwd=current_dir,
                       env={**os.environ, 'GIT_SSH_COMMAND': 'ssh -i ~/.ssh/id_rsa_gcis'}
                      )

def main():
    get_repos()

if __name__ == '__main__':
    main()
