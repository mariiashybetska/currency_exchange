import requests
import sqlite3
import json

from bs4 import BeautifulSoup
from user_agent import generate_user_agent

from offset.utils import save_info, random_sleep, insert_info, save_json

HOST = 'https://www.work.ua'
ROOT_PATH = '/ru/jobs/'


def main():
    page = 1

    while True:
        # if page == 30:
        #     break

        payload = {
            'ss': 1,
            'page': page,
        }
        user_agent = generate_user_agent()
        headers = {
            'User-Agent': user_agent,
        }

        print(f'PAGE: {page}')

        response = requests.get(HOST + ROOT_PATH, params=payload, headers=headers)
        response.raise_for_status()

        # if response.status_code != 200:
        #     print('something wrong!')
        #     break

        random_sleep()

        html = response.text

        soup = BeautifulSoup(html, 'html.parser')
        cards = soup.find_all(
            'div',
            class_='card card-hover card-visited wordwrap job-link js-hot-block'
        )

        if not cards:
            break

        result = []
        salary = ''
        json_result = []

        for card in cards:
            # card = cards[0]
            tag_a = card.find('h2').find('a')
            title = tag_a.text
            href = tag_a['href']
            job_response = requests.get(HOST + href, params=payload, headers=headers)
            html = job_response.text
            soup = BeautifulSoup(html, 'html.parser')
            job_description = soup.find_all('div', attrs={'id': 'job-description'})[0].get_text()
            conditions_info = soup.find_all('p', attrs={'class': 'text-indent add-top-sm'})

            for elem in conditions_info:
                if 'glyphicon-tick' in elem.find('span')['class']:
                    conditions = elem.get_text().strip().replace('\n', '').replace('   ', ' ')

            top_info = soup.find_all('p', attrs={'class': 'text-indent text-muted add-top-sm'})

            for elem in top_info:
                if 'glyphicon-hryvnia' in elem.find('span')['class']:
                    try:
                        salary = elem.find_all('b')[0].get_text().replace('\u202f', ' ')
                    except IndexError:
                        salary = 'не указано'
                elif 'glyphicon-company' in elem.find('span')['class']:
                    company = elem.find_all('b')[0].get_text()

            # print(salary)
            result.append([title, company, conditions, salary, job_description])

            json_result.append({'Job':
                {
                    'Vacancy': title,
                    'Компания': company,
                    'Conditions': conditions,
                    'Salary': salary,
                    'Description': job_description.replace('\n', ''),
                }
            })

        save_info(result)  # as .txt
        insert_info(result)  # into sqlite db
        save_json(json_result)  # as .json

        page += 1


main()

