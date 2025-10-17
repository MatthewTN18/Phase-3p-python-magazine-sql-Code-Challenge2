from .database_utils import get_connection

class Author:
    def __init__(self, name, id=None):
        self._name = None
        self.name = name
        self.id = id
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Author name must be a non-empty string")
        self._name = value
    
    @classmethod
    def new_from_db(cls, row):
    
        if row is None:
            return None
        return cls(id=row[0], name=row[1])
    
    @classmethod
    def find_by_id(cls, id):
        #Find author by ID
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = %s", (id,))
        row = cursor.fetchone()
        conn.close()
        return cls.new_from_db(row)
    
    def save(self):
        #Save author to database 
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            if self.id is None:
                # Insert new author
                cursor.execute("INSERT INTO authors (name) VALUES (%s) RETURNING id", (self.name,))
                self.id = cursor.fetchone()[0]
            else:
                # Update existing author
                cursor.execute("UPDATE authors SET name = %s WHERE id = %s", (self.name, self.id))
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    def articles(self):
        #get all articles written by this author
        from .article import Article
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = %s", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article.new_from_db(row) for row in rows]
    
    def magazines(self):
        #Get magazines this author has written for
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = %s
        ''', (self.id,))
        from .magazine import Magazine
        rows = cursor.fetchall()
        conn.close()
        return [Magazine.new_from_db(row) for row in rows]
    
    def add_article(self, magazine, title):
        """Add a new article for this author"""
        from .article import Article
        article = Article(title, self, magazine)
        article.save()
        return article
    
    def topic_areas(self):
        #Get uniquemagazines author has written for
        magazines = self.magazines()
        return list(set(magazine.category for magazine in magazines))
    
    def __repr__(self):
        return f"<Author {self.id}: {self.name}>"