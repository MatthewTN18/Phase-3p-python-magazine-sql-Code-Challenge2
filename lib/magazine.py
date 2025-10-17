from .database_utils import get_connection

class Magazine:
    def __init__(self, name, category, id=None):
        self._name = None
        self._category = None
        self.name = name  
        self.category = category  
        self.id = id
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not (2 <= len(value) <= 16):
            raise ValueError("Magazine name must be a string between 2 and 16 characters")
        self._name = value
    
    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Magazine category must be a non-empty string")
        self._category = value
    
    @classmethod
    def new_from_db(cls, row):
        #Create Magazine instance 
        if row is None:
            return None
        return cls(id=row[0], name=row[1], category=row[2])
    
    @classmethod
    def find_by_id(cls, id):
        #Find by ID
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = %s", (id,))
        row = cursor.fetchone()
        conn.close()
        return cls.new_from_db(row)
    
    def save(self):
        #Save magazine to database
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            if self.id is None:
                # Insert new magazine
                cursor.execute(
                    "INSERT INTO magazines (name, category) VALUES (%s, %s) RETURNING id",
                    (self.name, self.category)
                )
                self.id = cursor.fetchone()[0]
            else:
                # Update existing magazine
                cursor.execute(
                    "UPDATE magazines SET name = %s, category = %s WHERE id = %s",
                    (self.name, self.category, self.id)
                )
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    def articles(self):
        #Get all articles in this magazine
        from .article import Article
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = %s", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article.new_from_db(row) for row in rows]
    
    def contributors(self):
        #Get all authors who have written for this magazine
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT a.* FROM authors a
            JOIN articles art ON a.id = art.author_id
            WHERE art.magazine_id = %s
        ''', (self.id,))
        from .author import Author
        rows = cursor.fetchall()
        conn.close()
        return [Author.new_from_db(row) for row in rows]
    
    def article_titles(self):
        #Get all article titles for this magazine
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM articles WHERE magazine_id = %s", (self.id,))
        titles = [row[0] for row in cursor.fetchall()]
        conn.close()
        return titles
    
    
    @classmethod
    def top_publisher(cls):
        #Find the magazine with the most articles
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.id
            ORDER BY COUNT(a.id) DESC
            LIMIT 1
        ''')
        row = cursor.fetchone()
        conn.close()
        return cls.new_from_db(row) if row else None
    
    def __repr__(self):
        return f"<Magazine {self.id}: {self.name} ({self.category})>"