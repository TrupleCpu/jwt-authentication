import os
import uuid
from werkzeug.utils import secure_filename
from models.uploaded_file import UploadedFile
from models.uploaded_file import db
import logging

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file, base_folder):
    if not allowed_file(file.filename):
        raise ValueError('File type not allowed')
    
    os.makedirs(base_folder, exist_ok=True)
    filename = secure_filename(file.filename)
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    save_path = os.path.join(base_folder, unique_name)
    file.save(save_path)

    new_file = UploadedFile(filename=unique_name, file_path=save_path)
    db.session.add(new_file)
    db.session.commit()
    
    logging.info(f"File saved: {save_path}")
    return new_file

# Update service reuse the existing folder and remove the bug where after updating it gets added again in the database
def update_file(file_id, new_file, _):
    existing = UploadedFile.query.get(file_id)
    if not existing:
        raise ValueError('File not found')

    if os.path.exists(existing.file_path):
        os.remove(existing.file_path)

    existing_folder = os.path.dirname(existing.file_path)  
    os.makedirs(existing_folder, exist_ok=True)  
    filename = secure_filename(new_file.filename)
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    save_path = os.path.join(existing_folder, unique_name)  

    new_file.save(save_path)

    existing.filename = unique_name
    existing.file_path = save_path
    db.session.commit()

    logging.info(f"File updated: ID={file_id}")
    return existing


def delete_file(file_id):
    file_record = UploadedFile.query.get(file_id)
    if not file_record:
        raise ValueError('File not found')
    if os.path.exists(file_record.file_path):
        os.remove(file_record.file_path)
        logging.info(f"File deleted from storage: {file_record.file_path}")
        
    db.session.delete(file_record)
    db.session.commit()
    logging.info(f"Record deleted: ID={file_id}")