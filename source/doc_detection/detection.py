import easyocr
from PIL import Image, ImageFilter
""" 

path = r'X:\hackatone\back\back\source\doc_detection\input\2.jpg'

def text_recognition(file_path):
    reader = easyocr.Reader(['ru'])
    result = reader.readtext(file_path)

    return
def main():
    file_path = path
    print(text_recognition(file_path=file_path))
    
if __name__ == "__main__":
    main() """
def find_size(chords, line):
    height = chords[line][0][2][1]-chords[line][0][0][1]
    width = chords[line][0][2][0]-chords[line][0][0][0]
    size = [height, width]
    return size

def find_word(stroke, line):
    word = stroke[line][1]
    return word

def find_start(stroke, line):
    

reader = easyocr.Reader(['ru'])
result = reader.readtext(r'source\doc_detection\input\3.jpg')
print('СТрока: ', result[0])
print('Слово: ', result[0][1])
print('Chords ', result[0][0])

""" def addMask ( image_path, mask_array):
    doc_img = Image.open(image_path)
    doc_img.load()
    try:
        for item in mask_array:
            mask = Image.new('RGB', (mask_array[item][0][0], mask_array[item][0][1]),(0,0,0))
            doc_img.paste(mask,(mask_array[item][1][0], mask_array[item][1][1]))

    except:
        print('file ',item,' not found') """
""" 
mask = Image.new('RGB', [400,100] ,(0,0,0))
doc = r'source\doc_detection\input\3.jpg'

doc_img = Image.open(doc)  
doc_img.load()
doc_img.paste(mask,[96,126])
doc_img.show() """