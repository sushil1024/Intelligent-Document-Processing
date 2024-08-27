from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    lastonline = models.DateTimeField(auto_now_add=True)
    logincount = models.IntegerField(default=1)

    def __str__(self):
        return self.username


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    addedon = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ExtractedText(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    text_content = models.TextField()
    addedon = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.document.title


class AIResult(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    ner = models.TextField(blank=True)
    classifications = models.TextField(blank=True)
    sentiment = models.TextField(blank=True)
    addedon = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.document.title
