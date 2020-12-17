from PIL import Image, ImageDraw, ImageFont
import os
from django.conf import settings
from datetime import date
def generateCertificate(learner,course):
    font_name = ImageFont.truetype('./arial.ttf',50)
    font_course = ImageFont.truetype('./arial.ttf',30)
    font_date = ImageFont.truetype('./arial.ttf',20)
    font_founder = ImageFont.truetype('./arial.ttf',20)
    path_file = os.path.join(settings.MEDIA_ROOT,'certificates','certificate.jpg')
    img = Image.open(path_file)
    draw = ImageDraw.Draw(img)
    draw.text(xy=(325,287),text='{}'.format(learner.name),fill=(0,0,0),anchor="ms",font=font_name)
    draw.text(xy=(400,380),text='{}'.format(course.title),fill='#0b85a0',font=font_course)
    draw.text(xy=(200,533),text='{}'.format(date.today().strftime("%d/%m/%Y")),fill=(0,0,0),font=font_date)
    draw.text(xy=(580,533),text='{}'.format('Kamal Pabba'),fill=(0,0,0),font=font_founder)
    certificate_name=learner.name+str(learner.Lid)+str(course.Cid)+'.jpg'
    path = os.path.join(settings.MEDIA_ROOT,'certificates',certificate_name)
    img.save(path)
    context={
        'path':path,
        'certificate_name':certificate_name
    }
    return context