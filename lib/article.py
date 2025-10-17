
from .database_utils import get_connection

class Article:
    def __init__(self, title, author, magazine, id=None):
        self._title = None
        self.title = title  
        self.author = author
        self.magazine = magazine
        self.id = id
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not (5 <= len(value) <= 50):
            raise ValueError("Article title must be a string between 5 and 50 characters")
        self._title = value
    
    @property
    def author(self):
        return self._author
    
    @author.setter
    def author(self, value):
        from .author import Author
        if not isinstance(value, Author):
            raise ValueError("Author must be an instance of Author class")
        self._author = value
    
    @property
    def magazine(self):
        return self._magazine
    
    @magazine.setter
    def magazine(self, value):
        from .magazine import Magazine
        if not isinstance(value, Magazine):
            raise ValueError("Magazine must be an instance of Magazine class")
        self._magazine = value
    
    @classmethod
    def new_from_db(cls, row):
        
        if row is None:
            return None
        
        from .author import Author
        from .magazine import Magazine
        
        # Fetch author and magazine objects
        author = Author.find_by_id(row[2])
        magazine = Magazine.find_by_id(row[3])
        
        return cls(id=row[0], title=row[1], author=author, magazine=magazine)
    
    @classmethod
    def find_by_id(cls, id):
        #find article by ID
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = %s", (id,))
        row = cursor.fetchone()
        conn.close()
        return cls.new_from_db(row)
    
    def save(self):
        #Save article to database 
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            if self.id is None:
                # Insert new article
                cursor.execute(
                    "INSERT INTO articles (title, author_id, magazine_id) VALUES (%s, %s, %s) RETURNING id",
                    (self.title, self.author.id, self.magazine.id)
                )
                self.id = cursor.fetchone()[0]
            else:
                # Update existing article
                cursor.execute(
                    "UPDATE articles SET title = %s, author_id = %s, magazine_id = %s WHERE id = %s",
                    (self.title, self.author.id, self.magazine.id, self.id)
                )
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    def __repr__(self):
        return f"<Article {self.id}: '{self.title}' by {self.author.name} in {self.magazine.name}>"