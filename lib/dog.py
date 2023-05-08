import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed):
        self.id = None
        self.name= name
        self.breed = breed
    def create_table():
        sql = """
            CREATE TABLE IF NOT EXISTS dogs
            (id INTEGER PRIMARY KEY, name TEXT, breed TEXT)
        """
        CURSOR.execute(sql)
    def drop_table():
        sql = """
            DROP TABLE IF EXISTS dogs
        """
        CURSOR.execute(sql)
    def save(self):
        sql = """
            INSERT INTO dogs
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (self.id, self.name, self.breed))
        CONN.commit()
        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]
    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog
    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog
    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM dogs
        """
        all = CURSOR.execute(sql).fetchall()
        cls.all = [cls.new_from_db(row) for row in all]
        return cls.all
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM dogs
            WHERE name = ?
            LIMIT 1
        """
        dog = CURSOR.execute(sql, (name,)).fetchone()
        return cls.new_from_db(dog)
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM dogs
            WHERE id = ?
            LIMIT 1
        """
        dog = CURSOR.execute(sql, (id,)).fetchone()
        return cls.new_from_db(dog)
    @classmethod
    def find_or_create_by(cls, name, breed):
        if CURSOR.lastrowid == None:

            sql = """
                INSERT INTO dogs
                VALUES (?,?)
            """
            dog = CURSOR.execute(sql, (cls.id, name, breed))
            return cls.new_from_db(dog)
        else:
            sql = """
                SELECT *
                FROM dogs
                WHERE name = ? and breed = ?
                LIMIT 1
            """
            dog = CURSOR.execute(sql, (name,)).fetchone()
            return cls.new_from_db(dog)