# Импортируем необходимые библиотеки
import easyocr
import spacy
from PIL import Image, ImageEnhance, ImageDraw

# Определяем функцию, которая открывает изображение, увеличивает его контрастность и считывает текст
def read_text(image_path):
    # Открываем изображение в черно-белом режиме
    image = Image.open(image_path).convert("L")
    # Увеличиваем контрастность изображения
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)
    # Создаем объект для распознавания текста
    reader = easyocr.Reader(["ru"])
    # Считываем текст и его координаты
    result = reader.readtext(image)
    # Возвращаем результат
    return result

# Определяем функцию, которая проверяет текст на наличие чисел и персональных объектов и закрашивает их
def mask_text(image_path, text_data):
    # Загружаем модель для анализа текста
    nlp = spacy.load("ru_core_news_sm")
    # Открываем изображение в цветном режиме
    image = Image.open(image_path).convert("RGB")
    # Создаем объект для рисования на изображении
    draw = ImageDraw.Draw(image)
    # Перебираем все строки текста и их координаты
    for text, coords in text_data:
        # Преобразуем текст в документ для анализа
        doc = nlp(text)
        # Перебираем все токены в документе
        for token in doc:
            # Проверяем, является ли токен числом или персональным объектом
            if token.like_num or token.ent_type_ in ["PERSON", "LOC"] or len(token.text) < 3:
                # Определяем координаты токена на изображении
                start = int(token.idx / len(text) * (coords[1][0] - coords[0][0]) + coords[0][0])
                end = int((token.idx + len(token)) / len(text) * (coords[1][0] - coords[0][0]) + coords[0][0])
                top = coords[0][1]
                bottom = coords[3][1]
                # Закрашиваем токен черным цветом
                draw.rectangle([start, top, end, bottom], fill="black")
    # Возвращаем измененное изображение
    return image

# Определяем функцию, которая объединяет две предыдущие функции
def process_image(image_path):
    # Считываем текст с изображения
    text_data = read_text(image_path)
    # Закрашиваем текст на изображении
    image = mask_text(image_path, text_data)
    # Возвращаем изображение
    return image

# Применяем функцию к примеру изображения
image = process_image("example.jpg")
# Сохраняем изображение
image.save("output.jpg")
