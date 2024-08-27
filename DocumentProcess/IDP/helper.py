import os
from PIL import Image
from pdf2image import convert_from_path
import pytesseract as ts
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from .log_config import get_logger

logger = get_logger(__name__)

# library paths
ts.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'    # OCR - Install tesseract from 'https://github.com/UB-Mannheim/tesseract/wiki'
poppler_path = 'C:\\Program Files\\poppler-24.07.0\\Library\\bin'                   # pdf to img convert - Install Poppler from 'https://github.com/oschwartz10612/poppler-windows/releases'

tokenizer = AutoTokenizer.from_pretrained('dslim/bert-base-NER')
model = AutoModelForTokenClassification.from_pretrained('dslim/bert-base-NER')

nlp = pipeline('ner', model=model, tokenizer=tokenizer)

classifier = pipeline('text-classification', model='distilbert-base-uncased-finetuned-sst-2-english')

sentiment_analysis = pipeline('sentiment-analysis')


def read_img(file, lang='eng'):
    logger.info('Invoked read_img()')
    text = ts.image_to_string(Image.open(file), lang=lang)

    # write to txt file
    # output_file = os.path.splitext(file)[0] + '.txt'
    # with open(output_file, 'w', encoding='utf-8') as f:
    #     f.write(text)

    return text


def read_pdf(file, lang='eng'):
    logger.info('Invoked read_pdf()')
    # convert to img
    images = convert_from_path(file, poppler_path=poppler_path)

    pages = []  # text for each page
    logger.info('Initializing document convertion')
    for i, image in enumerate(images):
        filename = os.path.basename(file) + '_page_' + str(i) + '.jpg'
        image.save(filename, 'jpeg')
        logger.info('Document converted')

        text = ts.image_to_string(filename, lang=lang)
        logger.info('Text extracted')
        pages.append(text)
        if os.path.exists(os.path.basename(file) + '_page_' + str(i) + '.jpg'):
            os.remove(os.path.basename(file) + '_page_' + str(i) + '.jpg')
        logger.info('Temporary image file(s) purged')

    content = '\n'.join(pages)
    logger.info('Content joined')

    # write to txt file
    # output_file = os.path.splitext(file)[0] + '.txt'
    # with open(output_file, 'w', encoding='utf-8') as f:
    #     f.write(content)

    return content


def is_pdf(file: str):
    return file.lower().endswith('.pdf')


def is_img(file: str):
    if file.lower().endswith('.jpg') or file.lower().endswith('.jpeg') or file.lower().endswith('.png'):
        return True


def getLanguage(lang):
    if lang.lower().startswith('eng'):
        return 'eng'
    elif lang.lower().startswith('mar'):
        return 'mar'
    elif lang.lower().startswith('hin'):
        return 'hin'
    else:
        exit('Invalid language')


def process_file(file, language):
    language = getLanguage(lang=language)
    text = 'Not Found'
    if is_pdf(file):
        text = read_pdf(file=file, lang=language)
    elif is_img(file):
        text = read_img(file=file, lang=language)
    else:
        exit('Invalid File Type')

    if len(text) < 512:
        ner_result = nlp(text)
        category = classifier(text)
        sentiment = sentiment_analysis(text)
    else:
        ner_result = {}
        category = {}
        sentiment = {}

    if ner_result:
        ner_result[0]['score'] = float(ner_result[0]['score'])
    if category:
        category[0]['score'] = float(category[0]['score'])
    if sentiment:
        sentiment[0]['score'] = float(sentiment[0]['score'])

    res = {
        'status': 200,
        'text': text,
        'NER': ner_result,
        'category': category,
        'sentiment': sentiment
    }

    return res


if __name__ == '__main__':
    file = input(str('File Path: '))
    lang = input(str('File Language: '))

    process_file(file=file, language=lang)

    # example = 'Albert Einstein was born in Ulm, Germany, in 1879 and later moved to Princeton, New Jersey.'
    #
    # # NER
    # ner_result = nlp(example)
    # print(ner_result)
    #
    # # categorize / sentiment analysis
    # category = sentiment_analysis(example)
    # print(category)
