# Импортируем необходимые библиотеки
import pytesseract
import spacy
from PIL import Image, ImageEnhance, ImageDraw

# Определяем функцию, которая открывает изображение, увеличивает его контрастность и считывает текст
def read_text(image_path):
    # Открываем изображение в черно-белом режиме
    image = Image.open(image_path).convert("L")
    # Увеличиваем контрастность изображения
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)
    # Считываем текст и его координаты
    result = pytesseract.image_to_data(image, lang="rus", output_type=pytesseract.Output.DICT)
    # Формируем список кортежей из текста и координат
    text_data = []
    for text, left, top, width, height in zip(result["text"], result["left"], result["top"], result["width"], result["height"]):
        if text.strip():
            text_data.append((text, [(left, top), (left + width, top), (left + width, top + height), (left, top + height)]))
    # Возвращаем результат
    return text_data

# Определяем функцию, которая проверяет текст на наличие чисел и персональных объектов и закрашивает их
def mask_text(image_path, text_data):
    # Загружаем модель для анализа текста
    nlp = spacy.load("ru_core_news_sm")
    # Открываем изображение в цветном режиме
    image = Image.open(image_path)
    # Создаем объект для рисования на изображении
    draw = ImageDraw.Draw(image)
    # Перебираем все строки текста и их координаты
    for text, coords in text_data:
        # Преобразуем текст в документ для анализа
        doc = nlp(text)
        # Перебираем все токены в документе
        for token in doc:
            # Проверяем, является ли токен числом или персональным объектом
            if token.like_num or token.ent_type_ in ["PERSON", "LOC", "ORG", "LфW", "DATE"] or (len(token.text) < 3 and not(token.is_stop)):
                # Определяем координаты токена на изображении
                start = coords[0][0]
                end = coords[1][0]
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
    image.save(image_path)


process_image(r'anon\examples\5.jpeg')