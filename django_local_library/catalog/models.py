from django.db import models

# Create your models here.

# Used in get_absolute_url() to get URL for specified ID
from django.urls import reverse 

# Constrains fields to unique values
from django.db.models import UniqueConstraint

# Returns lower cased value of field
from django.db.models.functions import Lower


class Genre(models.Model):
    '''Model representing book genre'''

    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)"
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.name
    
    def get_absolute_url(self):
        return reverse("genre-details", args=[str(self.id)])
    
    class MetaData:
        constraits = [
            UniqueConstraint(
                Lower('name'), 
                name='genre_name_case_insensitive_unique',
                violation_error_message = "Genre already exists (case insensitive match)"
            ),
        ]


class Book(models.Model):
    '''Model representing a book'''

    title = models.CharField(max_length=200)

    author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True, blank=True)
    # Foreign Key used because book can only have one author, but authors can have multiple books.
    # Author as a string rather than object because it hasn't been declared yet in file.

    summary = models.TextField(
        max_length=1000, help_text="Enter a brief description of the book"
        )
    
    isbn = models.CharField(
        'ISBN', max_length=13,
        unique=True,
        help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                    '">ISBN number</a>'
        )

    genre = models.ManyToManyField(
        Genre, help_text="Select a genre for this book"
        )
    
    def __str__(self):
        '''String for representing Model object.'''
        return self.title
    
    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])
    

import uuid

class BookInstance(models.Model):

    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""

    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid5, 
        help_text="Unique ID for this particular book across whole library"
        )

    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    
    imprint = models.CharField(
        max_length=200
        )
    
    due_back = models.DateField(
        null=True, blank=True
        )

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default="m",
        help_text="Book availibility"
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f"{self.id} ({self.book.title})"
    
    
class Author(models.Model):
    '''a Model representing an author object.'''

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField("Dead",null=True, blank=True)

    
    def get_absolute_url(self):
        '''Returns the URL to access a particular author instance.'''
        return reverse('Author-detail', args=[str(self.id)])
    
    def __str__(self):
        '''String for representing the Model object.'''
        return f"{self.last_name}, {self.first_name}"