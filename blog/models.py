from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length =200)
    author = models.ForeignKey('auth.User',on_delete = models.CASCADE)
    body = models.TextField()
    date = models.DateField(default=now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

class Comments(models.Model):
    post = models.ForeignKey(Post,on_delete=CASCADE,null=True)
    owner = models.ForeignKey(to=User,on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateField(default=now)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering =['date']


# Ignore this part i was trying to  to understand django models
# #Learning Django fields
# class Musician(models.Model):
#     first_name = models.CharField(max_length =30)
#     last_name = models.CharField(max_length = 30)
#     instrument = models.CharField(max_length =100)
    
#     def __str__(self):
#         return self.first_name

#     class Meta:
#         verbose_name = "Musician"
#         verbose_name_plural = "Musicians"    

# class Albulm(models.Model):
#     artist = models.ForeignKey(Musician,on_delete = models.CASCADE)
#     name = models.CharField(max_length =100)
#     release_date = models.DateField()
#     num_star = models.IntegerField()  

#     def __str__(self):
#         return self.name
        
#     class Meta:
#         verbose_name = "Albulm"
#         verbose_name_plural = "Albulms" 


# # Django field types
# #VARCHAR
# #INTEGER


# #Field Options
# """
# null If True, Django will store empty values as NULL in the database. Default is False.
# blank If True, the field is allowed to be blank. Default is False.
# Note that this is different than null. null is purely database-related, whereas blank is validation-related. If
# a field has blank=True, form validation will allow entry of an empty value. If a field has blank=False,
# the field will be required.
# """   


# #Django choices
# """
# A sequence of 2-tuples to use 
# as choices for this field. 
# If this is given, the default
# form widget will be a
# select box instead of the standard t
# ext field and will limit choices to 
# the choices given.
# """

# class Person(models.Model):

#     SHIRT_SIZES =(
#         ('L','Large'),
#         ('M','Medium'),
#         ('S','Small')
#     )
#     name =models.CharField(max_length =20)
#     shirt_size = models.CharField(max_length=1,choices = SHIRT_SIZES)

#     def __str__(self):
#         return self.name
        
#     class Meta:
#         verbose_name = "Person"
#         verbose_name_plural = "Person" 

# #Abstract base classes
# """
# Abstract base classes are useful when you want to put some common information into a number of other models. You
# write your base class and put abstract=True in the Meta class. This model will then not be used to create any
# database table. Instead, when it is used as a base class for other models, its fields will be added to those of the child
# class."""

# class CommonInfo(models.Model):
#     name = models.CharField(max_length = 100)
#     age = models.PositiveIntegerField()

#     class Meta:
#         abstract = True
#         ordering = ["name"]

# class Student(CommonInfo):
#     home_group = models.CharField(max_length = 10)       

#     #Meta Inheritance 
#     class Meta(CommonInfo.Meta):
#         db_table = "student_info"


# class Blog(models.Model):
#     name = models.CharField(max_length = 100)
#     tagline = models.TextField()

#     def __str__(self):
#         return self.name

# class Author(models.Model):
#     name=models.CharField(max_length = 200)
#     email = models.EmailField()

#     def __str__(self):
#         return self.name

# class Entry(models.Model):
#     blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
#     headline = models.CharField(max_length=255)
#     body_text = models.TextField()
#     pub_date = models.DateField()
#     mod_date = models.DateField()
#     authors = models.ManyToManyField(Author)
#     number_of_comments = models.IntegerField()
#     number_of_pingbacks = models.IntegerField()
#     rating = models.IntegerField()

    
#     def __str__(self):
#         return self.headline               
