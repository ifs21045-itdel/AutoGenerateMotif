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

# pengenmbangan untuk select optiom
# class Motif(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     imgBefore = models.ImageField(upload_to='images/')  # Gambar sebelum motif dibuat
#     imgAfter = models.ImageField(upload_to='images/')   # Gambar setelah motif dibuat
#     urutanLidi = models.CharField(max_length=100)        # Urutan lidi yang digunakan
#     jenisGenerate = models.CharField(max_length=50)      # Jenis algoritma/generate yang digunakan
#     jmlBaris = models.IntegerField()                     # Jumlah baris yang dihasilkan
#     time = models.DateTimeField(auto_now_add=True)       # Waktu pembuatan motif