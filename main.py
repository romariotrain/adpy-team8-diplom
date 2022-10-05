from msilib.schema import tables
from os import link
import psycopg2
import yaml
from db_postgresql import DataBase
from db_postgresql import Client


if __name__ == '__main__':  
    with open('config.yaml') as f:
        config = yaml.safe_load(f)
        TOKEN_VK = config['token_vk'] # Токен от бота VK
        PASSWORD_SQL = config['password_sql'] 

    # Создается подключение к БД через обьект conn. 
    # database - имя БД, user - имя при регистрации в postgress, password - пароль от user 
    with psycopg2.connect(database = "tinder_min", user = "postgres", password = PASSWORD_SQL) as conn:        
        # Через обьект cur создаются запросы к БД 
        with conn.cursor() as cur:            
            db = DataBase(conn, cur) 
            table = Client(conn, cur)

            # Создать необходимые таблицы в БД
            name_table = 'person'
            print(db.create_table(name_table))
            name_table = 'best_photo'
            print(db.create_table(name_table)) 
            name_table = 'selected'
            print(db.create_table(name_table)) 


            # Добавить новую запись
            vk_id = 1
            first_name = 'Ira'
            last_name = 'Smirnova'
            sex = 'girl'
            age = 50
            city = 'Москва'
            print(table.add_person(vk_id, first_name, last_name, sex, age, city))        

            # Добавить ссылку на фотографию
            vk_id = 1
            link_list = ['photo-86093450_456239309', 'photo-86093450_456239390', 'photo-86093450_456239111']
            for link in link_list:
                print(table.add_photo(vk_id, link))     

            # Добавить страницу в список избранных (создать пару)
            elector_id = 1
            favorite_id = 123
            print(table.add_favorite(elector_id, favorite_id))  

            # Выводит список избранных людей
            vk_id = 1
            print(table.outputs_list(vk_id))  


    conn.close()


