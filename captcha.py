from PIL import Image
import pytesseract
import requests
import base64
import cv2
import numpy as np
from pytesseract import image_to_string
from bs4 import BeautifulSoup
from io import BytesIO
pytesseract.pytesseract.tesseract_cmd = r'link_to /AppData/Local/Programs/Tesseract-OCR/tesseract' # put the right link to tesseract


url = "********/" # put your url
s =requests.session()
req = s.get(url)
soup = BeautifulSoup(req.text, 'lxml')
links = soup.find_all('img')
data = str(links[0])[32:-3]
im = Image.open(BytesIO(base64.b64decode(data)))
im.save('img.png', 'PNG')
## OpenCV takes over
img = cv2.imread('img.png', 0)

### Hopefully cleaning up the image ###
kernel = np.ones((1,2), np.uint8)
kernel1 = np.ones((1,1), np.uint8)

## Invert the image so we have white on black, then erode and dilate
img = cv2.bitwise_not(img)
imge = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
imge = cv2.morphologyEx(imge, cv2.MORPH_OPEN, kernel1)
print (imge)
#imge = cv2.erode(img,kernel,iterations = 1)
cv2.imwrite("closing.png", imge)

res = image_to_string(Image.open('closing.png'), lang='eng')
datac = str(res)[:-2]
print ("")
print ("This is our result: " + datac)
payload = {'submit': 'submit', 'cametu': datac}
req = s.post(url,data=payload)

if 'retente ta chance' in req.text:
	print( "retry again")
else:
	print(req.text)
