DATABASE = 'blog_test'
HOSTNAME = 'localhost'
PORT = 3306
USERNAME = 'root'
PASSWORD = 'Zhangping890'
SECRET_KEY = b'F4Q8zu7IKn8uJi'
DB_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
_admin_default_password = "Quark Team"