import json
from PIL import Image, ImageFilter
import pytesseract
import re

class ImageScanning:
    def __init__(self,imageName:str):
        self.imageName=imageName
        self.pSeriesPattern = re.compile('^[A-Z]{2}[0-9]{7}$')
        im = Image.open(imageName) 
        self.filteredImage = im.filter(ImageFilter.DETAIL)


    def extrackArgs(self)->str:
    
        text:str = pytesseract.image_to_string(self.filteredImage)
        lines = text.splitlines()
    
        i = 1
        for line in lines:
            if (line.strip()):
                if(i==5):
                    try:
                        l = line.replace(" ","")
                        ps = re.sub(r'\W',"",l)
                        pseries = re.match(r'^[A-Z]{2}[0-9]{7}',ps).group()
                    except AttributeError:
                        pseries = line
                if (i==7):
                    lastname=line
                if (i==9):
                    firstname=line
                if (i==14):
                    birthdate=line.replace(" ",".")
                if (i==16):
                    GenderBPlace=line.split(" ",1)
                    gender=GenderBPlace[0]
                    birthplace=GenderBPlace[1]
                if(i==20):
                    pExpiryD=line.replace(" ",".",2)
                i +=1
    
        parguments=json.dumps({"birth_date":birthdate,
        "birth_place": birthplace,
        "firstname": firstname,
        "gender": gender,
        "lastname": lastname,
        "passport_expiry_date": pExpiryD,
        "passport_number": pseries[2:],
        "passport_series": pseries[:2]})
        return parguments
