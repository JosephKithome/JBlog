from django.contrib import admin
from .models import *
# Register your models here.
class PostsDB(admin.ModelAdmin):
    list_display =[
        "title","author","body"
    ]

class MusicianDB(admin.ModelAdmin):
    list_display =[
        "first_name","last_name","instrument"
    ]    
admin.site.register(Post,PostsDB)  

admin.site.register(Comments)
# admin.site.register(Musician,MusicianDB) 

# class AlbulmDB(admin.ModelAdmin):
#     list_display =[
#         "artist","name","num_star","release_date"
#     ]    
# admin.site.register(Albulm,AlbulmDB) 

# class PersonDB(admin.ModelAdmin):
#     list_display =[
#         "name","shirt_size",
#     ]    
# admin.site.register(Person,PersonDB)
# admin.site.register(Student)
# admin.site.register(Blog)
# admin.site.register(Author)
# admin.site.register(Entry)