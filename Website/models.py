from django.db import models
from django.contrib.auth.models import User
class Motif(models.Model):
    user = models.CharField(max_length=100)
    raw_url = models.CharField(max_length=255)
    edit_url = models.CharField(max_length=255)
    Urutan = models.CharField(max_length=255)
    jenis = models.CharField(max_length=50)
    jmlBaris = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Motif by {self.user} - {self.time}"



class MotifForm(models.Model):
    imgBefore = models.TextField()
    imgAfter  = models.TextField()
    urutanLidi = models.TextField()

class MotifForm1(models.Model):
    imgBefore = models.TextField()
    imgAfter = models.TextField()
    urutanLidi = models.TextField()
    jenisGenerate = models.TextField()
    jmlBaris = models.TextField()
    user = models.TextField()
    time = models.DateTimeField(auto_now_add= True)
    slice = models.TextField()
    coloredImage = models.TextField()
    coloredImagecombined = models.TextField()
    sliceColoredImage = models.TextField()
    class Meta:
        db_table = 'website_motifform1'
    def __str__(self):
        return f"Motif by {self.user} - {self.time}" 

    

class Post(models.Model):
    title= models.TextField()
    content= models.TextField()

# pengenmbangan untuk select optiom
class Motif(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imgBefore = models.ImageField(upload_to='images/')  # Gambar sebelum motif dibuat
    imgAfter = models.ImageField(upload_to='images/')   # Gambar setelah motif dibuat
    urutanLidi = models.CharField(max_length=100)        # Urutan lidi yang digunakan
    jenisGenerate = models.CharField(max_length=50)      # Jenis algoritma/generate yang digunakan
    jmlBaris = models.IntegerField()                     # Jumlah baris yang dihasilkan
    time = models.DateTimeField(auto_now_add=True)       # Waktu pembuatan motif