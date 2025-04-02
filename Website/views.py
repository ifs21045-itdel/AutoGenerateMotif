from django .shortcuts import render,redirect
from subprocess import run,PIPE
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.contrib import messages 
from django.core.files.storage import FileSystemStorage
from .models import MotifForm1
from django.contrib.auth.models import User
from .models import Post
from django.contrib.sessions.models import Session
from itertools import zip_longest
from .CheckModule import Check
from .CreateImageModule import CreateImageMotif
from .SaveModule import Save
from .MotifModule import Motif
from .zipModule import ZIP
from .deleteModule import Delete
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from PIL import Image
from django.http import HttpResponse
from django.conf import settings
from datetime import datetime
from .models import Motif   
from PIL import Image, ImageDraw, ImageOps
import zipfile
import time
import base64
import uuid
import os
import re
import io
import requests
import sys, os, re
import logging
import json


from django.utils.datastructures import MultiValueDictKeyError


@login_required(login_url='login')
def image(request):
    user = request.user
    status = user.is_staff
    
    if status == 0:
          status=None
    navlink = ['nav-link nav-link-1 ','nav-link nav-link-2 active','nav-link nav-link-3','nav-link nav-link-4']
    return render(request, 'home.html',{"status":status,'navlink1':navlink[0],'navlink2':navlink[1],'navlink3':navlink[2],'navlink4':navlink[3]})

@login_required(login_url='login')
def loading(request):
    user = request.user
    status = user.is_superuser

    if status == 1:
          Autentificate = 1
    users = User.objects.all()
    JumlahAkun = User.objects.count()
    
    jumlah_data = Session.objects.count()
    jumlah_Motif = MotifForm1.objects.count()

    return render(request, 'checkLoading.html',{'users':users,'status':Autentificate,'jmlOnline_user':jumlah_data,'jmlMotif':jumlah_Motif,'jmlAkun':JumlahAkun})

@login_required(login_url='login')
def UpdateUser(request, id):
     user = User.objects.get(id = id)

     return render(request, 'UpdateUser.html',{'user':user})

@login_required(login_url='login')
def updaterecord(request, id):
    staff = request.POST['staff']
    active = request.POST['active']
    admin = request.POST['admin']
    member = User.objects.get(id=id)
    member.is_staff = staff
    member.is_active = active
    member.is_superuser = admin
    member.save()
    messages.info(request, 'Data berhasil di ubah')

    return redirect('Monitoring')

@login_required(login_url='login')
def generator(request):
    # Pengolahan gambar motif
    if request.method == 'POST':
        # Ambil data gambar dari form atau sumber lain
        image = request.FILES.get('image')  # Misalnya gambar yang di-upload
        jmlBaris = request.POST.get('jmlBaris')
        user = request.user.username

        # Proses gambar menggunakan modul CreateImageMotif
        Image = CreateImageMotif(image, jmlBaris, user)  # Sesuaikan pemanggilan metode sesuai kebutuhan
        URLEdit, UrutanLidi = Image.imageEven()  # Ambil URL gambar yang dihasilkan
        URLEdit2, UrutanLidi2 = Image.imageEven()
        URLEdit3, UrutanLidi3 = Image.imageEven()
        URLEdit4, UrutanLidi4 = Image.imageEven()
        

        # Menyimpan URL gambar dalam session untuk diteruskan ke halaman kedua
        request.session['raw_url'] = URLEdit  # Simpan URL motif asal
        request.session['edit_url'] = URLEdit2  # Simpan URL hasil motif
        request.session['combined_motif_url'] = URLEdit3  # Simpan URL motif gabungan

        return redirect('gabungkan_motif')  # Redirect ke halaman gabungan motif setelah gambar diproses

    # Jika tidak ada pengolahan gambar, hanya tampilkan halaman awal
    navlink = ['nav-link nav-link-1 active', 'nav-link nav-link-2', 'nav-link nav-link-3', 'nav-link nav-link-4']
    return render(request, 'started.html', {'navlink1': navlink[0], 'navlink2': navlink[1], 'navlink3': navlink[2], 'navlink4': navlink[3]})

# external lama
@login_required(login_url='login')
def external(request):
    jmlBaris = request.POST.get('jmlBaris')
    Baris = "1"
    user = request.user
    username = user.username
    length = len(username)

    image = request.FILES['image']
    navlink = ['nav-link nav-link-1 ','nav-link nav-link-2 active','nav-link nav-link-3','nav-link nav-link-4']
    path = os.getcwd()

    fs = FileSystemStorage()
    filename = fs.save(image.name, image)
    fileurl = fs.open(filename)
    templateurl = fs.url(filename)

    # Memanggil Object Check
    Object = Check(str(fileurl), jmlBaris)

    # Cek format gambar
    formatStatus = Object.checkformat()
    if formatStatus == "0":
        messages.success(request, "Format file yang diproses hanya menerima jpg")
        return render(request, 'home.html', {"jmlBaris": jmlBaris, "status": None, 'navlink1':navlink[0], 'navlink2':navlink[1], 'navlink3':navlink[2], 'navlink4':navlink[3]})

    # Cek jumlah baris
    isOverRow = Object.checkrow()
    if isOverRow == "0":
        messages.success(request, "Jumlah baris yang dapat dihasilkan berkisar dari 2 hingga 40")
        return render(request, 'home.html', {"jmlBaris": jmlBaris, "status": None, 'navlink1':navlink[0], 'navlink2':navlink[1], 'navlink3':navlink[2], 'navlink4':navlink[3]})

    # Cek spesifikasi gambar
    state, imgHeight = Object.checkSpecImage1()
    if state == "0":
        return render(request,'failed.html',{'imgHeight': str(imgHeight)})

    state, imgWidth = Object.checkSpecImage2()
    jmlBaris = int(jmlBaris)
    if state == "0":
        return render(request,'failedWidth.html',{'imgWidth': str(imgWidth)})

    # Generate motif berdasarkan jumlah baris (genap atau ganjil)
    if jmlBaris % 2 == 0:
        Image = CreateImageMotif(str(fileurl), str(filename), str(jmlBaris), Baris, "4", username)
        URLEdit, UrutanLidi = Image.imageEven()
        URLEdit2, UrutanLidi2 = Image.imageEven()
        URLEdit3, UrutanLidi3 = Image.imageEven()
        URLEdit4, UrutanLidi4 = Image.imageEven()
    else:
        Image = CreateImageMotif(str(fileurl), str(filename), str(jmlBaris), Baris, "4", username)
        URLEdit, UrutanLidi = Image.imageOdd()
        URLEdit2, UrutanLidi2 = Image.imageOdd()
        URLEdit3, UrutanLidi3 = Image.imageOdd()
        URLEdit4, UrutanLidi4 = Image.imageOdd()

    # Simpan URL gambar ke dalam session agar bisa digunakan di halaman lain
    request.session['raw_url'] = templateurl
    request.session['edit_url'] = URLEdit
    request.session['edit_url2'] = URLEdit2
    request.session['edit_url3'] = URLEdit3
    request.session['edit_url4'] = URLEdit4

    jenisGenerate = ['Tabu Search', 'Greedy Search', 'Random Search', 'ACO']

    return render(request, 'motif.html', {
        'user': username,
        'jmlBaris': jmlBaris,
        'raw_url': templateurl,
        'edit_url': URLEdit,
        'urutan_lidi': UrutanLidi,
        'edit_url2': URLEdit2,
        'urutan_lidi2': UrutanLidi2,
        'edit_url3': URLEdit3,
        'urutan_lidi3': UrutanLidi3,
        'edit_url4': URLEdit4,
        'urutan_lidi4': UrutanLidi4,
        'jenis1': jenisGenerate[3],
        'jenis2': jenisGenerate[3],
        'jenis3': jenisGenerate[3],
        'jenis4': jenisGenerate[3],
        'navlink1': navlink[0],
        'navlink2': navlink[1],
        'navlink3': navlink[2],
        'navlink4': navlink[3]
    })

def save(self, *args, **kwargs):
    import logging
    logger = logging.getLogger(__name__)
    try:
        # Log sebelum menyimpan
        logger.info(f"Menyimpan motif ID: {self.id if self.id else 'baru'}")
        logger.info(f"Path gambar: {self.imgAfter.path if self.imgAfter else 'None'}")
        
        # Save
        super(MotifForm1, self).save(*args, **kwargs)
        
        # Log setelah menyimpan
        logger.info(f"Berhasil menyimpan motif ID: {self.id}")
    except Exception as e:
        # Log error
        logger.error(f"Gagal menyimpan motif: {str(e)}")
        raise

@login_required(login_url='login')
def PostImage(request):
        if request.method == 'POST':
            if request.POST.get('imgBefore') and request.POST.get('imgAfter') and request.POST.get('urutanLidi') and request.POST.get('jenisGenerate') and request.POST.get('jmlBaris') and request.POST.get('user'):
                    post=MotifForm1()
                    post.imgBefore= request.POST.get('imgBefore')
                    post.imgAfter= request.POST.get('imgAfter')
                    post.urutanLidi = request.POST.get('urutanLidi')
                    post.jenisGenerate = request.POST.get('jenisGenerate')
                    post.jmlBaris = request.POST.get('jmlBaris')
                    post.user = request.POST.get('user')
                    post.save()
                    
                    return render(request, 'success.html')  

            else:
                    return render(request,'success.html')

@login_required(login_url='login')
def createpost(request):
        if request.method == 'POST':
            if request.POST.get('title') and request.POST.get('content'):
                post=Post()
                post.title= request.POST.get('title')
                post.content= request.POST.get('content')
                post.save()
                
                return render(request, 'createpost.html')  

        else:
                return render(request,'createpost.html')

def tes(request):
    return render(request, 'createpost.html')

@login_required(login_url='login')
def Search(request):
    filter = request.POST.get('filter')
    f = request.POST.get('SearchMotif')
    user = request.user
    status = user.is_staff
    navlink = ['nav-link nav-link-1 ','nav-link nav-link-2','nav-link nav-link-3 active','nav-link nav-link-4']

    if status == 0:
          status=None
    if filter == "Jumlah Baris":
        motifForm = MotifForm1.objects.all().filter(jmlBaris__iexact=f).values().order_by('time').reverse()
        filter=['Jumlah Baris','Nama','Tanggal']
    elif filter == "Nama":
        motifForm = MotifForm1.objects.all().filter(user__icontains= f).values().order_by('time').reverse()
        filter=['Nama','Jumlah Baris','Tanggal']
    elif filter == "Tanggal":
        motifForm = MotifForm1.objects.all().filter(time__icontains=f).values().order_by('time').reverse()
        filter=['Tanggal','Nama','Jumlah Baris']

    if (motifForm == ""):
         motifForm = None
    
    context = {"motifForm" : motifForm, "typeFilter1": filter[0], "typeFilter2": filter[1], "typeFilter3": filter[2], "valueFilter": f, "status":status,'navlink1':navlink[0],'navlink2':navlink[1],'navlink3':navlink[2],'navlink4':navlink[3]}
    if(f == ''):
         return redirect('list1')
    return render(request,"search.html", context)


@login_required(login_url='login')
def show(request):
    user = request.user
    status = user.is_staff
    navlink = ['nav-link nav-link-1 ', 'nav-link nav-link-2', 'nav-link nav-link-3 active', 'nav-link nav-link-4']
    if status == 0:
        status = None
    
    motifForm = MotifForm1.objects.all().values().order_by('time').reverse()
    paginator = Paginator(motifForm, 9)  # 9 gambar per halaman

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Dapatkan jumlah halaman total
    total_pages = paginator.num_pages

    # Hitung nomor halaman yang akan ditampilkan
    start_page = max(page_obj.number - 1, 1)
    end_page = min(start_page + 2, total_pages)

    # Sesuaikan start_page jika end_page kurang dari 3 halaman dan total_pages lebih dari 3
    if end_page - start_page < 2 and total_pages > 3:
        start_page = max(end_page - 2, 1)

    page_range = range(start_page, end_page + 1)

    context = {
        "motifForm": page_obj,
        'page_range': page_range,
        "status": status,
        'navlink1': navlink[0],
        'navlink2': navlink[1],
        'navlink3': navlink[2],
        'navlink4': navlink[3]
    }

    return render(request, "ListMotif.html", context)

@login_required(login_url='login')
def tagName(request, user):
    username = request.user
    status = username.is_staff
    navlink = ['nav-link nav-link-1 ','nav-link nav-link-2','nav-link nav-link-3 active','nav-link nav-link-4']
    if status == 0:
          status=None
    
    motifForm = MotifForm1.objects.all().filter(user__iexact= user).values().order_by('time').reverse()
        

    context = {"motifForm":motifForm,"status":status,'navlink1':navlink[0],'navlink2':navlink[1],'navlink3':navlink[2],'navlink4':navlink[3]}

    return render(request, "searchTag.html", context)

@login_required(login_url='login')
def tagJmlBaris(request, jmlBaris):
    username = request.user
    status = username.is_staff
    navlink = ['nav-link nav-link-1 ','nav-link nav-link-2','nav-link nav-link-3 active','nav-link nav-link-4']
    if status == 0:
          status=None
    
    # Tambahkan pengecekan nilai khusus
    if jmlBaris == 'N/A':
        # Khusus untuk motif gabungan
        motifForm = MotifForm1.objects.all().filter(jenisGenerate='combine').values().order_by('time').reverse()
    else:
        # Untuk motif non-gabungan
        motifForm = MotifForm1.objects.all().filter(jmlBaris__iexact=jmlBaris).values().order_by('time').reverse()

    context = {"motifForm":motifForm,"status":status,'navlink1':navlink[0],'navlink2':navlink[1],'navlink3':navlink[2],'navlink4':navlink[3]}

    return render(request, "searchTag.html", context)

@login_required(login_url='login')
def tagWaktu(request, time):
    username = request.user
    status = username.is_staff
    navlink = ['nav-link nav-link-1 ','nav-link nav-link-2','nav-link nav-link-3 active','nav-link nav-link-4']
    if status == 0:
          status=None
    time = time[0:10]
    motifForm = MotifForm1.objects.all().filter(time__icontains= time).values().order_by('time').reverse()
        

    context = {"motifForm":motifForm,"status":status,'navlink1':navlink[0],'navlink2':navlink[1],'navlink3':navlink[2],'navlink4':navlink[3]}

    return render(request, "searchTag.html", context)

@login_required(login_url='login')

def create_grid_image_from_combined_motif(image_path, output_path):
    """
    Membuat gambar grid hitam-putih dari motif gabungan
    """
    try:
        # Buka gambar
        with Image.open(image_path) as img:
            # Konversi ke grayscale
            img_gray = img.convert('L')
            
            # Binarisasi (konversi ke hitam-putih)
            threshold = 128
            img_binary = img_gray.point(lambda p: 255 if p > threshold else 0)
            
            # Simpan ke output path
            img_binary.save(output_path)
            
            return output_path
    except Exception as e:
        print(f"Error creating grid image: {e}")
        return None
@login_required(login_url='login')
def motif(request, id):
    try:
        motif = MotifForm1.objects.get(id=id)
        user = request.user
        status = user.is_superuser
        status1 = user.is_staff
        navlink = ['nav-link nav-link-1 ','nav-link nav-link-2','nav-link nav-link-3 active','nav-link nav-link-4']
        
        if status1 == 0:
            status1 = None
        if status == 0:
            status = None
        
        # Periksa apakah ini adalah motif gabungan
        is_combined = motif.jenisGenerate == "combine"
        
        # Dapatkan path file gambar
        img_path = os.path.join(settings.MEDIA_ROOT, motif.imgAfter.lstrip('/'))
        if not os.path.exists(img_path):
            img_path = os.path.join(settings.BASE_DIR, motif.imgAfter.lstrip('/'))
        
        # Siapkan direktori untuk grid dan lainnya
        grid_dir = os.path.join(settings.MEDIA_ROOT, 'grids')
        slice_dir = os.path.join(settings.MEDIA_ROOT, f'slices/motif_{motif.id}')
        
        os.makedirs(grid_dir, exist_ok=True)
        os.makedirs(slice_dir, exist_ok=True)
        
        # Buat atau dapatkan grid dan red line image
        grid_filename = f"grid_motif_{motif.id}.png"
        red_filename = f"red_motif_{motif.id}.png"
        grid_path = os.path.join(grid_dir, grid_filename)
        red_path = os.path.join(grid_dir, red_filename)
        
        # Periksa ukuran gambar dan lakukan penyesuaian jika terlalu besar
        if os.path.exists(img_path):
            try:
                with Image.open(img_path) as img:
                    width, height = img.size
                    
                    # Jika gambar terlalu besar, resize
                    if width > 600 or height > 800:
                        # Simpan gambar asli sebagai backup
                        backup_path = img_path.replace('.png', '_original.png')
                        shutil.copy2(img_path, backup_path)
                        
                        # Hitung ukuran baru dengan mempertahankan rasio aspek
                        max_width = 600
                        max_height = 800
                        
                        if width > max_width:
                            ratio = max_width / width
                            new_width = max_width
                            new_height = int(height * ratio)
                            
                            if new_height > max_height:
                                ratio = max_height / new_height
                                new_height = max_height
                                new_width = int(new_width * ratio)
                        elif height > max_height:
                            ratio = max_height / height
                            new_height = max_height
                            new_width = int(width * ratio)
                        
                        # Resize gambar
                        img_resized = img.resize((new_width, new_height), Image.LANCZOS)
                        img_resized.save(img_path)
                        
                        # Perlu regenerasi grid dan red line
                        if os.path.exists(grid_path):
                            os.remove(grid_path)
                        if os.path.exists(red_path):
                            os.remove(red_path)
            except Exception as e:
                print(f"Error processing image size: {str(e)}")
        
        # Cek jika file grid sudah ada, jika tidak, buat baru
        if not os.path.exists(grid_path) and os.path.exists(img_path):
            with Image.open(img_path) as img:
                # Buat grid
                grid_img = img.copy().convert('RGB')
                draw = ImageDraw.Draw(grid_img)
                
                width, height = grid_img.size
                grid_size = 10
                
                # Gambar garis grid
                for x in range(0, width, grid_size):
                    draw.line((x, 0, x, height), fill=(100, 100, 100), width=1)
                
                for y in range(0, height, grid_size):
                    draw.line((0, y, width, y), fill=(100, 100, 100), width=1)
                
                # Simpan grid
                grid_img.save(grid_path)
        
        # Cek jika file red line sudah ada, jika tidak, buat baru
        if not os.path.exists(red_path) and os.path.exists(grid_path):
            with Image.open(grid_path) as img:
                red_img = img.copy()
                draw = ImageDraw.Draw(red_img)
                
                width, height = red_img.size
                y_mid = height // 2
                
                # Gambar garis merah
                draw.line((0, y_mid, width, y_mid), fill=(255, 0, 0), width=3)
                
                # Simpan red line
                red_img.save(red_path)
        
        # Ambil urutan lidi
        try:
            if motif.urutanLidi:
                lidi_sequence = motif.urutanLidi.split(',')
                Urutan_Lidi = [int(x) for x in lidi_sequence]
            else:
                # Jika tidak ada urutan lidi, buat default
                row_count = int(motif.jmlBaris)
                Urutan_Lidi = list(range(1, row_count + 1))
        except:
            # Handle error dengan membuat urutan default
            Urutan_Lidi = list(range(1, 10))
        
        # Buat slice jika belum ada
        Slice = []
        if os.path.exists(img_path):
            with Image.open(img_path) as img:
                width, height = img.size
                row_count = len(Urutan_Lidi)
                slice_height = height // row_count
                
                for i in range(row_count):
                    slice_filename = f"slice_{i+1}.png"
                    slice_path = os.path.join(slice_dir, slice_filename)
                    
                    # Buat slice jika belum ada
                    if not os.path.exists(slice_path):
                        y_top = i * slice_height
                        y_bottom = min((i + 1) * slice_height, height)
                        
                        # Potong gambar
                        slice_img = img.crop((0, y_top, width, y_bottom))
                        slice_img.save(slice_path)
                    
                    # Tambahkan ke list
                    Slice.append(f"/media/slices/motif_{motif.id}/{slice_filename}")
        
        # Buat ZIP file untuk download
        zip_dir = os.path.join(settings.MEDIA_ROOT, 'zips')
        os.makedirs(zip_dir, exist_ok=True)
        
        zip_filename = f"motif_{motif.id}.zip"
        zip_path = os.path.join(zip_dir, zip_filename)
        
        if not os.path.exists(zip_path):
            with zipfile.ZipFile(zip_path, 'w') as zf:
                if os.path.exists(img_path):
                    zf.write(img_path, arcname="motif.png")
                if os.path.exists(grid_path):
                    zf.write(grid_path, arcname="motif_grid.png")
                if os.path.exists(red_path):
                    zf.write(red_path, arcname="motif_red_line.png")
                
                # Tambahkan slice
                for i in range(len(Slice)):
                    slice_path = os.path.join(slice_dir, f"slice_{i+1}.png")
                    if os.path.exists(slice_path):
                        zf.write(slice_path, arcname=f"slice_{i+1}.png")
        
        # Pisahkan urutan lidi untuk tampilan
        UrutanLidi_even = []
        UrutanLidi_odd = []
        
        for i in range(len(Urutan_Lidi)):
            if i % 2 == 0:
                UrutanLidi_even.append(Urutan_Lidi[i])
            else:
                UrutanLidi_odd.append(Urutan_Lidi[i])
        
        # Buat Slice2 untuk grid yang sama dengan Slice
        Slice2 = Slice.copy()
        
        # Pisahkan slice untuk tampilan
        Slice_even = []
        Slice_odd = []
        Slice2_even = []
        Slice2_odd = []
        
        for i in range(len(Slice)):
            if i % 2 == 0:
                Slice_even.append(Slice[i])
                Slice2_even.append(Slice2[i])
            else:
                Slice_odd.append(Slice[i])
                Slice2_odd.append(Slice2[i])
        
        # Buat UrutanMotif sama dengan Urutan_Lidi
        UrutanMotif = Urutan_Lidi.copy()
        UrutanMotif_even = UrutanLidi_even.copy()
        UrutanMotif_odd = UrutanLidi_odd.copy()
        
        # Buat data untuk template
        myList = list(zip_longest(Slice_even, UrutanLidi_even, Slice_odd, UrutanLidi_odd))
        myList2 = list(zip_longest(Slice2_even, UrutanMotif_even, Slice2_odd, UrutanMotif_odd))
        
        # URL relatif untuk template
        grid_url = f"/media/grids/{grid_filename}"
        red_url = f"/media/grids/{red_filename}"
        zip_url = f"/media/zips/{zip_filename}"
        
        return render(request, 'lihatMotif.html', {
            'motif': motif,
            'Lidi': grid_url,
            'RedLine': red_url,
            'zip': zip_url,
            'UrutanLidi': Urutan_Lidi,
            'urutanAsliLidi': motif.urutanLidi,
            'GridHelp': grid_url,
            'SliceLidi': myList,
            'SliceMotif': myList2,
            'status': status,
            'status1': status1,
            'navlink1': navlink[0],
            'navlink2': navlink[1],
            'navlink3': navlink[2],
            'navlink4': navlink[3]
        })
        
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"Error in motif view: {error_detail}")
        messages.error(request, f"Error: {str(e)}")
        return redirect('list1')
    
@login_required(login_url='login')
def regenerate_motif(request, id):
    try:
        motif = MotifForm1.objects.get(id=id)
        
        # Untuk motif gabungan
        if motif.jenisGenerate == "combine":
            # Ambil path gambar
            img_path = os.path.join(settings.BASE_DIR, motif.imgAfter.lstrip('/'))
            
            # Regenerasi grid dan red line
            with Image.open(img_path) as img:
                width, height = img.size
                
                # Buat grid
                grid_path = img_path.replace(".png", "_grid.png")
                grid_img = img.copy()
                draw = ImageDraw.Draw(grid_img)
                grid_size = 10
                
                for x in range(0, width, grid_size):
                    draw.line((x, 0, x, height), fill=127)
                
                for y in range(0, height, grid_size):
                    draw.line((0, y, width, y), fill=127)
                
                grid_img.save(grid_path)
                
                # Buat red line
                red_path = img_path.replace(".png", "_red.png")
                red_img = grid_img.convert('RGB')
                draw = ImageDraw.Draw(red_img)
                y_mid = height // 2
                draw.line((0, y_mid, width, y_mid), fill=(255, 0, 0), width=3)
                red_img.save(red_path)
            
            # Regenerasi slice
            slice_dir = os.path.join(settings.MEDIA_ROOT, f"slices/motif_{motif.id}")
            if os.path.exists(slice_dir):
                shutil.rmtree(slice_dir)
            os.makedirs(slice_dir, exist_ok=True)
            
            # Potong gambar menjadi slice
            lidi_sequence = motif.urutanLidi.split(',')
            row_count = len(lidi_sequence)
            
            with Image.open(img_path) as img:
                width, height = img.size
                for i in range(row_count):
                    slice_height = height // row_count
                    y_top = i * slice_height
                    y_bottom = min((i + 1) * slice_height, height)
                    
                    slice_img = img.crop((0, y_top, width, y_bottom))
                    slice_file = os.path.join(slice_dir, f"slice_{i+1}.png")
                    slice_img.save(slice_file)
            
            # Regenerasi zip file
            zip_path = os.path.join(settings.MEDIA_ROOT, f"zips/motif_{motif.id}.zip")
            if os.path.exists(zip_path):
                os.remove(zip_path)
            
            with zipfile.ZipFile(zip_path, 'w') as zf:
                zf.write(img_path, arcname="combined_motif.png")
                zf.write(grid_path, arcname="motif_grid.png")
                zf.write(red_path, arcname="motif_red_line.png")
                
                for i in range(1, row_count + 1):
                    slice_file = os.path.join(slice_dir, f"slice_{i}.png")
                    if os.path.exists(slice_file):
                        zf.write(slice_file, arcname=f"slice_{i}.png")
            
            messages.success(request, "Motif berhasil diregenerate")
            return redirect('list', id=id)
        
        else:
            # Untuk motif biasa
            messages.success(request, "Motif berhasil diregenerate")
            return redirect('list', id=id)
    
    except Exception as e:
        import traceback
        print(f"Error regenerating motif: {str(e)}")
        print(traceback.format_exc())
        messages.error(request, f"Gagal meregenerate motif: {str(e)}")
        return redirect('list1')
@login_required(login_url='login')
def deleteMotif(request):

    id = request.POST.get('DeleteImage')
    prod = MotifForm1.objects.get(id = id)
    if len(prod.imgAfter)>0:
        ObjecDelete1 = Delete(str(prod.imgAfter))
        ObjecDelete2 = Delete(str(prod.imgBefore))

        Image1 =  ObjecDelete1.DeleteMotif()
        Image2 =  ObjecDelete2.DeleteMotif()
        
        messages.success(request, "Motif berhasil dihapus")
    prod.delete()
    
    return redirect('list1')

@login_required(login_url='login')    
def showTest(request):
    
    motifForm = Post.objects.all().values()
    context = {"motifForm":motifForm}

    return render(request, "ListMotif.html", context)

@login_required(login_url='login')
def help(request):
    
    navlink = ['nav-link nav-link-1 ','nav-link nav-link-2','nav-link nav-link-3','nav-link nav-link-4 active']
    return render(request, "help.html", {'navlink1':navlink[0],'navlink2':navlink[1],'navlink3':navlink[2],'navlink4':navlink[3]})

@login_required(login_url='login')
def help_generate(request):

    navlink = ['nav-link nav-link-1 ','nav-link nav-link-2','nav-link nav-link-3','nav-link nav-link-4 active']
    return render(request, "help-generator.html", {'navlink1':navlink[0],'navlink2':navlink[1],'navlink3':navlink[2],'navlink4':navlink[3]})

@login_required(login_url='login')
def help_lidi(request):

    navlink = ['nav-link nav-link-1 ','nav-link nav-link-2','nav-link nav-link-3','nav-link nav-link-4 active']
    return render(request, "help-lidi.html", {'navlink1':navlink[0],'navlink2':navlink[1],'navlink3':navlink[2],'navlink4':navlink[3]})

@login_required(login_url='login')
def help_search(request):

    navlink = ['nav-link nav-link-1 ','nav-link nav-link-2','nav-link nav-link-3','nav-link nav-link-4 active']
    return render(request, "help-search.html", {'navlink1':navlink[0],'navlink2':navlink[1],'navlink3':navlink[2],'navlink4':navlink[3]})

@login_required(login_url='login')
def help_download(request):

    navlink = ['nav-link nav-link-1 ','nav-link nav-link-2','nav-link nav-link-3','nav-link nav-link-4 active']
    return render(request, "help-download.html", {'navlink1':navlink[0],'navlink2':navlink[1],'navlink3':navlink[2],'navlink4':navlink[3]})

def SignupPage(request):
    if request.user.is_authenticated:
         return redirect('home')
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        
        if not re.match(r"^[a-zA-Z0-9_]+$", uname):
            # username is not valid, return an error response
            messages.info(request, 'Username tidak menerima adanya spasi dan simbol lainnya kecuali tanda "_"')
            return render(request,'signup.html', {'uname': uname,'email': email,'pass1': pass1,'pass2': pass2 })
        
        if pass1==pass2:
            if User.objects.filter(username=uname).exists():
                messages.info(request, 'Username sudah pernah digunakan')
                return render(request,'signup.html', {'uname': uname,'email': email,'pass1': pass1,'pass2': pass2 })
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email sudah pernah digunakan')
                return render(request,'signup.html', {'uname': uname,'email': email,'pass1': pass1,'pass2': pass2 })
            elif int(len(pass1)<8):
                 messages.info(request, 'Kata sandi minimal 8 karakter')
                 return render(request, 'signup.html', {'uname': uname,'email': email,'pass1': pass1,'pass2': pass2 })
            else:
                user = User.objects.create_user(username=uname, email=email, password=pass1)
                user.save()
                
                user=authenticate(request,username=uname,password=pass1)
                login(request,user)
                
                messages.success(request, 'Akun Berhasil Dibuat')
                
                return redirect('home')
                    
        else:
            messages.info(request, 'Kata Sandi dan Konfirmasi Kata Sandi yang dimasukkan berbeda')
            return render(request,'signup.html', {'uname': uname,'email': email,'pass1': pass1,'pass2': pass2 })
    else:
        return render(request, 'signup.html')


def LoginPage(request):
    if request.user.is_authenticated:
         return redirect('home')
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.warning(request, 'Username atau Kata Sandi Salah', extra_tags='alert')
            return redirect('login')

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def gabungkan_motif(request):
    # Ambil URL gambar dari session
    raw_url = request.session.get('raw_url')
    edit_url = request.session.get('edit_url')
    edit_url2 = request.session.get('edit_url2')
    edit_url3 = request.session.get('edit_url3')
    edit_url4 = request.session.get('edit_url4')

    # Pastikan semua gambar tersedia sebelum merender halaman
    if not raw_url or not edit_url:
        messages.error(request, "Beberapa gambar motif tidak tersedia.")
        return redirect('generator')

    return render(request, 'gabung-motif.html', {
        'raw_url': raw_url,
        'edit_url': edit_url,
        'edit_url2': edit_url2 if edit_url2 else edit_url,
        'edit_url3': edit_url3 if edit_url3 else edit_url,
        'edit_url4': edit_url4 if edit_url4 else edit_url
    })
@csrf_exempt
def save_combined_motif(request):
    if request.method == 'POST':
        try:
            # Ambil data gambar dari request
            img_data = request.POST.get('imgCombined')
            
            if not img_data:
                return JsonResponse({'status': 'error', 'message': 'Data gambar tidak ditemukan'}, status=400)
            
            # Proses data gambar (base64)
            format, imgstr = img_data.split(';base64,')
            ext = format.split('/')[-1]
            
            # Buat nama file unik
            file_name = f"combined_motif_{uuid.uuid4()}.png"
            file_path = os.path.join(settings.MEDIA_ROOT, 'combined_motifs', file_name)
            
            # Pastikan direktori ada
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Simpan gambar base64 ke file
            with open(file_path, "wb") as f:
                f.write(base64.b64decode(imgstr))
            
            # Resize gambar ke ukuran yang lebih wajar
            with Image.open(file_path) as img:
                # Tentukan ukuran maksimal yang wajar
                max_width = 600
                max_height = 800
                
                # Hitung ukuran baru dengan mempertahankan rasio aspek
                width, height = img.size
                if width > max_width:
                    ratio = max_width / width
                    new_width = max_width
                    new_height = int(height * ratio)
                    
                    # Pastikan tinggi tidak melebihi batas
                    if new_height > max_height:
                        ratio = max_height / new_height
                        new_height = max_height
                        new_width = int(new_width * ratio)
                elif height > max_height:
                    ratio = max_height / height
                    new_height = max_height
                    new_width = int(width * ratio)
                else:
                    # Gambar sudah cukup kecil
                    new_width, new_height = width, height
                
                # Resize gambar
                img_resized = img.resize((new_width, new_height), Image.LANCZOS)
                
                # Binarisasi dengan kualitas yang lebih baik
                img_gray = img_resized.convert('L')
                threshold = 128
                img_binary = img_gray.point(lambda p: 255 if p > threshold else 0)
                
                # Simpan gambar yang sudah diproses
                img_binary.save(file_path)
            
            # Hitung jumlah baris berdasarkan tinggi gambar
            with Image.open(file_path) as img:
                
                height = img.height
                # Tentukan jumlah baris yang proporsional
                grid_size = 10
                row_count = height // grid_size
                if row_count < 2:
                    row_count = 2  # Minimal 2 baris
                
                # Buat grid untuk motif
                grid_filename = f"grid_{file_name}"
                grid_path = os.path.join(settings.MEDIA_ROOT, 'grids', grid_filename)
                os.makedirs(os.path.dirname(grid_path), exist_ok=True)
                
                # Buat gambar grid
                grid_img = img.copy().convert('RGB')
                draw = ImageDraw.Draw(grid_img)
                
                width, height = grid_img.size
                
                # Gambar garis vertikal dan horizontal grid
                for x in range(0, width, grid_size):
                    draw.line((x, 0, x, height), fill=(100, 100, 100), width=1)
                
                for y in range(0, height, grid_size):
                    draw.line((0, y, width, y), fill=(100, 100, 100), width=1)
                
                # Simpan grid
                grid_img.save(grid_path)
                
                # Buat garis merah tengah
                red_filename = f"red_{file_name}"
                red_path = os.path.join(settings.MEDIA_ROOT, 'grids', red_filename)
                
                red_img = grid_img.copy()
                draw = ImageDraw.Draw(red_img)
                
                # Gambar garis tengah merah
                y_mid = height // 2
                draw.line((0, y_mid, width, y_mid), fill=(255, 0, 0), width=3)
                
                # Simpan gambar dengan garis merah
                red_img.save(red_path)
            
            # Buat urutan lidi dengan format yang benar
            lidi_sequence = [i for i in range(1, row_count + 1)]
            
            # Terapkan pola urutan seperti di CreateImageMotif
            if row_count % 2 == 0:  # Genap
                mid = len(lidi_sequence) // 2
                lidi_reversed = lidi_sequence[mid:]
                lidi_reversed.reverse()
                full_sequence = lidi_sequence[:mid] + lidi_reversed
            else:  # Ganjil
                mid = len(lidi_sequence) // 2
                lidi_first = lidi_sequence[:mid]
                lidi_mid = [lidi_sequence[mid]]
                lidi_last = lidi_sequence[mid+1:]
                lidi_last.reverse()
                full_sequence = lidi_first + lidi_mid + lidi_last
            
            # Konversi ke string
            lidi_string = ",".join(map(str, full_sequence))
            
            # Buat folder untuk slice
            slice_dir = os.path.join(settings.MEDIA_ROOT, 'slices', f"combined_{uuid.uuid4()}")
            os.makedirs(slice_dir, exist_ok=True)
            
            # Potong gambar menjadi slice sesuai baris
            with Image.open(file_path) as img:
                width, height = img.size
                slice_height = height // row_count
                
                for i in range(row_count):
                    y_top = i * slice_height
                    y_bottom = min((i + 1) * slice_height, height)
                    
                    # Potong gambar
                    slice_img = img.crop((0, y_top, width, y_bottom))
                    slice_path = os.path.join(slice_dir, f"slice_{i+1}.png")
                    slice_img.save(slice_path)
            
            # Buat URL relatif
            relative_path = f"/media/combined_motifs/{file_name}"
            grid_relative = f"/media/grids/{grid_filename}"
            red_relative = f"/media/grids/{red_filename}"
            
            # Simpan ke database
            motif = MotifForm1()
            motif.imgBefore = relative_path  # Gunakan path yang sama untuk asal dan hasil
            motif.imgAfter = relative_path
            motif.urutanLidi = lidi_string
            motif.jenisGenerate = "combine"
            motif.jmlBaris = str(row_count)
            motif.user = request.user.username
            motif.save()
            
            # Buat file ZIP untuk unduhan
            zip_dir = os.path.join(settings.MEDIA_ROOT, 'zips')
            os.makedirs(zip_dir, exist_ok=True)
            
            zip_filename = f"combined_motif_{motif.id}.zip"
            zip_path = os.path.join(zip_dir, zip_filename)
            
            with zipfile.ZipFile(zip_path, 'w') as zf:
                zf.write(file_path, arcname="combined_motif.png")
                zf.write(grid_path, arcname="motif_grid.png")
                zf.write(red_path, arcname="motif_red_line.png")
                
                # Tambahkan slice ke ZIP
                for i in range(row_count):
                    slice_path = os.path.join(slice_dir, f"slice_{i+1}.png")
                    if os.path.exists(slice_path):
                        zf.write(slice_path, arcname=f"slice_{i+1}.png")
            
            return JsonResponse({
                'status': 'success', 
                'message': 'Motif berhasil disimpan',
                'id': motif.id
            })
            
        except Exception as e:
            import traceback
            print(f"Error saving combined motif: {str(e)}")
            print(traceback.format_exc())
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Metode tidak diizinkan'}, status=405)

# views.py - perbaikan untuk fungsi upload gambar
@login_required(login_url='login')
def upload_image(request):
    if request.method == 'POST':
        try:
            # Pastikan ada file yang diupload
            if 'file' not in request.FILES:
                return JsonResponse({'error': 'Tidak ada file yang diupload'}, status=400)
            
            image = request.FILES['file']
            
            # Buat direktori jika belum ada
            import os
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            
            # Simpan file dengan nama unik
            import uuid
            filename = f"{uuid.uuid4()}.png"
            full_path = os.path.join(upload_dir, filename)
            
            with open(full_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            
            # Kembalikan URL untuk akses gambar
            image_url = os.path.join(settings.MEDIA_URL, 'uploads', filename)
            return JsonResponse({'imageUrl': image_url})
        
        except Exception as e:
            import traceback
            print(f"Error upload gambar: {str(e)}")
            print(traceback.format_exc())
            return JsonResponse({'error': f'Gagal mengupload gambar: {str(e)}'}, status=500)
    
    return JsonResponse({'error': 'Metode tidak diizinkan'}, status=405)
def ubah_warna(request):
    combined_motif_urls = request.session.get('combined_motifs', [])  # Mengambil motif yang sudah dipilih dari session

    if not combined_motif_urls:
        messages.error(request, "Motif tidak ditemukan!")

    return render(request, 'ubah-warna.html', {'combined_motif_urls': combined_motif_urls})

@login_required(login_url='login')
def ubah_warna(request, id):
    motif = MotifForm1.objects.get(id=id)
    # Ambil gambar motif yang akan diubah warnanya
    img_url = motif.imgAfter  # Misalnya, kamu ingin mengubah warna dari imgAfter
    
    if request.method == 'POST':
        warna = request.POST.get('warna')
        # Proses perubahan warna (misalnya menggunakan Python Image Library atau metode lain)
        # Di sini kamu bisa menambahkan logika untuk mengubah warna motif sesuai pilihan pengguna
        
        # Simpan gambar yang sudah diubah warna, misalnya:
        # motif.imgAfter = img_url_with_new_color
        motif.save()
        
        return render(request, 'ubah_warna_success.html', {'motif': motif, 'warna': warna})

    return render(request, 'ubah_warna.html', {'motif': motif, 'img_url': img_url})

@login_required(login_url='login')
def ubah_warna(request, id):
    motif = MotifForm1.objects.get(id=id)
    
    # Jika menggunakan gambar yang digabungkan, bisa menggunakan combined_motif_urls atau motif.imgAfter
    combined_motif_urls = [motif.imgAfter]  # Misalnya hanya satu gambar motif yang digabungkan
    
    if request.method == 'POST':
        warna_motif = request.POST.get('warnaMotif')
        # Lakukan pemrosesan untuk mewarnai motif sesuai dengan warna yang dipilih
        # Setelah pewarnaan, simpan gambar baru dan tampilkan hasilnya
        
        motif.imgAfter = 'path_to_new_colored_image'  # Ganti dengan path gambar yang sudah diwarnai
        motif.save()
        
        return render(request, 'ubah_warna_success.html', {'motif': motif, 'warna': warna_motif})
    
    return render(request, 'ubah-warna.html', {'combined_motif_urls': combined_motif_urls})
    
@csrf_exempt
def upload_base64_image(request):
    if request.method == 'POST':
        try:
            data_url = request.POST.get('image')
            if not data_url:
                return JsonResponse({'status': 'error', 'message': 'Image data not found'}, status=400)
            
            # Parse data URL
            format, imgstr = data_url.split(';base64,')
            ext = format.split('/')[-1]
            
            # Buat nama file unik
            filename = f"combined_motif_{uuid.uuid4()}.{ext}"
            filepath = os.path.join(settings.MEDIA_ROOT, 'combined_motifs', filename)
            
            # Pastikan direktori ada
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Simpan gambar ke file
            with open(filepath, "wb") as f:
                f.write(base64.b64decode(imgstr))
            
            # Kembalikan path yang dapat diakses melalui web
            web_path = f"/media/combined_motifs/{filename}"
            return JsonResponse({'status': 'success', 'path': web_path})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

def generate_lidi_sequence(image_height):
    """Menghasilkan urutan lidi berdasarkan tinggi gambar"""
    # Hitung jumlah baris berdasarkan tinggi gambar
    row_count = image_height // 10  # Asumsi 10px per baris
    
    # Buat urutan lidi (contoh: 1,2,3,4,5,...)
    lidi_sequence = ",".join([str(i) for i in range(1, row_count + 1)])
    return lidi_sequence