from rest_framework import serializers



class PDFuploadSerializer(serializers.Serializer):
    file_upload = serializers.FileField(help_text="Upload a PDF file containing questions")

