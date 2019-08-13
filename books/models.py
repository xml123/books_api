from django.db import models

# Create your models here.

#分类
class Category(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

#作者
class Author(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

#小说
class Book(models.Model):
	#小说名
	title = models.CharField(max_length=100)

	#小说链接
	url = models.CharField(max_length=100, blank=True)

	#小说封面图
	book_img = models.CharField(max_length=100, blank=True)

	# #创建时间
	#created_time = models.DateTimeField(blank=True)
	# #小说的赞
	# books_love = models.IntegerField(default=0)

	#小说收藏数
	# books_collect = models.CharField(max_length = 5000,blank=True)

	#小说简介
	book_abstract = models.CharField(max_length=500,blank=True)

	#一部小说只能有一个作者，但一个作者下面可以有许多小说，所以我们使用ForeignKey，即一对多的关系，分类也是如此
	author = models.ForeignKey(Author, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

#章节
class chapter(models.Model):

	#章节名
	name = models.CharField(max_length = 100)

	#章节id
	chapter_id = models.CharField(max_length=5000,blank=True)

	#章节链接
	chapter_url = models.CharField(max_length = 200)

	#章节内容
	chapter_text = models.TextField()

	#章节对应小说，小说下面有很多章节
	book_id = models.ForeignKey(Book, on_delete=models.CASCADE)

	def __str__(self):
		return self.name













