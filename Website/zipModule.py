import zipfile, sys, os

class ZIP:
    def __init__(self, pathAfter, pathBefore):
        self.fullpath = pathAfter
        self.fullpath2 = pathBefore
    
    def ZIPFile(self):
        image_fullpath = self.fullpath[1:]
        image_fullpath2 = self.fullpath2[1:]
        
        zip_filename = f"{image_fullpath[:-4]}.zip"
        file_name = []
        abs_file_path = []
        if os.path.exists(zip_filename):
            return f"{zip_filename}"

        else:
            files_to_zip = [f"{image_fullpath[:-4]}_grid.png", f"{image_fullpath[:-4]}_grid_red.jpg", f"{image_fullpath}", f"{image_fullpath2[:-4]}_grid.jpg", f"{image_fullpath2}"]

            output = zip_filename
            


            # create a ZipFile object in write mode
            with zipfile.ZipFile(output, 'w') as zip_file:
            # Loop through each input file path
                for file_path in files_to_zip:
                    file_name = os.path.basename(file_path)
                    # Write the file to the zip file, with the desired path
                    zip_file.write(file_path, arcname=file_name)

            
            return f"{zip_filename}"