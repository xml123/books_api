from django.db import models

# Create your models here.
class Classify(models.Model):
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Visitor(models.Model):
    name = models.CharField(max_length=100, blank=True)
    avatar = models.CharField(max_length=100, blank=True)
    link = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Artical(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    view = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    classify = models.ForeignKey(Classify, on_delete=models.CASCADE)
    status =models.BooleanField(default=False)

    def __str__(self):
        return self.title

class ArticalMessage(models.Model):
    message = models.CharField(max_length=500)
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    artical = models.ForeignKey(Artical, on_delete=models.CASCADE)

    def __str__(self):
        return self.message

class LiveMessage(models.Model):
    message = models.CharField(max_length=500)
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)

    def __str__(self):
        return self.message

class Friends(models.Model):
    name = models.CharField(max_length=100)
    avatar = models.CharField(max_length=100)
    link = models.CharField(max_length=100, blank=True)
    abstract = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.name




















