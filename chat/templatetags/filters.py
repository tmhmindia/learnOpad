from base64 import b64encode
from django import template
from LandingPage.models import *
register = template.Library()

@register.filter
def bin_2_img(_bin):
    if _bin is not None: return b64encode(_bin).decode('utf-8')
@register.filter(name='getVideos')
def getVideos(id):
    video=CourseVdeo.objects.get(Vid=id)
    return video



