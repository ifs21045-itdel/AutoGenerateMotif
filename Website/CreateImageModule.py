import cv2
import os
import uuid
import pants
import numpy as np
from PIL import Image
from itertools import permutations
from .Function import TabuSearch
from .Function import RandomSearch
from .Function import GreedySearch
from .Function import ACO
from .Function import SkorPertama
from .ProcessImage import ScaleImage
from .ProcessImage import ProcesImage
from .ProcessImage import SeparateImage
from .ProcessImage import ConvertRGB
from .ProcessImage import ConvertArrayImage
from .ProcessImage import ConvertLiditoArray
from .ProcessImage import CreateImage
import random
class CreateImageMotif:
    def __init__(self, fullpath, namaMotif, jmlBaris, Baris, mode, username, sessionName):
        self.fullpath = fullpath
        self.namaMotif = namaMotif
        self.jmlBaris = jmlBaris
        self.Baris = Baris
        self.mode = mode
        self.username = username
        self.sessionName = sessionName

    def imageOriginal(self):
        slice_url_path = []
        image_fullpath = self.fullpath
        folderUser = os.path.join("media", "motif_awal", "slices")  # Ensure the folder is inside 'media'
        os.makedirs(folderUser, exist_ok=True)

        
        img = cv2.imread(image_fullpath, 1)
        if img is None:
            raise ValueError(f"Gagal membaca gambar dari path: {image_fullpath}")

        
        if self.mode == "4":
            img = cv2.resize(img, None, fx=4, fy=4, interpolation=cv2.INTER_LINEAR)

        height, width, _ = img.shape
        num_slices = 8
        slice_height = height // num_slices
        slices = []
        slice_filenames = []
        slice_indices = []
        print(f"[INFO] Ukuran gambar: {width}x{height}, dipotong menjadi {num_slices} potongan vertikal.")

        for i in range(num_slices):
            start_y = i * slice_height
            end_y = height if i == num_slices - 1 else (i + 1) * slice_height

            slice_img = img[start_y:end_y, 0:width]

            if slice_img is None or slice_img.size == 0:
                print(f"[WARNING] Slice {i + 1} kosong.")
                continue
            
            slice_name = f"slice_{i + 1}_{self.sessionName}.jpg"
            slice_path = os.path.join(folderUser, slice_name).replace("\\", "/")  # Ensure consistent path format
            success = cv2.imwrite(slice_path, slice_img)
            if success:
                print(f"[OK] Slice {i + 1} saved at {slice_path}")
                slices.append(slice_img)
                slice_filenames.append(slice_name)
                slice_indices.append(i + 1)
                slice_url_path.append(f"motif_awal/slices/{slice_name}")  # Relative path for URL
            else:
                print(f"[ERROR] Gagal menyimpan slice {i + 1}")

        if not slices:
            raise ValueError("Semua slice gagal disimpan!")

        
        pil_slices = [Image.fromarray(cv2.cvtColor(s, cv2.COLOR_BGR2RGB)) for s in slices]
        total_height = sum(im.height for im in pil_slices)
        combined_img = Image.new('RGB', (width, total_height))

        y_offset = 0
        for im in pil_slices:
            combined_img.paste(im, (0, y_offset))
            y_offset += im.height

        hasil_akhir_path = os.path.join(folderUser, "hasil_akhir.png")
        combined_img.save(hasil_akhir_path)
        print(f"[DONE] Gabungan slice disimpan di {hasil_akhir_path}")

        print(f"slice_url_path: {slice_url_path}")

        return slice_filenames, slice_indices, slice_url_path
    
    def imageEven(self):
        def SkorACO(a, b):
            temp1 = Array_data[a[0]]
            temp2 = Array_data[a[1]]
            temp3 = Array_data[b[0]]
            temp4 = Array_data[b[1]]

            SkorArray1 = SkorPertama(temp1, temp2)
            SkorArray2 = SkorPertama(temp3, temp4)
            SkorArray3 = SkorPertama(temp2, temp3)

            SkorArray = 1/(1 + SkorArray1 + SkorArray2 + SkorArray3)
            return SkorArray
        
        image_fullpath = self.fullpath
        image_name = self.namaMotif
        
        jmlBaris = int(self.jmlBaris)
        jmlBaris = int(jmlBaris/2)
        
        Baris = int(self.Baris)

        ModeGenerate = self.mode
        folderUser = self.username
        makeFolder = f"media/{folderUser}"

        if(not os.path.exists(makeFolder)):
            os.mkdir(makeFolder)
        
        ModeGenerate = int(ModeGenerate)

        unique_file_name = uuid.uuid4().hex
        unique = f"{folderUser}/{unique_file_name}.png"
        image_save_path = image_fullpath.replace(image_name, unique)

        namaDirektori = f"Image/{folderUser}"
        Direktori = str(namaDirektori)

        if(not os.path.exists(Direktori)):
            os.mkdir(Direktori)

        #Separate Image
        img = cv2.imread(str(image_fullpath), 1)
        SeparateImage(img, Direktori)

        height, width, channels = img.shape

        img = []
        Lidi = []

        # Conver to RGBA
        img, Lidi = ConvertRGB(img, Lidi, height, Direktori)

        # Convert Binary
        Array_data = []
        Tabu_List = []

        Array_data = ConvertArrayImage(img, Array_data)

        comb = list(permutations(Lidi, 2))

        SkorArray = []
        for i in range(0, int(len(Lidi))):
            for j in range(0, int(len(Lidi)-1)):
                temp1 = Array_data[i].copy()
                temp2 = Array_data[j].copy()

                SkorArray.append(SkorPertama(temp1, temp2))
        
        #ACO
        world = pants.World(comb, SkorACO)
        solver = pants.Solver()

        comb = np.array_split(comb, height)
        PanjangLidi = int(len(Lidi))-1

        if(ModeGenerate == 1):
            Tabu_List, Best_Solution = TabuSearch(PanjangLidi, Array_data, Baris, jmlBaris, Tabu_List)
            a = Best_Solution[0]
        elif(ModeGenerate == 2):
            a = GreedySearch(PanjangLidi, comb, Baris, jmlBaris)
        elif(ModeGenerate == 3):
            a = RandomSearch(PanjangLidi, jmlBaris)
        elif(ModeGenerate == 4):
            a = ACO(solver, world, jmlBaris)
        
        img = cv2.imread(str(image_fullpath), 1)

        height, width, channels = img.shape
        img = []

        img = ConvertLiditoArray(img, height, Direktori)

        c = a.copy()
        c = c[::-1]
        a.extend(c)
        b = a.copy()
        b = [x+1 for x in b]

        img = CreateImage(a, img)
        Image.fromarray(img).save(f"{namaDirektori}/Hasil1.jpg")
        
        img = Image.open(f"{namaDirektori}/Hasil1.jpg")
        img = ProcesImage(img)
        img = ScaleImage(img)
        img.save(image_save_path)

        return f"/media/{folderUser}/{unique_file_name}.png", b
        
    def imageOdd(self):
        def SkorACO(a, b):
            temp1 = Array_data[a[0]]
            temp2 = Array_data[a[1]]
            temp3 = Array_data[b[0]]
            temp4 = Array_data[b[1]]

            SkorArray1 = SkorPertama(temp1, temp2)
            SkorArray2 = SkorPertama(temp3, temp4)
            SkorArray3 = SkorPertama(temp2, temp3)

            SkorArray = 1/(1 + SkorArray1 + SkorArray2 + SkorArray3)
            return SkorArray
        
        image_fullpath = self.fullpath
        image_name = self.namaMotif
        
        jmlBaris = int(self.jmlBaris)+1
        jmlBaris = int(jmlBaris/2)
        
        Baris = int(self.Baris)

        ModeGenerate = self.mode
        folderUser = self.username
        makeFolder = f"media/{folderUser}"

        if(not os.path.exists(makeFolder)):
            os.mkdir(makeFolder)
        
        ModeGenerate = int(ModeGenerate)

        unique_file_name = uuid.uuid4().hex
        unique = f"{folderUser}/{unique_file_name}.png"
        image_save_path = image_fullpath.replace(image_name, unique)

        namaDirektori = f"Image/{folderUser}"
        Direktori = str(namaDirektori)

        if(not os.path.exists(Direktori)):
            os.mkdir(Direktori)

        #Separate Image
        img = cv2.imread(str(image_fullpath), 1)
        SeparateImage(img, Direktori)

        height, width, channels = img.shape

        img = []
        Lidi = []

        # Conver to RGBA
        img, Lidi = ConvertRGB(img, Lidi, height, Direktori)

        # Convert Binary
        Array_data = []
        Tabu_List = []

        Array_data = ConvertArrayImage(img, Array_data)

        comb = list(permutations(Lidi, 2))

        SkorArray = []
        for i in range(0, int(len(Lidi))):
            for j in range(0, int(len(Lidi)-1)):
                temp1 = Array_data[i].copy()
                temp2 = Array_data[j].copy()

                SkorArray.append(SkorPertama(temp1, temp2))
        
        #ACO
        world = pants.World(comb, SkorACO)
        solver = pants.Solver()

        comb = np.array_split(comb, height)
        PanjangLidi = int(len(Lidi))-1

        if(ModeGenerate == 1):
            Tabu_List, Best_Solution = TabuSearch(PanjangLidi, Array_data, Baris, jmlBaris, Tabu_List)
            a = Best_Solution[0]
        elif(ModeGenerate == 2):
            a = GreedySearch(PanjangLidi, comb, Baris, jmlBaris)
        elif(ModeGenerate == 3):
            a = RandomSearch(PanjangLidi, jmlBaris)
        elif(ModeGenerate == 4):
            a = ACO(solver, world, jmlBaris)
        
        img = cv2.imread(str(image_fullpath), 1)

        height, width, channels = img.shape
        img = []

        img = ConvertLiditoArray(img, height, Direktori)

        temp = a.pop()
        c = a.copy()
        c = c[::-1]

        a.append(temp)
        a.extend(c)
        b = a.copy()
        b = [x+1 for x in b]

        img = CreateImage(a, img)
        Image.fromarray(img).save(f"{namaDirektori}/Hasil1.jpg")
        
        img = Image.open(f"{namaDirektori}/Hasil1.jpg")
        img = ProcesImage(img)
        img = ScaleImage(img)
        img.save(image_save_path)

        return f"/media/{folderUser}/{unique_file_name}.png", b
def create_grids_around_black(image_path, output_path):
    """
    Create grids around black regions in the image.

    Args:
        image_path (str): Path to the input image file.
        output_path (str): Path to save the image with grids.

    Returns:
        list: List of grid coordinates created around black regions.
    """
    import cv2
    import numpy as np

    # Read the image in grayscale mode
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Failed to read image from path: {image_path}")

    # Threshold to detect black regions
    _, binary = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY_INV)

    # Create a copy of the image for visualization
    output_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # Iterate through each pixel to detect black regions and draw grids
    height, width = binary.shape
    for y in range(height):
        for x in range(width):
            if binary[y, x] == 255:  # If the pixel is black
                # Draw grid lines around the black pixel
                if x > 0 and binary[y, x - 1] == 0:
                    cv2.line(output_img, (x, y), (x, y), (0, 255, 0), 1)  # Left line
                if x < width - 1 and binary[y, x + 1] == 0:
                    cv2.line(output_img, (x, y), (x, y), (0, 255, 0), 1)  # Right line
                if y > 0 and binary[y - 1, x] == 0:
                    cv2.line(output_img, (x, y), (x, y), (0, 255, 0), 1)  # Top line
                if y < height - 1 and binary[y + 1, x] == 0:
                    cv2.line(output_img, (x, y), (x, y), (0, 255, 0), 1)  # Bottom line

    # Save the image with grids
    cv2.imwrite(output_path, output_img)

    return output_path

def create_lines_for_black_pixels(image_path, output_path, grid_size=5):
    """
    Create horizontal and vertical lines for consecutive black pixels in the image with smaller grid size.

    Args:
        image_path (str): Path to the input image file.
        output_path (str): Path to save the image with lines.
        grid_size (int): Size of the grid to process smaller areas.

    Returns:
        str: Path to the output image with lines.
    """
    import cv2
    import numpy as np

    # Read the image in grayscale mode
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Failed to read image from path: {image_path}")

    # Threshold to detect black regions
    _, binary = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY_INV)

    # Create a copy of the image for visualization
    output_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    height, width = binary.shape

    # Detect horizontal lines with smaller grid size
    for y in range(0, height, grid_size):
        start_x = None
        for x in range(width):
            if binary[y, x] == 255:  # Black pixel
                if start_x is None:
                    start_x = x
            else:
                if start_x is not None and x - start_x > 1:  # More than 1 consecutive black pixel
                    cv2.line(output_img, (start_x, y), (x - 1, y), (0, 255, 0), 1)  # Draw horizontal line
                start_x = None

    # Detect vertical lines with smaller grid size
    for x in range(0, width, grid_size):
        start_y = None
        for y in range(height):
            if binary[y, x] == 255:  # Black pixel
                if start_y is None:
                    start_y = y
            else:
                if start_y is not None and y - start_y > 1:  # More than 1 consecutive black pixel
                    cv2.line(output_img, (x, start_y), (x, y - 1), (0, 255, 0), 1)  # Draw vertical line
                start_y = None

    # Save the image with lines
    cv2.imwrite(output_path, output_img)

    return output_path

def fill_color_on_white_click(image_path, output_path, click_position, fill_color):
    """
    Fill all white regions in the image with the selected color when clicking on a white grid.

    Args:
        image_path (str): Path to the input image file.
        output_path (str): Path to save the image with filled color.
        click_position (tuple): (x, y) position of the click.
        fill_color (tuple): (B, G, R) color to fill the white regions.

    Returns:
        str: Path to the output image with filled color.
    """
    import cv2
    import numpy as np

    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Failed to read image from path: {image_path}")

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Threshold to detect white regions
    _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

    # Get the clicked position
    x, y = click_position

    # Check if the clicked position is white
    if binary[y, x] == 255:
        # Flood fill to replace all connected white regions with the fill color
        mask = np.zeros((binary.shape[0] + 2, binary.shape[1] + 2), np.uint8)
        cv2.floodFill(img, mask, (x, y), fill_color)

    # Save the image with filled color
    cv2.imwrite(output_path, img)

    return output_path

def create_grid_from_motif(image_path, output_path, grid_color=(0, 255, 0), grid_thickness=1):
    """
    Create a grid that follows the exact shape of the motif in the image.

    Args:
        image_path (str): Path to the input image file.
        output_path (str): Path to save the image with the grid.
        grid_color (tuple): Color of the grid lines (B, G, R).
        grid_thickness (int): Thickness of the grid lines.

    Returns:
        str: Path to the output image with the grid.
    """
    import cv2
    import numpy as np

    # Read the image in grayscale mode
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Failed to read image from path: {image_path}")

    # Threshold to detect the motif (black regions)
    _, binary = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY_INV)

    # Find contours of the motif
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a blank image for the grid
    grid_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # Draw grid lines following the contours of the motif
    for contour in contours:
        # Approximate the contour to reduce the number of points
        epsilon = 0.005 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Draw the contour as grid lines
        cv2.drawContours(grid_img, [approx], -1, grid_color, grid_thickness)

    # Save the image with the grid
    cv2.imwrite(output_path, grid_img)

    return output_path

   