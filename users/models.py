from django.db import models

# Create your models here.
#用户
class Users(models.Model):
	openid = models.CharField(max_length=100,blank=True)
	session_key = models.CharField(max_length=100,blank=True)
	code = models.CharField(max_length=100,blank=True)

	book = models.ManyToManyField('books.Book',blank=True) #多对多，收藏的书

	def __str__(self):
		return self.openid

#用户书架上次读到的章节
class BookCapter(models.Model):
	users = models.ForeignKey(Users,on_delete=models.CASCADE)
	bookid = models.CharField(max_length=100)
	capterid = models.CharField(max_length=100)

	def __str__(self):
		return self.bookid

#用户的一些阅读习惯
class UserReadStatus(models.Model):
	users = models.ForeignKey(Users,on_delete=models.CASCADE)
	read_status = models.CharField(max_length=100,blank=True)
	word_size = models.CharField(max_length=100,blank=True)
	bg_color = models.CharField(max_length=100,blank=True)

	def __str__(self):
		return self.read_status