1.	python@3.7.0、mysql@5.7.22

2.	终端工作目录运行sudo django-admin startproject xxxx;

3.	配置数据库	
	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.mysql',
	        'NAME': 'books',
	        'USER': 'root',
	        'PASSWORD': 'xml123',
	        'HOST': '127.0.0.1',
	        'PORT': '3306',
	    }
	}

	__init__.py文件配置：
	import pymysql
	pymysql.install_as_MySQLdb()

4.	迁移数据库：
	python3 manage.py makemigrations
	python3 manage.py migrate
	