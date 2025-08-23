
import subprocess
import os
import csv
from dotenv import load_dotenv

load_dotenv()
CLASSROOM_LINK = os.getenv("CLASSROOM_LINK")
script_dir = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(script_dir, 'data', 'classroom_roster.csv')



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

def get_repos(unit_number):
    current_dir = os.getcwd()
    student_links = get_student_links(unit_number)
    for repo in student_links:
        print(repo+'\n')
        subprocess.run(['git', 'clone', repo],
                       cwd=current_dir,
                       env={**os.environ, 'GIT_SSH_COMMAND': 'ssh -i ~/.ssh/id_rsa_gcis'}
                      )

def main():
    
    while True:
        try:
           unit_number = input("Unit#: ")
           if unit_number.isalpha():
               raise ValueError
           if len(unit_number) != 2:
               raise ValueError
           break
        except:
            print("Unit must be two digits within 01-13")
            continue
        
    get_repos(str(unit_number))

if __name__ == '__main__':
    main()
