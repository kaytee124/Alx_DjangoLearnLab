from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title
    
    class Meta:
        permissions = [
            ('can_add_book', 'Can add book'),
            ('can_change_book', 'Can change book'),
            ('can_delete_book', 'Can delete book'),
        ]

class Library(models.Model):
    name= models.CharField(max_length=100)
    books = models.ManyToManyField(Book, related_name='libraries')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Library'
        verbose_name_plural = 'Libraries'

class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')
    
    class Meta:
        verbose_name = 'Librarian'
        verbose_name_plural = 'Librarians'

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    ROLES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarians'),
        ('Member', 'Member'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=100, choices=ROLES)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



@receiver(post_save, sender=User)
def assign_group(sender, instance, created, **kwargs):
    if created:
        role = instance.profile.role
        group, created_group = Group.objects.get_or_create(name=role)

        if created_group:
            content_type = ContentType.objects.get_for_model(Book)

            if role == 'Admin':
                perms = ['can_add_book', 'can_change_book', 'can_delete_book']
            elif role == 'Librarian':
                perms = ['can_add_book', 'can_change_book']
            else:
                perms = []

            for codename in perms:
                permission = Permission.objects.get(
                    codename=codename,
                    content_type=content_type
                )
                group.permissions.add(permission)

        instance.groups.add(group)
