import firebase_admin
from firebase_admin import credentials, storage

# Class that organizes and groups all code related to the storage
class firebaseManager: 
    
    # Constructor - Runs once when we use the class to create an object
    # Establishes a connection to the database
    def __init__(self):
        self.bucket = None
        if not firebase_admin._apps:
            cred = credentials.Certificate('key.json') # Provide the key(password) to the database
            firebase_admin.initialize_app(cred, {
                'storageBucket':'fitnessdatabase-243dc.appspot.com' # Provide the database name we want to connect to
            })
            self.bucket = storage.bucket() # self.bucket is a variable that contains information about the database we connected to

    # Method to upload the given file path to the database
    def uploadFile(self, fileLocation): 
        blob = self.bucket.blob(fileLocation)   # Package the file to be ready to upload

        blob.upload_from_filename(fileLocation) # Upload the file
        blob.make_public()  # Create a public link to access and download the file/ analyzed video
        print('this file is uploaded to cloud')
        return blob.public_url