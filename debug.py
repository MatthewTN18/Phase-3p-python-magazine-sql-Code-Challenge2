from lib.database_utils import create_tables, get_connection
from lib.author import Author
from lib.magazine import Magazine
from lib.article import Article

def setup_database():
    """Test database setup"""
    print("Setting up PostgreSQL database...")
    
    # Testing the connection
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Test PostgreSQL version
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"Connected to: {version[0]}")
        
        # Create tables
        create_tables()
        print("Database setup completed successfully!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error during database setup: {e}")
        return False
    
    return True

def test_author_class():
    
    print("\n Testing Author Class ")
    
    # Test creating authors
    author1 = Author("Michael Njuguna")
    author1.save()
    print(f"Created author: {author1}")
    
    author2 = Author("Sarah Kimani")
    author2.save()
    print(f"Created author: {author2}")
    
    
    found_author = Author.find_by_id(author1.id)
    print(f"Found author by ID: {found_author}")
    
    # Test validation
    try:
        invalid_author = Author("")
        print("ERROR: Should have raised validation error")
    except ValueError as e:
        print(f"Correctly caught validation error: {e}")
    
    print("Author class tests passed")
    return author1, author2


def test_magazine_class():
    
    print("\n Testing Magazine Class ")
    
    
    mag1 = Magazine("Tech Weekly", "Technology")
    mag1.save()
    print(f"Created magazine: {mag1}")
    
    mag2 = Magazine("Science Digest", "Science")
    mag2.save()
    print(f"Created magazine: {mag2}")
    
    
    found_mag = Magazine.find_by_id(mag1.id)
    print(f"Found magazine by ID: {found_mag}")
    
    
def test_article_class(author1, author2, mag1, mag2):
    
    print("\n Testing Article Class ")
    
    # Test creating articles
    article1 = Article("Python Programming Basics", author1, mag1)
    article1.save()
    print(f"Created article: {article1}")
    
    article2 = Article("Advanced Machine Learning", author1, mag1)
    article2.save()
    print(f"Created article: {article2}")
    
    
    # Test finding article by ID
    found_article = Article.find_by_id(article1.id)
    print(f"Found article by ID: {found_article}")
    
    # Test validation 
    try:
        invalid_article = Article("Hi", author1, mag1)
        print("ERROR: Should have raised validation error")
    except ValueError as e:
        print(f" Correctly caught short title: {e}")
    
    
    try:
        long_title = "This is a very long article title that is so long that it is impractical blah blah blab blaah blah"
        invalid_article = Article(long_title, author1, mag1)
        print("ERROR: Should have raised validation error")
    except ValueError as e:
        print(f" Correctly caught long title: {e}")
    
    
    try:
        invalid_article = Article("Valid Title", "not an author", mag1)
        print("ERROR: Should have raised validation error")
    except ValueError as e:
        print(f" Correctly caught invalid author: {e}")
    
    print("Article class tests passed")
    return article1, article2, article3

def test_author_relationships(author1, author2, mag1, mag2):
    
    print("\n Testing Author Relationship Methods ")
    
    # Test articles() method
    johns_articles = author1.articles()
    print(f"{author1.name}'s articles: {[article.title for article in johns_articles]}")
    
    # Test magazines() method  
    johns_magazines = author1.magazines()
    print(f"{author1.name} writes for: {[mag.name for mag in johns_magazines]}")
    
    # Test add_article() method
    new_article = author1.add_article(mag1, "New Python Features")
    print(f"Added new article: {new_article}")
    
    # Test topic_areas() method
    johns_categories = author1.topic_areas()
    print(f"{author1.name}'s topic areas: {johns_categories}")
    
    print("Author relationship tests passed")


def test_magazine_relationships(author1, author2, mag1, mag2):
    
    print("\n Testing Magazine Relationship Methods ")
    
    # Test articles() 
    tech_articles = mag1.articles()
    print(f"Articles in {mag1.name}: {[article.title for article in tech_articles]}")
    
    # Test contributors() 
    tech_contributors = mag1.contributors()
    print(f"Contributors to {mag1.name}: {[author.name for author in tech_contributors]}")
    
    # Test article_titles() 
    tech_titles = mag1.article_titles()
    print(f"Article titles in {mag1.name}: {tech_titles}")
    
    # Test contributing_authors() 
    contributing_authors = mag1.contributing_authors()
    print(f"Contributing authors to {mag1.name}: {[author.name for author in contributing_authors]}")
    
    # Test top_publisher() 
    top_magazine = Magazine.top_publisher()
    print(f"Top publisher: {top_magazine}")
    
    print("Magazine relationship tests passed")

if __name__ == "__main__":
    if setup_database():
        
        author1, author2 = test_author_class()
        test_article_class(author1, author2, mag1, mag2)
        test_author_relationships(author1, author2, mag1, mag2)
        test_magazine_relationships(author1, author2, mag1, mag2)
        
        print("\n All tests completed")