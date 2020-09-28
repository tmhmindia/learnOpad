from facilitators.models import *
from LandingPage.models import *
from learners.models import *
from LandingPage.utils import *


def base(request):
    context = cartData(request)
    context['cat']=Category.objects.all()
    return context