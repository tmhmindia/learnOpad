from django import template
from LandingPage.models import Course
from learners.models import enrollment

register = template.Library() 

@register.filter(name='check_learner_status') 
def check_learner_status(learner, Cid):
    check=enrollment.objects.get(Lid=learner.Lid,Cid=Cid).status
    return check