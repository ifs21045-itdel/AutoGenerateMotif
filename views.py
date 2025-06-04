from PIL import Image
import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def ubah_warna_combined(request, id):
    # Paths for saving images
    base_dir = os.path.join(settings.MEDIA_ROOT, 'admin', 'colored_motifs', f'motif_{id}')
    os.makedirs(base_dir, exist_ok=True)

    background_path = os.path.join(base_dir, 'colored_background.png').replace('\\', '/')
    motif_path = os.path.join(base_dir, 'colored_motif.png').replace('\\', '/')
    combined_path = os.path.join(base_dir, 'colored_motif_combined.png').replace('\\', '/')

    # Load canvas images (replace with actual logic to retrieve canvas data)
    background = Image.open("path/to/background/image.png")  # Replace with actual background path
    motif = Image.open("path/to/motif/image.png")  # Replace with actual motif path

    # Resize background to original size + 10%
    original_width, original_height = background.size
    new_width = int(original_width * 1.1)
    new_height = int(original_height * 1.1)
    background = background.resize((new_width, new_height), Image.ANTIALIAS)

    # Save resized background and motif
    background.save(background_path)
    motif.save(motif_path)

    # Combine images
    combined = Image.new('RGBA', (new_width, new_height), (255, 255, 255, 0))
    motif_width, motif_height = motif.size
    x_offset = (new_width - motif_width) // 2
    y_offset = (new_height - motif_height) // 2
    combined.paste(background, (0, 0))
    combined.paste(motif, (x_offset, y_offset), mask=motif)

    # Save combined image
    combined.save(combined_path)

    return render(request, 'motif_gabungan_colored_preview.html', {
        'background_path': background_path.replace(settings.MEDIA_ROOT, settings.MEDIA_URL),
        'motif_path': motif_path.replace(settings.MEDIA_ROOT, settings.MEDIA_URL),
        'combined_path': combined_path.replace(settings.MEDIA_ROOT, settings.MEDIA_URL),
    })

@csrf_exempt
def PostColoredMotifImage(request):
    if request.method == 'POST':
        # Retrieve files from the request
        background_file = request.FILES.get('background_warna')
        motif_file = request.FILES.get('motif_warna')

        if not background_file or not motif_file:
            return JsonResponse({'status': 'error', 'message': 'Both background and motif images are required.'})

        # Define paths for saving images
        motif_id = request.POST.get('motif_id')

        print(f"motif_id: {motif_id}")

        base_dir = os.path.join(settings.MEDIA_ROOT, 'admin', 'colored_motifs', f'motif_{motif_id}')
        os.makedirs(base_dir, exist_ok=True)

        background_path = os.path.join(base_dir, 'colored_background.png')
        motif_path = os.path.join(base_dir, 'colored_motif.png')
        combined_path = os.path.join(base_dir, 'colored_combined.png')

        # Save the uploaded images
        with open(background_path, 'wb') as f:
            for chunk in background_file.chunks():
                f.write(chunk)

        with open(motif_path, 'wb') as f:
            for chunk in motif_file.chunks():
                f.write(chunk)

        # Generate URL paths for the images
        background_url = os.path.join(settings.MEDIA_URL, 'admin', 'colored_motifs', f'motif_{motif_id}', 'colored_background.png').replace('\\', '/')
        motif_url = os.path.join(settings.MEDIA_URL, 'admin', 'colored_motifs', f'motif_{motif_id}', 'colored_motif.png').replace('\\', '/')
        combined_url = os.path.join(settings.MEDIA_URL, 'admin', 'colored_motifs', f'motif_{motif_id}', 'colored_combined.png').replace('\\', '/')

        # Print the URLs for debugging
        print(f"Background Image URL: {background_url}")
        print(f"Motif Image URL: {motif_url}")
        print(f"Combined Image URL: {combined_url}")

        # Open the images
        background = Image.open(background_path)
        motif = Image.open(motif_path)

        # Resize background to 110% of its original size
        original_width, original_height = background.size
        new_width = int(original_width * 1)
        new_height = int(original_height * 1)
        background = background.resize((new_width, new_height), Image.ANTIALIAS)

        # Combine the images
        combined = Image.new('RGBA', (new_width, new_height), (255, 255, 255, 0))
        motif_width, motif_height = motif.size
        x_offset = (new_width - motif_width) // 2
        y_offset = (new_height - motif_height) // 2
        combined.paste(background, (0, 0))
        combined.paste(motif, (x_offset, y_offset), mask=motif)

        # Save the combined image
        combined.save(combined_path)

        # Update the database with the image URLs
        from .models import MotifForm1  # Ensure the correct model is imported
        try:
            motif_instance = MotifForm1.objects.get(id=motif_id)
            motif_instance.coloredImage = f"{background_url}@@{motif_url}"
            motif_instance.coloredImagecombined = combined_url
            motif_instance.save()
        except MotifForm1.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Motif not found in the database.'}, status=404)

        # Redirect to the preview page
        return redirect(f'/motif_colored/preview/{motif_id}')

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def newMotifColoredGabunganPreview(request, motif_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Metode tidak diizinkan'}, status=405)

    # Retrieve uploaded files from the request
    background_file = request.FILES.get('background_warna')
    motif_file = request.FILES.get('motif_warna')

    if not background_file or not motif_file:
        return JsonResponse({'status': 'error', 'message': 'Background or motif file is missing.'}, status=400)

    # Save the uploaded files to the specified directory
    base_dir = os.path.join(settings.MEDIA_ROOT, 'admin', 'colored_motifs', f'motif_{motif_id}')
    os.makedirs(base_dir, exist_ok=True)

    background_path = os.path.join(base_dir, 'colored_background.png').replace('\\', '/')
    motif_combined_path = os.path.join(base_dir, 'colored_motifs_combined.png').replace('\\', '/')
    combined_image_path = os.path.join(base_dir, 'combined_colored_motif.png').replace('\\', '/')

    # Save the uploaded files
    with open(background_path, 'wb') as f:
        for chunk in background_file.chunks():
            f.write(chunk)

    with open(motif_combined_path, 'wb') as f:
        for chunk in motif_file.chunks():
            f.write(chunk)

    try:
        # Open the saved images
        background = Image.open(background_path).convert("RGBA")
        motif = Image.open(motif_combined_path).convert("RGBA")

        # Resize motif to match background size (if needed)
        motif = motif.resize(background.size, Image.ANTIALIAS)

        # Combine images
        combined = Image.alpha_composite(background, motif)

        # Save the combined image
        combined.save(combined_image_path, format="PNG")

        # Retrieve the combined image URL from the database
        from .models import Motif  # Import the Motif model
        try:
            motif_instance = Motif.objects.get(id=motif_id)
            combined_image_url = motif_instance.coloredImageCombined.url
        except Motif.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Motif not found in the database.'}, status=404)

        # Render the template with the combined image URL
        return render(request, 'motif_gabungan_colored_preview.html', {
            'combined_image_url': combined_image_url
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Error processing images: {str(e)}'}, status=500)