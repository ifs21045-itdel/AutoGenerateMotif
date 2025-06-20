from django.db import models
from django.contrib.auth.models import User
class Motif(models.Model):
    user = models.CharField(max_length=100, blank=True, null=True)
    raw_url = models.CharField(max_length=255, blank=True, null=True)
    edit_url = models.CharField(max_length=255, blank=True, null=True)
    Urutan = models.CharField(max_length=255, blank=True, null=True)  # Sesuaikan dengan database
    jenis = models.CharField(max_length=50, blank=True, null=True)
    jmlBaris = models.CharField(max_length=20, blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Motif by {self.user} - {self.time}"



class MotifForm(models.Model):
    imgBefore = models.TextField()
    imgAfter  = models.TextField()
    urutanLidi = models.TextField()

class MotifForm1(models.Model):
    imgBefore = models.TextField(blank=True, null=True)
    imgAfter = models.TextField(blank=True, null=True)
    urutanLidi = models.TextField(blank=True, null=True)
    jenisGenerate = models.TextField(blank=True, null=True)
    jmlBaris = models.TextField(blank=True, null=True)
    user = models.TextField(blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    slice = models.TextField(blank=True, null=True)
    coloredImage = models.TextField(blank=True, null=True)
    coloredImagecombined = models.TextField(blank=True, null=True)
    sliceColoredImage = models.TextField(blank=True, null=True)
    urutanLidiAsal = models.TextField(blank=True, null=True)
    jenisKain = models.TextField(blank=True, null=True)  # Tambahkan field ini
    jenisProduk = models.TextField(blank=True, null=True)
    class Meta:
        db_table = 'website_motifform1'
    def __str__(self):
        return f"Motif by {self.user} - {self.time}" 

    

class Post(models.Model):
    title= models.TextField()
    content= models.TextField()
