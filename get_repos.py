
import subprocess
import os
import csv
from dotenv import load_dotenv

"""
IMPORTANT PREREQUISITE
YOU MUST ADD AN SSH KEY TO YOUR GITHUB ACCOUNT TO CLONE INTO EACH STUDENT'S REPO
PLS FOLLOW THE BELOW LINK FOR INSTRUCTIONS

https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens

YOU MUST CREATE A .env FILE TO STORE THE CLASSROOM LINK IN THE FORMAT:

CLASSROOM_LINK="INSERT LINK WITHIN QUOTES HERE"

AND THE SECTION NUMBER IN THE FORMAT:

SECTION_NUMBER="INSERT NUMBER WITHIN QUOTES HERE AS A TWO DIGIT STRING"

"""

load_dotenv()
CLASSROOM_LINK = os.getenv("CLASSROOM_LINK")
SECTION_NUMBER = os.getenv("SECTION_NUMBER")
script_dir = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(script_dir, 'data', 'classroom_roster.csv')



def get_student_links(unit_number):
    """
    Creates the unique github classroom links per student per unit \n

    Args: \n
    \tunit_number (str) : string representation of the currently used unit number \n

    Returns: \n
    \tAn array of strings of GH classroom links to be used to clone repos
    """
    with open(DATA_FILE) as file:
        reader = csv.reader(file)
        ret_links = []
        count = 0
        next(reader) 
        for line in reader:
            if line[0].startswith(SECTION_NUMBER):
                student_username = line[1]
                formatted_url = f"{CLASSROOM_LINK}unit{unit_number}-{student_username}"
                ret_links.append(formatted_url)
                count += 1
    print("*"*10)
    print(str(count) + "students found")
    print("*"*10)
    return ret_links

def get_repos(unit_number):
    """
    Uses the command line and student gh classroom links to clone repos
    Will cone to the current directory \n 

    Args: 
    \tunit_number (str) : string representation of the currently used unit number \n

    Returns: \n
   \tNone 
    """
    current_dir = os.getcwd()
    student_links = get_student_links(unit_number)
    for repo in student_links:
        print(repo+'\n')
        subprocess.run(['git', 'clone', repo],
                       cwd=current_dir,
                       env={**os.environ, 'GIT_SSH_COMMAND': 'ssh -i ~/.ssh/id_rsa_gcis'}
                      )

def main():

    #Unit numbers must be a two digit string to add to the repo links    
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
