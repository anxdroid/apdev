import base64

with open("IMG_20180215_100229.jpg", "rb") as imageFile:
    str = base64.b64encode(imageFile.read())
    print str

with open("IMG_20180215_100229.jpg", "rb") as imageFile:
    f = imageFile.read()
    b = bytearray(f)
    #print b
