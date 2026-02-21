from django.apps import AppConfig
import MySQLdb
from django.conf import settings
import sys


def create_database_if_not_exists():
    """Create MySQL database if it doesn't exist."""
    db_config = settings.DATABASES['default']
    
    # Only proceed if using MySQL
    if db_config['ENGINE'] != 'django.db.backends.mysql':
        return
    
    db_name = db_config['NAME']
    db_user = db_config['USER']
    db_password = db_config['PASSWORD']
    db_host = db_config.get('HOST', 'localhost')
    db_port = int(db_config.get('PORT', 3306))
    
    try:
        # Connect to MySQL server without specifying a database
        connection = MySQLdb.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            passwd=db_password
        )
        cursor = connection.cursor()
        
        # Check if database exists
        cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
        result = cursor.fetchone()
        
        if not result:
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"[OK] Database '{db_name}' created successfully.")
        else:
            print(f"[OK] Database '{db_name}' already exists.")
        
        cursor.close()
        connection.close()
        
    except MySQLdb.Error as e:
        print(f"[ERROR] Error creating database: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    
    def ready(self):
        """Called when Django starts. Create database if it doesn't exist."""
        # Only create database when running server/migrations, not during tests
        if 'runserver' in sys.argv or 'migrate' in sys.argv or 'makemigrations' in sys.argv:
            create_database_if_not_exists()