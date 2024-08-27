import os.path
import json
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .forms import QueryForm
from .helper import process_file
from .log_config import get_logger

logger = get_logger(__name__)


# Create your views here.


def home(request):
    return render(request, 'index.html')


def inputdata(request):
    return render(request, 'input.html')


def documentprocess(request):
    logger.info('------------------------------------------------')
    logger.info('Initialized Document Processing')
    logger.info('Invoked documentprocess')
    res = 'No Content'

    if not os.path.exists('documents'):
        os.mkdir('documents')

    if request.method == 'POST':
        logger.info('POST request received')

        user = request.POST.get('user')
        title = request.POST.get('title')

        file = request.FILES.get('file_path')
        file_name = file.name
        file_content = file.read()

        # save temporary file
        with open(f'documents/{file_name}', 'wb') as f:
            f.write(file_content)

        file_path = f'documents/{file_name}'

        language = request.POST.get('langauge')

        logger.info(f"Document: {file}")
        logger.info(f"Document language: {language}")

        res = process_file(file=file_path, language=language)

        # remove saved temporary file
        if os.path.exists(file_path):
            os.remove(file_path)

        logger.info(f'Response: {res}')
        logger.info(f'Response Type: {type(res)}')

        logger.info('Concluded Document Processing')
        logger.info('------------------------------------------------')

        return JsonResponse(res)

    return render(request, 'input.html')


