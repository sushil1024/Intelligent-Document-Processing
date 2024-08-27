from rest_framework.serializers import Serializer, FileField

# serializers define the API representation
class UploadSerializer(Serializer):
    file_uploaded = FileField()
    class Meta:
        fields = ['file_uploaded']