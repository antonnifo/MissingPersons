from django.shortcuts import get_object_or_404, redirect, render
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin

from .models import Comment, Person


def home(request):
    persons = Person.objects.all()
    
    context = {'persons': persons}
    return render(request, 'person/index.html', context)


def person_detail(request, year, month, day, person):
    person = get_object_or_404(Person,
           
                             last_name=person,
                             reported_at__year=year,
                             reported_at__month=month,
                             reported_at__day=day)

    context = {
                'person': person,
             
    }

    # hitcount logic
    hit_count = get_hitcount_model().objects.get_for_object(person)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits 

    return render(request,
                  'person/person_detail.html', context)    
                  
