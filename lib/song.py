from test import cursor, conn

#Define the Song Class
class Song:

    def __init__(self, song_title, genre, id=None):
        self.id = id
        self.song_title = song_title
        self.genre = genre

#Property and setter methods for the Song attributes
    @property
    def song_title(self):
        return self._song_title
    
    @song_title.setter
    def song_title(self, value):
        if not value:
            raise ValueError("song title cannot be empty")
        self._song_title= value
    
    @property
    def genre(self):
        return self._genre
    
    @genre.setter
    def genre(self, value):
        if not value:
            raise ValueError("genre cannot be empty")
        self._genre=value

#Calling the class methods ORM using CRUD operations specifically(create,delete,get all and find by id) as per the brief  
#
# Creating The Song Table    
    @classmethod
    def create_table(cls):
        '''This method will create a song table in our db'''
        sql = """
            CREATE TABLE IF NOT EXISTS song (
            id INTEGER PRIMARY KEY,
            song_title TEXT NOT NULL,
            genre TEXT NOT NULL
            )
        """

        cursor.execute(sql)
        conn.commit()

#Dropping the Song Table
    @classmethod
    def drop_table(cls):
        sql = """
           DROP TABLE IF EXISTS song
        """ 
        cursor.execute(sql)
        conn.commit()


#Saving the song to the database  
    def save(self):
        if self.id is None:
            sql = """
                INSERT INTO song (song_title, genre)
                VALUES (?, ?)
            """
            cursor.execute(sql, (self.song_title, self.genre))
            self.id = cursor.lastrowid
        else:
            sql = """
                UPDATE song
                SET song_title = ?, genre = ?
                WHERE id = ?
            """
            cursor.execute(sql, (self.song_title, self.genre, self.id))
        conn.commit()

#Deleting the song from the database
    def delete(self):
        if self.id is None:
            raise ValueError("song does not exist")
        sql = "DELETE FROM song WHERE id = ?"
        cursor.execute(sql, (self.id,))
        conn.commit()
        self.id = None
   
#Create and save a new song
    @classmethod
    def create (cls,song_title, genre):
        song = cls(id, song_title, genre)
        song.save()
        return song

#Get all songs from the database
    @classmethod
    def get_all(cls):
        sql= "SELECT * FROM song"
        cursor.execute(sql)
        rows = cursor.fetchall()
        return [cls(id=row[0], song_title= row[1], genre=row[2]) for row in rows]

#Find a song by ID    
    @classmethod
    def find_by_id(cls,id):
        sql = "SELECT * FROM song WHERE id = ?"
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        if row:
            return cls(
                id=row[0], 
                song_title=row[1],
                genre=row[2])
        return None

#String representation of the song    
    def __repr__(self):
        return f"<song('{self.song_title}', '{self.genre}'>"
         