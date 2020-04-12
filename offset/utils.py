import random
import json
import sqlite3
from time import sleep


def random_sleep():
    sleep(random.randint(2, 15))


def save_info(array: list) -> None:
    with open('workua.txt', 'a') as file:
        for line in array:
            file.write('|'.join(line) + '\n')


def insert_info(result: list) -> None:
    connection = sqlite3.connect('WorkUADB.db')
    cursor = connection.cursor()

    sql = f'''insert into workua (title, company, conditions, salary, job_description) 
              values (?, ?, ?, ?, ?);'''

    cursor.execute(sql, (str(result[0]), str(result[1]), str(result[2]), str(result[3]), str(result[4]), ))
    connection.commit()
    connection.close()


def save_json(json_data: list) -> None:
    with open('data.json', mode='w', encoding='utf-8') as jf:
        json.dump(json_data, jf, ensure_ascii=False, indent=2)


