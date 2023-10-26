import firebase_admin
from firebase_admin import credentials, storage

class firebaseManager: 

    def __init__(self):
        self.bucket = None
        if not firebase_admin._apps:
            cred = credentials.Certificate('key.json')
            firebase_admin.initialize_app(cred, {
                'storageBucket':'fitnessdatabase-243dc.appspot.com'
            })
            self.bucket = storage.bucket()

    def uploadFile(self, fileLocation): 
        blob = self.bucket.blob(fileLocation)

        blob.upload_from_filename(fileLocation)
        blob.make_public()
        print('this file is uploaded to cloud')
        return blob.public_url