from faker import Faker
from faker.providers import profile
import random
import requests
import sqlite3
from datetime import datetime

fake = Faker('ru_RU')

base ='/Users/anja/projects/easy_learn/easy_learn/db.sqlite3'
conn = sqlite3.connect(base)
cur = conn.cursor()


def save_photo(profile_sex):
    num = random.randint(1, 100)

    if profile_sex == 'M':
        sex = 'men'
    else:
        sex = 'women'

    url = 'https://randomuser.me/api/portraits/{}/{}.jpg'.format(sex, num)
    file_name = str(num) + '.jpg'
    r = requests.get(url, allow_redirects=True)
    open('media/media/' + file_name, 'wb').write(r.content)
    file_name = 'media/' + str(num) + '.jpg'
    return file_name

for _ in range(5):
    user = fake.simple_profile()
    profile_sex = user['sex']
    username = user['username']
    email = user['mail']
    first_name = user['name'].split()[0]
    last_name = user['name'].split()[1]
    avatar = save_photo(profile_sex)
    registration_date = datetime.today()
    password = fake.password()
    user_type = random.randint(1,2)
    group_id = 1

    cur.execute("""INSERT INTO learn_app_user ( username, 
                                                first_name, 
                                                last_name, 
                                                avatar,
                                                group_id, 
                                                user_type_id, 
                                                password,  
                                                email,
                                                is_superuser, 
                                                is_staff, 
                                                is_active, 
                                                date_joined) 
                    VALUES ('{}', '{}', '{}', '{}','{}', '{}', '{}', '{}','{}', '{}', '{}', '{}');""".format(

        username, first_name, last_name, avatar, group_id, user_type, password, email, False, False, False, registration_date))

    conn.commit()
conn.close()

# cur.execute("PRAGMA TABLE_INFO(learn_app_user);")
# cur.execute("SELECT name FROM sqlite_master WHERE type='table';")

"""
('django_migrations',)
('sqlite_sequence',)
('django_content_type',)
('auth_group',)
('auth_group_permissions',)
('auth_permission',)
('learn_app_user_groups',)
('learn_app_user_user_permissions',)
('learn_app_usertype',)
('django_admin_log',)
('django_session',)
('learn_app_course',)
('learn_app_lesson',)
('learn_app_question',)
('learn_app_test',)
('learn_app_user',)"""
