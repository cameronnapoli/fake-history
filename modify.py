import subprocess
from pathlib import Path
from datetime import datetime, date, timedelta

FOLDER = Path('files')
# make sure folder exists
FOLDER.mkdir(exist_ok=True)

def cmd(command, print_output=True):
    cmd_output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = cmd_output.stdout.decode('utf-8')
    stderr = cmd_output.stderr.decode('utf-8')
    if stdout and print_output:
        print(stdout)
    if stderr and print_output:
        print(stderr)
    return cmd_output.returncode


'''
https://dev.to/itsmohamedyahia/how-to-change-a-git-commit-date-for-beginners-40ge
'''
def convert_iso_to_git_date(iso_date):
    # Parse the ISO date string into a datetime object
    dt = datetime.strptime(iso_date, '%Y-%m-%d')
    
    # Format the datetime object into the desired git date format
    git_date = dt.strftime('%d %b %Y %H:%M:%S')
    return git_date


def fake_commit(iso_date, n=1):
    for i in range(n):
        # create file in folder
        path = Path(FOLDER, '{}-{}.txt'.format(iso_date, i))
        path.touch()
        # add file to git
        cmd('git add {}'.format(FOLDER))
        # commit with amended date
        cmd('git commit --date="{}" -m "fake commit"'.format(convert_iso_to_git_date(iso_date)))


def git_push(branch='main'):
    cmd('git push origin {}'.format(branch))


def run_for_dates(dates):
    for date in dates:
        fake_commit(date, 3)
    git_push()

def loop_through_year(year):
    start_date = date(year, 1, 1)
    end_date = date(year+1, 1, 1)

    current_date = start_date
    while current_date < end_date:
        yield current_date
        current_date += timedelta(days=1)


INVERT = True

YEAR = 2015

DATES = [
    # L
    '02-02',
    '02-03',
    '02-04',
    '02-05',
    '02-06',
    # 
    '02-09',
    '02-10',
    '02-11',
    '02-12',
    '02-13',
    # 
    '02-19',
    '02-20',
    '02-26',
    '02-27',

    # O
    '03-17',
    '03-18',
    '03-19',
    # 
    '03-23',
    '03-24',
    '03-25',
    '03-26',
    '03-27',
    '03-30',
    '04-06',
    '04-03',
    '04-10',
    # 
    '04-13',
    '04-14',
    '04-15',
    '04-16',
    '04-17',
    # 
    '04-21',
    '04-22',
    '04-23',

    # L
    '05-04',
    '05-05',
    '05-06',
    '05-07',
    '05-08',
    # 
    '05-11',
    '05-12',
    '05-13',
    '05-14',
    '05-15',
    # 
    '05-21',
    '05-28',
    '05-22',
    '05-29',
]

# Construct dates
dates = []

if INVERT:
    # Loop through all dates in year and don't add any in DATES
    for date in loop_through_year(YEAR):
        if date.strftime('%m-%d') not in DATES:
            dates.append(date.strftime('%Y-%m-%d'))
else:
    for date in DATES:
        dates.append('{}-{}'.format(YEAR, date))

run_for_dates(dates)
