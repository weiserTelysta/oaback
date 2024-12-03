
from rest_framework import serializers
from django.core.validators import FileExtensionValidator


class UploadImageSerializer(serializers.Serializer):
    image = serializers.ImageField(
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg','gif'])],
        error_messages={'invalid': 'Image extension must be png, jpg, jpeg, gif','required':'Please upload an image'}
    )

    def validate_image(self, value):
        max_size = 1024*1024*0.5
        size = value.size
        if size > max_size:
            raise serializers.ValidationError('Image cannot be uploaded to 0.5MB size')
        return value
