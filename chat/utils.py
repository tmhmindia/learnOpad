
import io
from django.core.files.images import ImageFile
from django.core.files.base import ContentFile
import os
from django.conf import settings

from django.template.loader import get_template


def BytesToImg(image_data):
    image = ImageFile(io.BytesIO(image_data), name='foo.jpg')  # << the answer!
    return image


def BytesToFile(obj,name):
<<<<<<< HEAD
=======
   
>>>>>>> b3b8a2b7ae5d7c04559a71610ff129746e67b822
    obj = io.BytesIO(obj)
    file_content = ContentFile(obj.read())
    filename = os.path.join(settings.MEDIA_ROOT, 'msgs', name)
    print(file_content)
    return {'file_content':file_content,'filename':filename}


