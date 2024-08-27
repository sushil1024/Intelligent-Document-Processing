from datetime import datetime
from django.shortcuts import get_object_or_404, _get_queryset
from .models import User, Document, ExtractedText, AIResult
from .log_config import get_logger

logger = get_logger(__name__)


def adduser(username: str):
    user = User(username=username)
    user.save()
    return user


def checkuser(username: str):
    try:
        user = get_object_or_404(User, username=username)
        user.logincount += 1
        user.lastonline = datetime.now()
        user.save()
        logger.info('User data updated')
        return user
    except:
        return None


def userops(username: str):
    user = checkuser(username=username)
    if not user:
        user = adduser(username=username)
        logger.info('New User Created')
        return user
    logger.info('Existing User Updated')
    return user


def docops(user, title: str):
    docs = Document(
        user=user,
        title=title
    )
    docs.save()
    logger.info('Document Title Stored in DB')
    return docs


def extractops(document, text: str):
    ext = ExtractedText(
        document=document,
        text_content=text
    )
    ext.save()
    logger.info('Document Info Stored in DB')
    return ext


def airesops(document, ner: dict, classifications: dict, sentiment: dict):
    aires = AIResult(
        document=document,
        ner=ner,
        classifications=classifications,
        sentiment=sentiment
    )
    aires.save()
    logger.info('AI Results Stored in DB')
    return aires

