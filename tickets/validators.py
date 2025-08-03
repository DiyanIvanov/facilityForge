from django.core.files.uploadedfile import UploadedFile
from django.forms import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class ImageSizeValidator:

    def __init__(self, img_size: int, msg=None):
        self.img_size = img_size
        self.msg = msg or f"Image size must be less than {img_size} pixels."

    def __call__(self, value: UploadedFile):
        if value.size > self.img_size:
            raise ValidationError(self.msg)


@deconstructible
class ImageValidator:
    def __init__(self, msg=None):
        self.msg = msg

    def __call__(self, value: UploadedFile):
        if not value.content_type.startswith('image/'):
            raise ValidationError(f"{value.name} is not a valid image file.")
