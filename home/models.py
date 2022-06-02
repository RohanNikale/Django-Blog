from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Post(models.Model):
    # sno=models.AutoField(primary_key=True ,default=1)
    name = models.CharField(max_length=20 ,default='Rohan Nikale')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=1000000)
    image = models.ImageField(upload_to='blogimage',default='rohan')
    view=models.IntegerField(default=0)
    datetime= models.DateTimeField(default=now)
    def __str__(self):
        return self.title

class postComment(models.Model):
    sno=models.AutoField(primary_key=True)
    comment =models.TextField(max_length=255)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    parent=models.ForeignKey('self', on_delete=models.CASCADE,null=True)
    datetime= models.DateTimeField(default=now)
    def __str__(self):
        return self.comment[0:100]

