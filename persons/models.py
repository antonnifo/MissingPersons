from django.db import models
from django.contrib.auth.models import User
from hitcount.models import HitCount
from django.contrib.contenttypes.fields import GenericRelation

class Person(models.Model):

    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    age = models.PositiveIntegerField(help_text="The age of the missing person")
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    location = models.CharField(max_length=250, help_text="The last known location of the missing person")
    description = models.TextField()
    is_found = models.BooleanField(default=False)
    reported_at = models.DateTimeField(auto_now_add=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE ,related_name='persons_reported')

    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                    related_query_name='hit_count_generic_relation')

    class Meta:
        ordering = ['-reported_at']
        indexes = [
            models.Index(fields=['-reported_at']),
        ]

    def __str__(self):
        return self.last_name

    def get_absolute_url(self):
            return reverse('persons:person_detail',
                        args=[self.reported_at.year,
                                self.reported_at.month,
                                self.reported_at.day,
                                self.last_name])

class Comments(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE ,related_name='comments')
    person = models.ForeignKey(Person, on_delete=models.CASCADE ,related_name='comments')
    comment = models.TextField()
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
   
    
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.last_name