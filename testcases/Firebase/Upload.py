import firebase_admin
from firebase_admin import credentials, storage

cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred, {
    'storageBucket':'fitnessdatabase-243dc.appspot.com'
})
bucket = storage.bucket()

blob = bucket.blob('resources/a.png')
blob.upload_from_filename('resources/a.png')
blob.make_public()
print(blob.public_url)