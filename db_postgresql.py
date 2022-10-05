from sqlalchemy import null


class DataBase:
    """Класс для создания таблиц БД"""
    def __init__(self, conn, cur):
        self.conn = conn 
        self.cur = cur

    def create_table(self, name: str) -> str:
        if name == 'person':   
            # cur.execute - метод для написания запросов с помощью cur(курсор)                            
            self.cur.execute("""
                            CREATE TABLE IF NOT EXISTS person(
                            person_id   SERIAL       PRIMARY KEY,
                            vk_id       INTEGER      UNIQUE NOT NULL,                
                            first_name  VARCHAR(30)  NOT NULL,   
                            last_name   VARCHAR(30)  NOT NULL,
                            sex         VARCHAR(8)   NOT NULL,
                            age         SMALLINT,
                            city        VARCHAR(50)
                            );
                            """)
            self.conn.commit()  # только после commit или fetch(one,many,all) происходит отправка запроса в БД
            return f'Создана таблица {name}'
        
        elif name == 'best_photo':                          
            self.cur.execute("""
                            CREATE TABLE IF NOT EXISTS best_photo(
                            photo_id    SERIAL       PRIMARY KEY,
                            person_id   INTEGER      NOT NULL     REFERENCES person(vk_id),                
                            link_photo  VARCHAR(200) NOT NULL     UNIQUE    
                            );                 
                            """)
            self.conn.commit()
            return f'Создана таблица {name}'
        
        elif name == 'selected':                          
            self.cur.execute("""
                            CREATE TABLE IF NOT EXISTS selected(
                            selected_id  SERIAL   PRIMARY KEY,
                            elector_id   INTEGER  NOT NULL     REFERENCES person(vk_id),
                            favorite_id  INTEGER  NOT NULL     REFERENCES person(vk_id)       
                            );                 
                            """)
            self.conn.commit()
            return f'Создана таблица {name}'
        
        else:
            return 'Ошибка! Возможные имена "person", "best_photo", "selected"'


class Client:
    """Класс для работы с БД"""
    def __init__(self, conn, cur):
        self.conn = conn 
        self.cur = cur

    def checking_available(self, vk_id:int) -> bool:
        'Метод возвращет True если в базе есть такой id и Folse если нет'
        self.cur.execute("""
                        SELECT vk_id 
                        FROM   person
                        WHERE  vk_id = %s;
                        """ % (vk_id,))
        return bool(self.cur.fetchall())

    def add_person(self, vk_id: int, first_name: str, last_name: str, sex: str, age: int=null, city: str=null)-> str:
        'Добавляет запись в таблицу person'
        flag = self.checking_available(vk_id)        
        if not flag:      
            self.cur.execute("""
                            INSERT INTO person (vk_id, first_name, last_name, sex, age, city) 
                            VALUES ('%s', '%s', '%s', '%s', '%s', '%s');                
                            """ % (vk_id, first_name, last_name, sex, age, city))
            self.conn.commit()                 
            return 'Данные занесены'
        else:    
            self.cur.execute("""
                            UPDATE person
                            SET first_name = '%s', last_name = '%s', age = '%s', city = '%s'
                            WHERE vk_id = %s;
                            """ % (first_name, last_name, age, city, vk_id))
            self.conn.commit()                 
            return 'Данные обновлены'   

    def outputs_list(self, vk_id: int,) -> str:
        'Выводит список избранных людей'
        with self.conn.cursor() as cur: 
            cur.execute("""
                        SELECT vk_id, first_name, last_name
                        FROM   client
                        FULL   JOIN selected 
                                ON  selector_id = person_id
                        WHERE  selected_id = %s;
                        """% (vk_id,))
            self.conn.commit()  
            return 'Получены все совпадения'
            
    def add_photo(self, vk_id: int)-> str:
        'Добавляет запись в таблицу best_photo'
        pass

    def add_favorite(self, elector_id: int, favorite_id: int)-> str:
        'Добавить страницу в список избранных'
        pass
