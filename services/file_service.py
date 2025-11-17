from datetime import datetime
import os
from werkzeug.utils import secure_filename

class FileService:
    def create_file_path(self, filename, temp_folder):
        current_time = datetime.now()
        timestamp = current_time.timestamp()

        filename = str(timestamp) + "-" + secure_filename(filename)
        file_path = os.path.join(temp_folder, filename)

        return file_path
    
    def save_file(self, file, file_path):
        with open(file_path, "wb") as f:
            f.write(file.file.read())
    
    def validate_file(self, filename: str, file_type: str):
        return filename != '' and '.' in filename and filename.rsplit('.', 1)[1].lower() in { file_type }   

    def remove_file(self, file_path):
        os.remove(file_path)
 
    


