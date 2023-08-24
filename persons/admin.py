from django.contrib import admin

from .models import Comment, Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display  = ('first_name', 'last_name', 'age', 'location', 'is_found', 'reported_at',
                    'reported_by', 'reward', 'phone_to_call')
    list_filter   = ('is_found', 'reported_at',)
    search_fields = ('title', 'body')
    raw_id_fields       = ('reported_by',)
    date_hierarchy      = 'reported_at'
    list_per_page       = 10
    list_editable       = ('is_found', 'reward') 

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display  = ('person', 'name','phone','active','created')
    list_filter   = ('active','created')

    raw_id_fields       = ('person',)
    date_hierarchy      = 'created'
    list_per_page       = 10
    list_editable       = ('active',)    