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
import shutil
from django.utils.timezone import now
from django.utils.crypto import get_random_string
from django.utils.text import get_valid_filename

from django.utils.datastructures import MultiValueDictKeyError


# #@login_required(login_url='login')
def image(request):
    
    print(f"DEBUG: generator view called")
    # user = request.user
    # status = user.is_staff
    status = 1
    if status == 0:
          status=None
    navlink = ['nav-link nav-link-1 ','nav-link nav-link-2 active','nav-link nav-link-3','nav-link nav-link-4']
    return render(request, 'home.html',{"status":status,'navlink1':navlink[0],'navlink2':navlink[1],'navlink3':navlink[2],'navlink4':navlink[3]})

# #@login_required(login_url='login')
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

# #@login_required(login_url='login')
def UpdateUser(request, id):
     user = User.objects.get(id = id)

     return render(request, 'UpdateUser.html',{'user':user})

# #@login_required(login_url='login')
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

# #@login_required(login_url='login')
def generator(request):
    
    if request.method == 'POST':
    
        image = request.FILES.get('image')  
        jmlBaris = request.POST.get('jmlBaris')
        user = "admin"

        
        Image = CreateImageMotif(image, jmlBaris, user)  
        URLEdit, UrutanLidi = Image.imageEven()  
        URLEdit2, UrutanLidi2 = Image.imageEven()
        URLEdit3, UrutanLidi3 = Image.imageEven()
        URLEdit4, UrutanLidi4 = Image.imageEven()
        

    
        request.session['raw_url'] = URLEdit  
        request.session['edit_url'] = URLEdit2
        request.session['combined_motif_url'] = URLEdit3  
        request.session['jumlahasal'] = jmlBaris
        request.session['urutannyalidi'] = UrutanLidi
        return redirect('gabungkan_motif')  

    
    navlink = ['nav-link nav-link-1 active', 'nav-link nav-link-2', 'nav-link nav-link-3', 'nav-link nav-link-4']
    return render(request, 'started.html', {'navlink1': navlink[0], 'navlink2': navlink[1], 'navlink3': navlink[2], 'navlink4': navlink[3]})


# external lama
# #@login_required(login_url='login')
def external(request):
    jmlBaris = request.POST.get('jmlBaris')
    jumlahasal = jmlBaris  
    request.session['jumlahasal'] = jumlahasal
    Baris = "1"
    user = "admin"
    username = "admin"
    length = len(username)
    url_raw_path = []
    print("DEBUG: POST received")
    print("DEBUG: POST =>", request.FILES['image'])
    image = request.FILES['image']
    imagesave = request.FILES['image']
    processed_image = enhance_image(imagesave)
    
    navlink = ['nav-link nav-link-1 ','nav-link nav-link-2 active','nav-link nav-link-3','nav-link nav-link-4']
    path = os.getcwd()
    fss = FileSystemStorage()
    filenames = fss.save(processed_image.name, processed_image)
    templateurls = fss.url(filenames)
    fs = FileSystemStorage()
    filename = fs.save(image.name, image)
    fileurl = fs.open(filename)
    templateurl = fs.url(filename)

    
    Object = Check(str(fileurl), jmlBaris)

    
    formatStatus = Object.checkformat()
    if formatStatus == "0":
        messages.success(request, "Format file yang diproses hanya menerima jpg")
        return render(request, 'home.html', {"jmlBaris": jmlBaris, "status": None, 'navlink1':navlink[0], 'navlink2':navlink[1], 'navlink3':navlink[2], 'navlink4':navlink[3]})

    
    isOverRow = Object.checkrow()
    if isOverRow == "0":
        messages.success(request, "Jumlah baris yang dapat dihasilkan berkisar dari 2 hingga 40")
        return render(request, 'home.html', {"jmlBaris": jmlBaris, "status": None, 'navlink1':navlink[0], 'navlink2':navlink[1], 'navlink3':navlink[2], 'navlink4':navlink[3]})

    
    state, imgHeight = Object.checkSpecImage1()
    if state == "0":
        return render(request,'failed.html',{'imgHeight': str(imgHeight)})

    state, imgWidth = Object.checkSpecImage2()
    jmlBaris = int(jmlBaris)
    if state == "0":
        return render(request,'failedWidth.html',{'imgWidth': str(imgWidth)})
    # imgl = CreateImageMotif(str(fileurl), str(filename), str(jmlBaris), Baris, "4", username)
    # UrutanLidiRaw = imgl.imageUrutan()
    

    session_name = f"session_{uuid.uuid4()}"

    if jmlBaris % 2 == 0:
        Image = CreateImageMotif(str(fileurl), str(filename), str(jmlBaris), Baris, "4", username, session_name)
        UrutanLidiRaw, UrutanLidiIndex, url_raw_path = Image.imageOriginal()
        url_raw_path = [f"/media/{path}" for path in url_raw_path]  
        URLEdit, UrutanLidi = Image.imageEven()
        URLEdit2, UrutanLidi2 = Image.imageEven()
        URLEdit3, UrutanLidi3 = Image.imageEven()
        URLEdit4, UrutanLidi4 = Image.imageEven()
    else:
        Image = CreateImageMotif(str(fileurl), str(filename), str(jmlBaris), Baris, "4", username, session_name)
        UrutanLidiRaw, UrutanLidiIndex, url_raw_path = Image.imageOriginal()
        url_raw_path = [f"/media/{path}" for path in url_raw_path]  
        URLEdit, UrutanLidi = Image.imageOdd()
        URLEdit2, UrutanLidi2 = Image.imageOdd()
        URLEdit3, UrutanLidi3 = Image.imageOdd()
        URLEdit4, UrutanLidi4 = Image.imageOdd()

    print(f"UrutanLidiRaw: {UrutanLidiRaw}")

    UrutanLidi = [int(x) for x in UrutanLidi]
    UrutanLidiIndex = [int(x) for x in UrutanLidiIndex]
    UrutanLidi2 = [int(x) for x in UrutanLidi2]
    UrutanLidi3 = [int(x) for x in UrutanLidi3]
    UrutanLidi4 = [int(x) for x in UrutanLidi4]

    
    request.session['raw_url'] = templateurls
    request.session['raw_asal'] = UrutanLidiRaw       
    request.session['raw_lidi'] = UrutanLidiIndex 
    request.session['edit_url'] = URLEdit
    request.session['urutanasal'] = [int(x) for x in UrutanLidiIndex]
    request.session['urutan'] = [int(x) for x in UrutanLidi]
    request.session['urutan2'] = [int(x) for x in UrutanLidi2]
    request.session['urutan3'] = [int(x) for x in UrutanLidi3]
    request.session['urutan4'] = [int(x) for x in UrutanLidi4]
    request.session['edit_url2'] = URLEdit2
    request.session['edit_url3'] = URLEdit3
    request.session['edit_url4'] = URLEdit4
    request.session['list_lidi_path'] = url_raw_path
    request.session['session_name'] = session_name
    # request.session['gember'] = image
    request.session['jumlahasal'] = jumlahasal
    jenisGenerate = ['Tabu Search', 'Greedy Search', 'Random Search', 'ACO']

    return render(request, 'motif.html', {
        'user': username,
        'raw_lidi': UrutanLidiRaw,
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
        'jenis_generate': jenisGenerate[3],
        'navlink1': navlink[0],
        'navlink2': navlink[1],
        'navlink3': navlink[2],
        'navlink4': navlink[3],
        'list_lidi_path': url_raw_path,
        'session_name': session_name,
        'jumlahasal':jumlahasal
    })

# Penggabungan Motif
def enhance_image(uploaded_file): #Gambar yang diunggah akan diubah menjadi array NumPy dan diproses dengan OpenCV.
    import cv2
    import numpy as np
    from io import BytesIO
    from django.core.files.uploadedfile import InMemoryUploadedFile 


    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    # Membaca byte file menjadi gambar berwarna (BGR) agar bisa diproses OpenCV
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR) 

    # jumlah potongan vertikal gambar menjadi 5 bagian.
    num_slices = 5
    height, width = image.shape[:2] #mengambil ukuran tinggi dan lebar dari gambar
    slice_height = height // num_slices #mhitung tinggi tiap potongan gambar

    enhanced_slices = [] #buat list kosong untuk menyimpan potongan gambar yang diproses.

    for i in range(num_slices): #loop sebanyak jumlah potongan 
        y_start = i * slice_height #titik awal tinggi (y-axis) untuk potongan gambar ke-i
        y_end = height if i == num_slices - 1 else (i + 1) * slice_height
        slice_img = image[y_start:y_end, :]

        # Mengubah potongan gambar dari BGR ke grayscale untuk mempermudah thresholding.
        gray = cv2.cvtColor(slice_img, cv2.COLOR_BGR2GRAY)

        # Mengubah gambar grayscale menjadi hitam-putih (biner), threshold di 200.
        _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

        # Mengubah kembali gambar biner ke format 3 channel (BGR) agar bisa digabungkan nanti.
        result = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)

        enhanced_slices.append(result)
    # Menggabungkan semua potongan gambar hasil enhance secara vertikal jadi satu gambar utuh.
    enhanced_full = cv2.vconcat(enhanced_slices)

    # Mengubah gambar akhir (NumPy array) menjadi format JPEG dalam bentuk byte buffer.
    _, buffer = cv2.imencode('.jpg', enhanced_full)
    io_buf = BytesIO(buffer.tobytes())

   
    enhanced_file = InMemoryUploadedFile(
        file=io_buf,
        field_name='image',
        name='enhanced_' + uploaded_file.name,
        content_type='image/jpeg',
        size=io_buf.getbuffer().nbytes,
        charset=None
    )

    return enhanced_file



# def save(self, *args, **kwargs):
#     import logging
#     logger = logging.getLogger(__name__)
#     try:
#         # Log sebelum menyimpan
#         logger.info(f"Menyimpan motif ID: {self.id if self.id else 'baru'}")
#         logger.info(f"Path gambar: {self.imgAfter.path if self.imgAfter else 'None'}")
        
#         # Save
#         super(MotifForm1, self).save(*args, **kwargs)
        
#         # Log setelah menyimpan
#         logger.info(f"Berhasil menyimpan motif ID: {self.id}")
#     except Exception as e:
#         # Log error
#         logger.error(f"Gagal menyimpan motif: {str(e)}")
#         raise

def save(request):
    if request.method == "POST":
        try:
            jumlahasal = request.session.get("jumlahasal")
            
            # Ambil data dari form POST (bukan dari session statis)
            
            imgBefore = request.POST.get("image2")  # Motif asal
            imgAfter = request.POST.get("image3")   # Motif hasil yang dipilih
            urutanLidi = request.POST.get("urutan") # Urutan lidi yang dipilih
            jenisGenerate = request.POST.get("JenisGenerate")
            jmlBaris = request.POST.get("jmlBaris")
            user = request.POST.get("user")

            if not imgBefore or not imgAfter:
                return JsonResponse({
                    "status": "error",
                    "message": "Data motif tidak lengkap"
                })

            # Simpan motif ke database
            motif = MotifForm1(
                imgBefore=imgBefore,
                imgAfter=imgAfter,
                urutanLidi=urutanLidi,
                jenisGenerate=jenisGenerate,
                jmlBaris=jmlBaris,
                user=user,
            )
            motif.save()

            # Update session dengan data motif yang dipilih
            request.session['img_before'] = imgBefore
            request.session['img_after'] = imgAfter
            request.session['urutan'] = urutanLidi
            request.session['jenis'] = jenisGenerate
            request.session['jml_baris'] = jmlBaris
            request.session['user'] = user
            request.session['jumlahasal'] = jumlahasal
           
            return redirect('download_page')

        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            })
        
        
def download(request):
    context = {
        'raw_url1': request.session.get('img_before'),
        'raw_lidi': request.session.get('raw_lidi'),
        'raw_asal': request.session.get('raw_asal'),
        'edit_url1': request.session.get('img_after'),
        'Urutan': request.session.get('urutan'),
        'jenis': request.session.get('jenis'),
        'jmlBaris': request.session.get('jml_baris'),
        'user': request.session.get('user'),
    }
    return render(request, 'download.html', context)
        
def download(request):
    context = {
        'raw_url1': request.session.get('img_before'),
        'raw_lidi': request.session.get('raw_lidi'),
        'raw_asal': request.session.get('raw_asal'),
        'edit_url1': request.session.get('img_after'),
        'Urutan': request.session.get('urutan'),
        'jenis': request.session.get('jenis'),
        'jmlBaris': request.session.get('jml_baris'),
        'user': request.session.get('user'),
    }
    return render(request, 'download.html', context)
@csrf_exempt
def PostImage(request):
    if request.method == 'POST':
        print("DEBUG: POST received")
        print("DEBUG: FILES =>", request.FILES)
        print("DEBUG: POST =>", request.POST)

        print("request.POST.get(imgBefore) =>", request.POST.get('imgBefore'))
        print("request.POST.get(imgAfter) =>", request.POST.get('imgAfter'))
        print("request.POST.get(urutanLidi) =>", request.POST.get('urutanLidi'))
        print("request.POST.get(jenisGenerate) =>", request.POST.get('jenisGenerate'))
        print("request.POST.get(user) =>", request.POST.get('user'))

        # Validasi field wajib
        if all(request.POST.get(field) for field in ['imgBefore', 'imgAfter', 'urutanLidi', 'jenisGenerate', 'user']):
            urutlidi = request.POST.get('urutanLidi')
            urutlidi_list = urutlidi.split(',')
            jumlah_slice = len(urutlidi_list)

            imagegenerate_url = request.POST.get('imgAfter')
            image_path = os.path.join(settings.BASE_DIR, imagegenerate_url.lstrip('/'))
            hasil_slice_paths = []

            img = Image.open(image_path)
            width, height = img.size
            slice_height = height // jumlah_slice  # untuk slice vertikal

            post = MotifForm1()
            post.imgBefore = request.POST.get('imgBefore')
            post.imgAfter = request.POST.get('imgAfter')
            post.urutanLidi = urutlidi
            post.jenisGenerate = request.POST.get('jenisGenerate')
            post.jmlBaris = request.POST.get('jmlBaris', '0')  
            post.user = request.POST.get('user')
            raw_lidi = request.session.get('raw_lidi', [])
            post.urutanLidiAsal = ','.join(map(str, raw_lidi)) if raw_lidi else ''
            post.jenisKain = request.POST.get('jenisKain', '-')  # Default "-" jika tidak ada
            post.jenisProduk = request.POST.get('jenisProduk', '-')

            # Save the post object before accessing its ID
            post.save()

            output_dir = os.path.join(settings.MEDIA_ROOT, 'admin', 'hasilslice', 'motif'+str(post.id))
            os.makedirs(output_dir, exist_ok=True)

            for i in range(jumlah_slice):
                top = i * slice_height
                bottom = (i + 1) * slice_height if i != jumlah_slice - 1 else height
                box = (0, top, width, bottom)
                slice_img = img.crop(box)

                base_name = f"slice_{i+1}.png"
                save_path = os.path.join(output_dir, base_name)

                print(f"save_path: {save_path}")

                while os.path.exists(save_path):
                    random_suffix = get_random_string(6)
                    base_name = f"slice_{i+1}_{random_suffix}.png"
                    save_path = os.path.join(output_dir, base_name)

                slice_img.save(save_path)

                relative_path = f"{settings.MEDIA_URL}admin/hasilslice/{base_name}".replace('\\', '/')
                hasil_slice_paths.append(relative_path)

            postImageSlice = "@@".join(hasil_slice_paths) if hasil_slice_paths else ""

            # Simpan slice ke database
            post.slice = postImageSlice
            post.save()

            request.session['url_image_slice'] = postImageSlice

            # Upload ulang gambar jika dikirim lewat FILES (opsional)
            if 'file' in request.FILES:
                image = request.FILES['file']
                upload_dir = os.path.join(settings.MEDIA_ROOT, 'Uploads')
                os.makedirs(upload_dir, exist_ok=True)

                filename = image.name
                full_path = os.path.join(upload_dir, filename)

                with open(full_path, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)

                image_url = os.path.join(settings.MEDIA_URL, 'Uploads', filename).replace('\\', '/')
                post.imgBefore = image_url
                post.imgAfter = image_url
                post.save()

            print("DEBUG: Sukses simpan post dan slice.")
            return JsonResponse({
                'status': 'success',
                'motif_id': post.id  # Kembalikan ID motif yang baru disimpan
            })
        else:
            print("DEBUG: Ada field POST yang kosong.")
            return JsonResponse({
                'status': 'error',
                'message': 'Ada field yang kosong.'
            }, status=400)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Metode tidak diizinkan.'
        }, status=405)


@csrf_exempt
def PostImageGabungan(request):
    if request.method == 'POST':
        print("DEBUG: POST received")
        print("DEBUG: FILES =>", request.FILES)
        print("DEBUG: POST =>", request.POST)

        # Validasi wajib
        if all(request.POST.get(field) for field in ['imgBefore', 'urutanLidi', 'jenisGenerate', 'user', 'jenisKain', 'jenisProduk']):
            urutlidi = request.POST.get('urutanLidi')
            urutlidi_list = urutlidi.split(',')
            jumlah_slice = len(urutlidi_list)

            hasil_slice_paths = []
            output_dir_slice = os.path.join(settings.MEDIA_ROOT, 'hasilslice')
            os.makedirs(output_dir_slice, exist_ok=True)

            try:
                if 'file' in request.FILES:
                    image = request.FILES['file']
                    # Simpan gambar gabungan ke hasilfix/
                    hasilfix_dir = os.path.join(settings.MEDIA_ROOT, 'hasilfix')
                    os.makedirs(hasilfix_dir, exist_ok=True)

                    # Cek dan ganti nama jika duplikat
                    original_name = image.name
                    name, ext = os.path.splitext(original_name)
                    filename = original_name
                    filepath = os.path.join(hasilfix_dir, filename)

                    while os.path.exists(filepath):
                        random_suffix = get_random_string(6)
                        filename = f"{name}_{random_suffix}{ext}"
                        filepath = os.path.join(hasilfix_dir, filename)

                    with open(filepath, 'wb+') as destination:
                        for chunk in image.chunks():
                            destination.write(chunk)

                    img = Image.open(filepath)
                    width, height = img.size
                    slice_height = height // jumlah_slice

                    # Lakukan slicing
                    for i in range(jumlah_slice):
                        top = i * slice_height
                        bottom = (i + 1) * slice_height if i != jumlah_slice - 1 else height
                        box = (0, top, width, bottom)
                        slice_img = img.crop(box)

                        base_name = f"slice_{i+1}.png"
                        save_path = os.path.join(output_dir_slice, base_name)

                        while os.path.exists(save_path):
                            random_suffix = get_random_string(6)
                            base_name = f"slice_{i+1}_{random_suffix}.png"
                            save_path = os.path.join(output_dir_slice, base_name)

                        slice_img.save(save_path)

                        relative_path = os.path.join(settings.MEDIA_URL, 'hasilslice', base_name).replace('\\', '/')
                        hasil_slice_paths.append(relative_path)

                    image_url = os.path.join(settings.MEDIA_URL, 'hasilfix', filename).replace('\\', '/')
                else:
                    return JsonResponse({'status': 'error', 'message': 'File gambar motif gabungan tidak ditemukan.'}, status=400)

            except Exception as e:
                print("ERROR saat proses gambar gabungan:", str(e))
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

            img_before_full = request.POST.get('imgBefore', '')
            img_before_rel = img_before_full.replace(request.build_absolute_uri('/'), '/') if img_before_full.startswith('http') else img_before_full
            # Simpan ke database
            post = MotifForm1()
            post.imgBefore = img_before_rel
            post.imgAfter = image_url
            post.urutanLidi = urutlidi
            post.jenisGenerate = request.POST.get('jenisGenerate')
            post.jmlBaris = request.POST.get('jmlBaris', '0')
            post.user = request.POST.get('user')
            post.slice = json.dumps(hasil_slice_paths)
            raw_lidi = request.session.get('raw_lidi', [])
            post.urutanLidiAsal = ','.join(map(str, raw_lidi)) if raw_lidi else ''
            post.jenisKain = request.POST.get('jenisKain')
            post.jenisProduk = request.POST.get('jenisProduk')

            post.save()
            print("DEBUG: Sukses simpan post gabungan dan slice.")
            return JsonResponse({
                'status': 'success',
                'motif_id': post.id  # Kembalikan ID motif
            })
        else:
            print("DEBUG: Ada field POST yang kosong.")
            return JsonResponse({
                'status': 'error',
                'message': 'Ada field yang kosong.'
            }, status=400)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Metode tidak diizinkan.'
        }, status=405)


def save_image_to_session(request, image):
 
    if 'file' in request.FILES:
        uploaded_image = request.FILES['file']
        print("FILES:", request.FILES['file'])
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)

      
        filename = 'Checking.png'
        full_path = os.path.join(upload_dir, filename)

      
        with open(full_path, 'wb+') as destination:
            for chunk in uploaded_image.chunks():
                destination.write(chunk)

        
        image_url = os.path.join(settings.MEDIA_URL, 'uploads', filename)
        request.session['image_url'] = image_url
        return image_url
    else:
        return None# #@login_required(login_url='login')
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

#@login_required(login_url='login')
def Search(request):
    filter = request.POST.get('filter')
    f = request.POST.get('SearchMotif')
    # user = request.user
    # status = user.is_staff
    navlink = ['nav-link nav-link-1 ','nav-link nav-link-2','nav-link nav-link-3 active','nav-link nav-link-4']
    status = 1
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

    if (motifForm == ""):
         motifForm = None
    
    context = {"motifForm" : motifForm, "typeFilter1": filter[0], "typeFilter2": filter[1], "typeFilter3": filter[2], "valueFilter": f, "status":status,'navlink1':navlink[0],'navlink2':navlink[1],'navlink3':navlink[2],'navlink4':navlink[3]}
    if(f == ''):
         return redirect('list1')
    return render(request,"search.html", context)


#@login_required(login_url='login')
def show(request):
    # user = request.user
    # status = user.is_staff
    navlink = ['nav-link nav-link-1 ', 'nav-link nav-link-2', 'nav-link nav-link-3 active', 'nav-link nav-link-4']
    status = 1
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

#@login_required(login_url='login')
def tagName(request, user):
    username = request.user
    status = username.is_staff
    navlink = ['nav-link nav-link-1 ','nav-link nav-link-2','nav-link nav-link-3 active','nav-link nav-link-4']
    if status == 0:
          status=None
    
    motifForm = MotifForm1.objects.all().filter(user__iexact= user).values().order_by('time').reverse()
        

    context = {"motifForm":motifForm,"status":status,'navlink1':navlink[0],'navlink2':navlink[1],'navlink3':navlink[2],'navlink4':navlink[3]}

    return render(request, "searchTag.html", context)

#@login_required(login_url='login')
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

#@login_required(login_url='login')
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

#@login_required(login_url='login')

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
    
#@login_required(login_url='login')
def motif(request, id):
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Accessing motif detail for ID: {id}")

    try:
        
        motif = MotifForm1.objects.get(id=id)
        user = request.user
        status = user.is_superuser or None
        status1 = user.is_staff or None
        navlink = ['nav-link nav-link-1', 'nav-link nav-link-2', 'nav-link nav-link-3 active', 'nav-link nav-link-4']

        # Ambil data dari sesi
        list_lidi_path = request.session.get('list_lidi_path', [])
        session_name = request.session.get('session_name', '')
        postImageurl = request.session.get('url_image_slice', '')

        logger.debug(f"Session data - list_lidi_path: {list_lidi_path}, session_name: {session_name}, postImageurl: {postImageurl}")

        # Periksa apakah ini motif gabungan
        is_combined = motif.jenisGenerate == "combine"
        logger.debug(f"Motif ID {id} is_combined: {is_combined}")

        # Dapatkan path file gambar
        img_path = os.path.join(settings.MEDIA_ROOT, motif.imgAfter.lstrip('/'))
        if not os.path.exists(img_path):
            img_path = os.path.join(settings.BASE_DIR, motif.imgAfter.lstrip('/'))
            if not os.path.exists(img_path):
                logger.error(f"Image not found at: {img_path}")
                raise FileNotFoundError(f"Image not found: {motif.imgAfter}")

        logger.debug(f"Image path: {img_path}, imgBefore: {motif.imgBefore}")

        # Siapkan direktori untuk grid dan slice
        grid_dir = os.path.join(settings.MEDIA_ROOT, 'grids')
        slice_dir = os.path.join(settings.MEDIA_ROOT, f'slices/motif_{motif.id}')
        os.makedirs(grid_dir, exist_ok=True)
        os.makedirs(slice_dir, exist_ok=True)

        # Resize gambar jika terlalu besar
        if os.path.exists(img_path):
            with Image.open(img_path) as img:
                width, height = img.size
                if width > 600 or height > 800:
                    logger.info(f"Resizing image {img_path} from {width}x{height}")
                    backup_path = img_path.replace('.png', '_original.png')
                    shutil.copy2(img_path, backup_path)
                    max_width, max_height = 600, 800
                    ratio = min(max_width / width, max_height / height)
                    new_width, new_height = int(width * ratio), int(height * ratio)
                    img_resized = img.resize((new_width, new_height), Image.LANCZOS)
                    img_resized.save(img_path)
                    logger.info(f"Resized to {new_width}x{new_height}")

        # Buat grid dan red line
        grid_filename = f"grid_motif_{motif.id}.png"
        red_filename = f"red_motif_{motif.id}.png"
        grid_path = os.path.join(grid_dir, grid_filename)
        red_path = os.path.join(grid_dir, red_filename)

        if not os.path.exists(grid_path) and os.path.exists(img_path):
            with Image.open(img_path) as img:
                grid_img = img.copy().convert('RGB')
                draw = ImageDraw.Draw(grid_img)
                width, height = grid_img.size
                grid_size = 10
                for x in range(0, width, grid_size):
                    draw.line((x, 0, x, height), fill=(100, 100, 100), width=1)
                for y in range(0, height, grid_size):
                    draw.line((0, y, width, y), fill=(100, 100, 100), width=1)
                grid_img.save(grid_path)
                logger.info(f"Created grid image: {grid_path}")

        if not os.path.exists(red_path) and os.path.exists(grid_path):
            with Image.open(grid_path) as img:
                red_img = img.copy()
                draw = ImageDraw.Draw(red_img)
                width, height = red_img.size
                y_mid = height // 2
                draw.line((0, y_mid, width, y_mid), fill=(255, 0, 0), width=3)
                red_img.save(red_path)
                logger.info(f"Created red line image: {red_path}")

        # Proses urutan lidi
        try:
            if motif.urutanLidi and motif.urutanLidi.strip():
                lidi_sequence = re.findall(r'\d+', motif.urutanLidi)
                Urutan_Lidi = [int(x) for x in lidi_sequence]
                if not Urutan_Lidi:
                    raise ValueError("Parsed urutanLidi is empty")
            else:
                row_count = int(motif.jmlBaris) if motif.jmlBaris.isdigit() else 10
                Urutan_Lidi = list(range(1, row_count + 1))
        except Exception as e:
            logger.warning(f"Error processing urutanLidi: {e}")
            row_count = int(motif.jmlBaris) if motif.jmlBaris.isdigit() else 10
            Urutan_Lidi = list(range(1, row_count + 1))
        logger.debug(f"Urutan Lidi: {Urutan_Lidi}")

        # Buat slice
        Slice = []
        if os.path.exists(img_path):
            with Image.open(img_path) as img:
                width, height = img.size
                row_count = len(Urutan_Lidi)
                slice_height = height // row_count
                for i in range(row_count):
                    slice_filename = f"slice_{i+1}.png"
                    slice_path = os.path.join(slice_dir, slice_filename)
                    if not os.path.exists(slice_path):
                        y_top = i * slice_height
                        y_bottom = min((i + 1) * slice_height, height)
                        slice_img = img.crop((0, y_top, width, y_bottom))
                        slice_img.save(slice_path)
                        logger.info(f"Created slice: {slice_path}")
                    Slice.append(f"/media/slices/motif_{motif.id}/{slice_filename}")

        # Buat ZIP
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
                for i in range(len(Slice)):
                    slice_path = os.path.join(slice_dir, f"slice_{i+1}.png")
                    if os.path.exists(slice_path):
                        zf.write(slice_path, arcname=f"slice_{i+1}.png")
            logger.info(f"Created ZIP file: {zip_path}")

        # Siapkan data untuk template
        mySlice = list(zip_longest(Slice, Urutan_Lidi))
        UrutanLidi_even = [Urutan_Lidi[i] for i in range(0, len(Urutan_Lidi), 2)]
        UrutanLidi_odd = [Urutan_Lidi[i] for i in range(1, len(Urutan_Lidi), 2)]
        Slice2 = Slice.copy()
        Slice_even = [Slice[i] for i in range(0, len(Slice), 2)]
        Slice_odd = [Slice[i] for i in range(1, len(Slice), 2)]
        Slice2_even = [Slice2[i] for i in range(0, len(Slice2), 2)]
        Slice2_odd = [Slice2[i] for i in range(1, len(Slice2), 2)]
        UrutanMotif = Urutan_Lidi.copy()
        UrutanMotif_even = UrutanLidi_even.copy()
        UrutanMotif_odd = UrutanLidi_odd.copy()
        myList = list(zip_longest(Slice_even, UrutanLidi_even, Slice_odd, UrutanLidi_odd))
        myList2 = list(zip_longest(Slice2_even, UrutanMotif_even, Slice2_odd, UrutanMotif_odd))

        # URL untuk template
        grid_url = f"/media/grids/{grid_filename}"
        red_url = f"/media/grids/{red_filename}"
        zip_url = f"/media/zips/{zip_filename}"
        list_lidi_path = motif.urutanLidiAsal.split(',') if motif.urutanLidiAsal else []
        context = {
            'motif': motif,
            'Lidi': grid_url,
            'RedLine': motif.imgAfter,
            'zip': zip_url,
            'UrutanLidi': motif.urutanLidi,
            'urutanAsliLidi': motif.urutanLidi,
            'GridHelp': grid_url,
            'SliceLidi': myList,
            'SliceMotif': myList2,
            'status': status,
            'status1': status1,
            'navlink1': navlink[0],
            'navlink2': navlink[1],
            'navlink3': navlink[2],
            'navlink4': navlink[3],
            'list_lidi_path': list_lidi_path,
            'jenis_kain': motif.jenisKain,  # Tambahkan jenis kain
            'jenis_produk': motif.jenisProduk,
            'jenis_kain': motif.jenisKain, 
            'jenis_produk': motif.jenisProduk, 
            'session_name': session_name,
            'slice': mySlice,
            'postImageurl': postImageurl,
            'motif_asal': motif.imgBefore,
        }
        return render(request, 'lihatMotif.html', context)
    except Motif.DoesNotExist:
        return render(request, 'lihatMotif.html', {'error_messages': ['Motif tidak ditemukan']})

    except MotifForm1.DoesNotExist:
        logger.error(f"Motif with ID {id} not found")
        messages.error(request, "Motif tidak ditemukan.")
        return redirect('list1')
    except Exception as e:
        logger.error(f"Error in motif view: {str(e)}", exc_info=True)
        messages.error(request, f"Terjadi kesalahan: {str(e)}")
        return redirect('list1')    

#@login_required(login_url='login')
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
#@login_required(login_url='login')
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

#@login_required(login_url='login')    
def showTest(request):
    
    motifForm = Post.objects.all().values()
    context = {"motifForm":motifForm}

    return render(request, "ListMotif.html", context)

#@login_required(login_url='login')
def help(request):
    
    navlink = ['nav-link nav-link-1 ','nav-link nav-link-2','nav-link nav-link-3','nav-link nav-link-4 active']
    return render(request, "help.html", {'navlink1':navlink[0],'navlink2':navlink[1],'navlink3':navlink[2],'navlink4':navlink[3]})

#@login_required(login_url='login')
def help_generate(request):

    navlink = ['nav-link nav-link-1 ','nav-link nav-link-2','nav-link nav-link-3','nav-link nav-link-4 active']
    return render(request, "help-generator.html", {'navlink1':navlink[0],'navlink2':navlink[1],'navlink3':navlink[2],'navlink4':navlink[3]})

#@login_required(login_url='login')
def help_lidi(request):

    navlink = ['nav-link nav-link-1 ','nav-link nav-link-2','nav-link nav-link-3','nav-link nav-link-4 active']
    return render(request, "help-lidi.html", {'navlink1':navlink[0],'navlink2':navlink[1],'navlink3':navlink[2],'navlink4':navlink[3]})

#@login_required(login_url='login')
def help_search(request):

    navlink = ['nav-link nav-link-1 ','nav-link nav-link-2','nav-link nav-link-3','nav-link nav-link-4 active']
    return render(request, "help-search.html", {'navlink1':navlink[0],'navlink2':navlink[1],'navlink3':navlink[2],'navlink4':navlink[3]})

#@login_required(login_url='login')
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

#@login_required(login_url='login')
def gabungkan_motif(request):
    # Ambil URL gambar dari session
    urutanasal = request.session.get('urutanasal')
    urutan=request.session.get('urutan')
    urutan2=request.session.get('urutan2')
    urutan3=request.session.get('urutan3')
    urutan4=request.session.get('urutan4')
    raw_url = request.session.get('raw_url')
    raw_lidi = request.session.get('raw_lidi')
    edit_url = request.session.get('edit_url')
    edit_url2 = request.session.get('edit_url2')
    edit_url3 = request.session.get('edit_url3')
    edit_url4 = request.session.get('edit_url4')
    list_lidi_path = request.session.get('list_lidi_path')
    jumlahasal = request.session.get('jumlahasal')
    sessionName = request.session.get('session_name')
    print(f"raw_lidi: {raw_lidi}")
    print(f"raw_url: {raw_url}")
    print(f"urutan nih ye:{urutanasal}")
    # Pastikan semua gambar tersedia sebelum merender halaman
    if not raw_url or not edit_url:
        messages.error(request, "Beberapa gambar motif tidak tersedia.")
        return redirect('generator')

    return render(request, 'gabung-motif.html', {
        'urutanasal':(urutanasal),
        'urutan':urutan,
        'urutan1':urutan2,
        'urutan2':urutan3,
        'urutan3':urutan4,
        'raw_url': raw_url,
        'raw_lidi': raw_lidi,
        'edit_url': edit_url,
        'list_lidi_path': list_lidi_path,
        'sessionName': sessionName,
        'edit_url2': edit_url2 if edit_url2 else edit_url,
        'edit_url3': edit_url3 if edit_url3 else edit_url,
        'edit_url4': edit_url4 if edit_url4 else edit_url,
        'jumlahasal': jumlahasal
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
            raw_lidi = request.session.get('raw_lidi', [])
            motif.urutanLidiAsal = ','.join(map(str, raw_lidi)) if raw_lidi else ''
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
#@login_required(login_url='login')
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
            import uuid
            
            print(f"Error upload gambar: {str(e)}")
            print(traceback.format_exc())
            return JsonResponse({'error': f'Gagal mengupload gambar: {str(e)}'}, status=500)
    
    return JsonResponse({'error': 'Metode tidak diizinkan'}, status=405)

def ubah_warna(request):
    combined_motif_urls = request.session.get('combined_motifs', [])  # Mengambil motif yang sudah dipilih dari session

    if not combined_motif_urls:
        messages.error(request, "Motif tidak ditemukan!")

    print(f"Combined Motif URLs: {combined_motif_urls}")

    return render(request, 'ubah-warna.html', {'combined_motif_urls': combined_motif_urls})

#@login_required(login_url='login')
@csrf_exempt
def ubah_warna_combined(request, id):
    motif = MotifForm1.objects.get(id=id)

    # Ambil gambar motif yang akan diubah warnanya
    img_url = os.path.join(settings.MEDIA_ROOT, motif.imgAfter.lstrip('/')).replace("media\\", "/")  # Resolve to absolute path and normalize slashes

    print(f"img_url: {img_url}")
    print(f"motif_asal: {motif.imgBefore}")

    def separate_background_and_motif(img_url, motif_id): #memisahkan background dan motif dari sebuah gambar.
        try:
            # Path untuk menyimpan hasil pemisahan
            base_dir = os.path.join(settings.MEDIA_ROOT, 'admin', 'colored_motifs', f'motif_{motif_id}')
            os.makedirs(base_dir, exist_ok=True)

            print(f"Base dir: {base_dir}")

            # Path untuk gambar background dan motif
            background_path = os.path.join(base_dir, f'background_{motif_id}.png')
            motif_path = os.path.join(base_dir, f'motif_{motif_id}.png')

            # Cek apakah file sudah ada, jika ada hapus
            if os.path.exists(background_path):
                os.remove(background_path)
                print(f"Deleted existing background image: {background_path}")
            if os.path.exists(motif_path):
                os.remove(motif_path)
                print(f"Deleted existing motif image: {motif_path}")

            absolute_img_path = os.path.join(settings.BASE_DIR, img_url.lstrip('/'))
            
            # Buka gambar
            if not os.path.exists(absolute_img_path):
                raise FileNotFoundError(f"File not found: {absolute_img_path}")
            
            with Image.open(absolute_img_path) as img:
                img = img.convert('RGBA')  
                width, height = img.size

                background_img = Image.new('RGBA', (width, height), (255, 255, 255, 0)) #>200 berarti terang, jd dianggap bg
                motif_img = Image.new('RGBA', (width, height), (0, 0, 0, 0)) #0 dianggap gelap

                for x in range(width): #dilakukan dua kali looping dikarnakan gambarnya 2 dimensi
                    for y in range(height):
                        r, g, b, a = img.getpixel((x, y)) #menciptakan pixel baru
                        if r > 200 and g > 200 and b > 200:  
                            background_img.putpixel((x, y), (r, g, b, a))
                        else:  
                            motif_img.putpixel((x, y), (r, g, b, a))

                # Simpan hasil
                background_img.save(background_path, format="PNG")
                motif_img.save(motif_path, format="PNG")

            return background_path, motif_path

        except Exception as e:
            print(f"Error separating background and motif: {e}")
            return None, None

    # Pisahkan background dan motif
    background_path, motif_path = separate_background_and_motif(img_url, motif.id)
    if not background_path or not motif_path:
        messages.error(request, "Gagal memisahkan background dan motif")
        return redirect('ubah_warna', id=id)

    if request.method == 'POST':
        try:
            # Ambil data gambar dari request (base64)
            img_data = request.POST.get('image')
            if not img_data:
                return JsonResponse({'status': 'error', 'message': 'Image data not found'}, status=400)

            # Parse data URL
            format, imgstr = img_data.split(';base64,')
            ext = format.split('/')[-1]

            # Buat nama file unik untuk gambar yang diubah
            filename = f"colored_motif_{uuid.uuid4()}.{ext}"
            filepath = os.path.join(settings.MEDIA_ROOT, 'admin', 'colored_motifs', filename)

            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            # Simpan gambar ke file
            with open(filepath, "wb") as f:
                f.write(base64.b64decode(imgstr))

            motif.imgAfter = f"/media/admin/colored_motifs/{filename}"
            motif.save()

            return JsonResponse({'status': 'success', 'message': 'Motif updated successfully', 'path': motif.imgAfter})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        
    print({
        'motif': motif,
        'combined_motif_urls': img_url.replace("\\", "/"),
        'background_path': background_path.replace("\\", "/"),
        'motif_path': motif_path.replace("\\", "/"),
        'motif_asal': motif.imgBefore.replace("\\", "/"),
    })

    return render(request, 'ubah-warna.html', {     #render ke halaman ubah warna (344-397)
        'motif': motif,         
        'combined_motif_urls': img_url.replace("\\", "/"),
        'background_path': background_path.replace("\\", "/"),
        'motif_path': motif_path.replace("\\", "/"),
        'motif_id': id,
        'motif_asal': motif.imgBefore.replace("\\", "/"),
    })

#@login_required(login_url='login')
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

    return render(request, 'ubah-warna.html', {'motif': motif, 'img_url': img_url})

#@login_required(login_url='login')
def ubah_warna(request, id):
    motif = MotifForm1.objects.get(id=id)
    
    # Jika menggunakan gambar yang digabungkan, bisa menggunakan combined_motif_urls atau motif.imgAfter
    combined_motif_urls = [motif.imgAfter.replace("\\", "/")]  # Misalnya hanya satu gambar motif yang digabungkan
    
    if request.method == 'POST':
        warna_motif = request.POST.get('warnaMotif')
        # Lakukan pemrosesan untuk mewarnai motif sesuai dengan warna yang dipilih
        # Setelah pewarnaan, simpan gambar baru dan tampilkan hasilnya
        
        motif.imgAfter = 'path_to_new_colored_image'  # Ganti dengan path gambar yang sudah diwarnai
        motif.save()
        
        return render(request, 'ubah_warna_success.html', {'motif': motif, 'warna': warna_motif})
    
    print(f"Combined Motif URLs: {combined_motif_urls}")

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

# Normalize the file path to remove invalid characters
    img_url = os.path.normpath(motif.imgAfter.replace("\\", "/"))
    img_url = img_url.strip()  # Remove any leading or trailing whitespace

    if not os.path.exists(os.path.join(settings.BASE_DIR, img_url.lstrip('/'))):
        raise FileNotFoundError(f"File not found: {img_url}")

def ubah_warna(request, id):
    motif = MotifForm1.objects.get(id=id)
    
    # Ambil gambar motif yang akan diubah warnanya
    img_url = motif.imgAfter  # Misalnya, gambar hasil gabungan
    
    # Path untuk menyimpan grid yang mengikuti bentuk motif
    grid_output_path = os.path.join(settings.MEDIA_ROOT, 'grids', f'grid_motif_{id}.png')
    os.makedirs(os.path.dirname(grid_output_path), exist_ok=True)

    # Buat grid mengikuti bentuk motif jika belum ada
    if not os.path.exists(grid_output_path):
        create_grid_from_motif(os.path.join(settings.MEDIA_ROOT, img_url.lstrip('/')), grid_output_path)

    if request.method == 'POST':
        warna = request.POST.get('warna')
        # Proses perubahan warna (misalnya menggunakan Python Image Library atau metode lain)
        # Di sini kamu bisa menambahkan logika untuk mengubah warna motif sesuai pilihan pengguna
        
        # Simpan gambar yang sudah diubah warna, misalnya:
        # motif.imgAfter = img_url_with_new_color
        motif.save()
        
        return render(request, 'ubah_warna_success.html', {'motif': motif, 'warna': warna})

    return render(request, 'ubah-warna.html', {'motif': motif, 'img_url': img_url, 'grid_url': f'/media/grids/grid_motif_{id}.png'})

@csrf_exempt
def newMotifColoredGabunganPreview(request, motif_id):
    motif_instance = MotifForm1.objects.get(id=motif_id)
    background_file = motif_instance.coloredImage.split('@@')[0]
    motif_file = motif_instance.coloredImage.split('@@')[1]
    combined_image_url = motif_instance.coloredImagecombined
    urutanLidi = motif_instance.urutanLidi.strip().split(',')
    
    jumlahbaris = len(motif_instance.urutanLidi.strip().split(','))

    print('newMotifColoredGabunganPreview')

    slice_dir = os.path.join(settings.MEDIA_ROOT, 'admin', 'colored_motifs', f'motif_{motif_id}', 'slice_colored')
    os.makedirs(slice_dir, exist_ok=True)

    ditenun_logo_1 = os.path.join(settings.MEDIA_ROOT, 'admin', 'ditenun_static', 'image-removebg-preview.png')
    ditenun_logo_2 = os.path.join(settings.MEDIA_ROOT, 'admin', 'ditenun_static', 'logo_ditenun_2.jpeg')

    combined_image_path = os.path.join(settings.BASE_DIR, combined_image_url.lstrip('/'))
    slice_urls = []

    
    user = request.session.get('user')

    try:
        if os.path.exists(slice_dir):
            for file in os.listdir(slice_dir):
                file_path = os.path.join(slice_dir, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)

        with Image.open(combined_image_path) as img:
            width, height = img.size
            slice_height = height / jumlahbaris

            for i in range(jumlahbaris):
                y_top = round(i * slice_height)
                y_bottom = round((i + 1) * slice_height)

                print(f"y_top: {y_top}")
                print(f"y_bottom: {y_bottom}")

                slice_img = img.crop((0, y_top, width, y_bottom))

                slice_filename = f"colored_slice_image_{i}.png"
                slice_path = os.path.join(slice_dir, slice_filename)
                slice_img.save(slice_path)

                slice_url = os.path.join(settings.MEDIA_URL, 'admin', 'colored_motifs', f'motif_{motif_id}', 'slice_colored', slice_filename).replace('\\', '/')
                slice_urls.append(slice_url)

        slice_urls_combined = '@@'.join(slice_urls)
        motif_instance.sliceColoredimage = slice_urls_combined
        motif_instance.save()

        mySlice = list(zip_longest(slice_urls, urutanLidi))

        date_now = now()

    except Exception as e:
        print(f"Error slicing combined image: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return render(request, 'motif_gabungan_colored_preview.html', {
        'combined_image_url': combined_image_url, 
        'slice_urls': slice_urls, 
        'jumlahbaris': jumlahbaris, 
        'urutanLidi': urutanLidi, 
        'slice': mySlice, 
        'motif': motif_instance, 
        'user': user, 
        'date_now': now(),
        'ditenun_logo_1': ditenun_logo_1.replace('\\', '/'),
        'ditenun_logo_2': ditenun_logo_2.replace('\\', '/'),
    })

@csrf_exempt
def PostColoredMotifImage(request):
    if request.method == 'POST':
        background_file = request.FILES.get('background_warna')
        motif_file = request.FILES.get('motif_warna')

        if not background_file or not motif_file:
            return JsonResponse({'status': 'error', 'message': 'Both background and motif images are required.'})

        try:
            motif_id = str(request.POST.get('motif_id'))  # Ensure motif_id is treated as a string
            print(f"motif_id: {motif_id}")
            base_dir = os.path.join(settings.MEDIA_ROOT, 'admin', 'colored_motifs', f'motif_{motif_id}')
            os.makedirs(base_dir, exist_ok=True)

            background_path = os.path.join(base_dir, 'colored_background.png')
            motif_path = os.path.join(base_dir, 'colored_motif.png')
            combined_path = os.path.join(base_dir, 'colored_combined.png')

            with open(background_path, 'wb') as f:
                for chunk in background_file.chunks():
                    f.write(chunk)

            with open(motif_path, 'wb') as f:
                for chunk in motif_file.chunks():
                    f.write(chunk)

            background_url = os.path.join(settings.MEDIA_URL, 'admin', 'colored_motifs', f'motif_{motif_id}', 'colored_background.png').replace('\\', '/')
            motif_url = os.path.join(settings.MEDIA_URL, 'admin', 'colored_motifs', f'motif_{motif_id}', 'colored_motif.png').replace('\\', '/')
            combined_url = os.path.join(settings.MEDIA_URL, 'admin', 'colored_motifs', f'motif_{motif_id}', 'colored_combined.png').replace('\\', '/')

            print(f"Background Image URL: {background_url}")
            print(f"Motif Image URL: {motif_url}")
            print(f"Combined Image URL: {combined_url}")

            background = Image.open(background_path)
            motif = Image.open(motif_path)

            original_width, original_height = background.size
            new_width = int(original_width * 1)
            new_height = int(original_height * 1)
            background = background.resize((new_width, new_height), Image.ANTIALIAS)

            combined = Image.new('RGBA', (new_width, new_height), (255, 255, 255, 0))
            motif_width, motif_height = motif.size
            x_offset = (new_width - motif_width) // 2
            y_offset = (new_height - motif_height) // 2
            combined.paste(background, (0, 0))
            combined.paste(motif, (x_offset, y_offset), mask=motif)

            combined.save(combined_path)

            motif_instance = MotifForm1.objects.get(id=motif_id)
            motif_instance.coloredImage = f"{background_url}@@{motif_url}"
            motif_instance.coloredImagecombined = combined_url
            motif_instance.save()

            return redirect(f'/motif_colored/preview/{motif_id}')

        except Exception as e:
            print(f"Error processing motif_id: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

logger = logging.getLogger(__name__)

def motif_gabungan_colored_preview(request, id):
    try:
        motif = MotifForm1.objects.get(id=id)
        user = request.session.get('user', 'admin')  # Ambil user dari session atau default ke 'admin'

        # Ambil data dari model
        combined_image_url = motif.coloredImagecombined if motif.coloredImagecombined else motif.imgAfter
        slice_urls = motif.sliceColoredimage.split('@@') if motif.sliceColoredimage else []
        urutanLidi = motif.urutanLidi.strip().split(',') if motif.urutanLidi else []
        jumlahbaris = len(urutanLidi) if urutanLidi else 0

        # Siapkan data untuk slicing jika belum ada
        if not slice_urls:
            slice_dir = os.path.join(settings.MEDIA_ROOT, 'admin', 'colored_motifs', f'motif_{id}', 'slice_colored')
            os.makedirs(slice_dir, exist_ok=True)
            combined_image_path = os.path.join(settings.BASE_DIR, combined_image_url.lstrip('/'))
            if os.path.exists(combined_image_path):
                with Image.open(combined_image_path) as img:
                    width, height = img.size
                    slice_height = height / jumlahbaris if jumlahbaris else height
                    slice_urls = []
                    for i in range(jumlahbaris):
                        y_top = round(i * slice_height)
                        y_bottom = round((i + 1) * slice_height)
                        slice_img = img.crop((0, y_top, width, y_bottom))
                        slice_filename = f"colored_slice_image_{i}.png"
                        slice_path = os.path.join(slice_dir, slice_filename)
                        slice_img.save(slice_path)
                        slice_url = os.path.join(settings.MEDIA_URL, 'admin', 'colored_motifs', f'motif_{id}', 'slice_colored', slice_filename).replace('\\', '/')
                        slice_urls.append(slice_url)
                motif.sliceColoredimage = '@@'.join(slice_urls)
                motif.save()

        # Gabungkan slice dan urutanLidi untuk template
        mySlice = list(zip_longest(slice_urls, urutanLidi))

        # Path logo (sesuaikan dengan struktur direktori Anda)
        ditenun_logo_1 = os.path.join(settings.MEDIA_ROOT, 'admin', 'ditenun_static', 'image-removebg-preview.png').replace('\\', '/')
        ditenun_logo_2 = os.path.join(settings.MEDIA_ROOT, 'admin', 'ditenun_static', 'logo_ditenun_2.jpeg').replace('\\', '/')

        context = {
            'combined_image_url': combined_image_url,
            'slice_urls': slice_urls,
            'jumlahbaris': jumlahbaris,
            'urutanLidi': urutanLidi,
            'slice': mySlice,
            'motif': motif,
            'user': user,
            'date_now': timezone.now().strftime('%d-%m-%Y'),
            'ditenun_logo_1': ditenun_logo_1,
            'ditenun_logo_2': ditenun_logo_2,
        }
        
        # Format tetap sama, hanya memastikan WIB ditambahkan
        date_now = timezone.now().strftime('%d-%m-%Y %H:%M') + " WIB"
        logger.debug(f"date_now: {date_now}")
        
        logger.debug(f"Preview - Kain: {motif.jenisKain}, Produk: {motif.jenisProduk}")
        return render(request, 'motif_gabungan_colored_preview.html', context)
    except MotifForm1.DoesNotExist:
        logger.error(f"Motif with ID {id} not found")
        return render(request, 'error.html', {'error_message': 'Motif tidak ditemukan'})