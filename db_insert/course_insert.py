from connection_with_db import conn_open, curr_execute, conn_close

conn = conn_open()


description = u"""Lorem Ipsum - это текст-"рыба", часто используемый в печати и вэб-дизайне. Lorem Ipsum является стандартной "рыбой" для текстов на латинице с начала XVI века. В то время некий безымянный печатник создал большую коллекцию размеров и форм шрифтов, используя Lorem Ipsum для распечатки образцов. Lorem Ipsum не только успешно пережил без заметных изменений пять веков, но и перешагнул в электронный дизайн. Его популяризации в новое время послужили публикация листов Letraset с образцами Lorem Ipsum в 60-х годах и, в более недавнее время, программы электронной вёрстки типа Aldus PageMaker, в шаблонах которых используется Lorem Ipsum."""

with open('insert_in_db_files/courses.txt', 'r') as f:
    for course_name in f.readlines():
        query = "INSERT INTO learn_app_course (name, description) VALUES ('{}', '{}')".format(course_name, description)
        curr_execute(conn[0], conn[1], query)

conn_close(conn[1])