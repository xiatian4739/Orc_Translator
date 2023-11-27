from PIL import Image, ImageQt
import io
import pytesseract

class Orc:
    def ImageFromQPixmap(self,pixmap):
        return ImageQt.fromqpixmap(pixmap)

    #将图片中的文字转换成字符串
    def image_to_string(self,img,lang):
        text = pytesseract.image_to_string(img,lang)
        return text
