#/usr/local/bin/python3

# Generator and storage of customer invoice id.
# Hens Zimmerman, 13-06-2021, python3. MacOS only.

# ID has the following format:

# YYMMnnn e.g. 2106023
# YY is year of invoice
# MM is month of invoice
# nnn is next number in line

from datetime import datetime
import os
import platform
import re
import subprocess

# Hidden file where the last id has been stored.

storage_file = '.hza_stored_id'

# Not running on Darwin? Then bail out.

if platform.system() != 'Darwin':
    print('This code only runs on MacOS')
    exit()

# Generate YYMM portion of id.

now = datetime.now() # current date and time
cur_month = now.strftime("%m")
cur_year = now.strftime("%y")
prefix = cur_year + cur_month

# Read old number.

if os.path.isfile(storage_file):
    file = open(storage_file, "r")
    id = file.read(7)
    file.close()

    matches = re.match(r"(\d{2})(\d{2})(\d{3})", id)

    if matches:
        id_year = matches.group(1)
        id_month = matches.group(2)
        id_num = matches.group(3)
    else:
        # this should of course never happen.
        print("Wrong number read!\n")
        exit()

    # Have we entered a new month?

    if id_month != cur_month or id_year != cur_year:
        # Reset number to 1.
       id = prefix + '001'
    else:
        # Bump up number.
        id = prefix + "%03d" % (int(id_num) + 1)
else:
    # First time run; generate an id.
    id = prefix + '001'

# Store new number

file = open(storage_file, "w")
file.write(id)
file.close()

# Copy number as plain text to clipboard.

process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
process.communicate(id.encode('utf-8'))

print("Your new invoice has id: " + id)
print("This number has been copied to the MacOS clipboard.\n")
