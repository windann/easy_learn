import requests
from bs4 import BeautifulSoup


url = 'https://stepik.org/catalog?auth=registration&language=ru'
response = requests.get(url).content

html = BeautifulSoup(response, 'lxml')

courses_name = set([course.text.strip() for course in html.find_all('a', class_='course-promo-widget__title')])
print(courses_name)

with open('insert_in_db_files/courses.txt', 'w') as f:
    for elem in courses_name:
        f.write(elem + '\n')

