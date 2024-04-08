from django.db import models

#Create Model Here
class MotifForm(models.Model):
    imgBefore = models.TextField()
    imgAfter  = models.TextField()
    urutanLidi = models.TextField()

class MotifForm1(models.Model):
    imgBefore = models.TextField()
    imgAfter  = models.TextField()
    urutanLidi = models.TextField()
    jenisGenerate = models.TextField()
    jmlBaris = models.TextField()
    user = models.TextField()
    time = models.DateTimeField(auto_now_add= True)

    

class Post(models.Model):
    title= models.TextField()
    content= models.TextField()