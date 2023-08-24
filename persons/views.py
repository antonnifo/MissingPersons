from django.shortcuts import get_object_or_404, redirect, render
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import Comment, Person


def home(request):  

    OBJECT_LIST =  Person.objects.all()
    paginator = Paginator(OBJECT_LIST, 8)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)        
    return render(request, 'person/index.html', {
                                                   'posts' : posts,
                                                   'page' : page,
       })    


def person_detail(request, year, month, day, person):
    person = get_object_or_404(Person,
                             last_name=person,
                             reported_at__year=year,
                             reported_at__month=month,
                             reported_at__day=day)

    latest_comments = Comment.objects.filter(active=True)
    
    # List of active comments for this post
    comments = person.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':

        name  = request.POST['name']
        phone = request.POST['phone']
        comment  = request.POST['comment']

        new_comment = Comment(name=name, phone=phone,comment=comment)
        
        # Assign the current person to the comment
        new_comment.person = person
        
        new_comment.save()                             

    context = {
                'person': person,
                'latest_comments': latest_comments,
                'comments': comments,
                'new_comment': new_comment,           
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
                  
