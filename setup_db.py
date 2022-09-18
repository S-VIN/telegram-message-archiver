import psycopg2
import glob
import os
import itertools

connection = psycopg2.connect(
    database="telegram_my_messages", user='postgres', password='3228', host='127.0.0.1', port='5432'
)

connection.autocommit = True
cursor = connection.cursor()

def get_last_used_script():
    cursor.execute('SELECT script_name FROM last_used_script')
    message_records = cursor.fetchall()
    return message_records[0][0]


def get_number_of_script(script_name):
    return int(script_name[4:script_name.find('-')])


def sql_sort(dict_of_files):
    files_with_numbers = dict()
    for filename in dict_of_files:
        files_with_numbers[get_number_of_script(filename)] = filename
    return sorted(files_with_numbers.items())


def set_executed(filename):
    cursor.execute('UPDATE last_used_script SET script_name = \'' + filename + '\' WHERE onerow_id=true;')


def execute_script(filename):
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        text = f.name
        command = open(f.name, "r").read()
        cursor.execute(command)

sorted_scripts = sql_sort(glob.glob('sql/*.sql'))
last_script = get_number_of_script(get_last_used_script())

for script_pair in sorted_scripts:
    if script_pair[0] > last_script:
        print(script_pair[1], 'EXECUTE')
        try:
            execute_script(script_pair[1])
            set_executed(script_pair[1])
        except Exception as err:
            print(script_pair[1], 'ERROR EXECUTION')
            print(err)
            print('SCRIPT STOPPED')
            break
    else:
        print(script_pair[1], 'SKIPPED')
