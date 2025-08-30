from django.urls import reverse
from django.utils import timezone
from django.db import models
from django.conf import settings

# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT='DF','Draft'
        PUBLISHED = 'PB','publish'
    
    objects = models.Manager() # manager par default
    publish = PublishedManager() #notre manager customiser
    
    title = models.CharField(max_length=255)
    
    # Champ slug utilisé souvent pour les URLs, limité à 250 caractères.
    slug = models.SlugField(max_length=250,unique_for_date='published')
    
    body = models.TextField()
    
    # Date et heure de publication, par défaut la date 
    # et heure actuelle au moment de la création.
    published = models.DateTimeField(default=timezone.now)
    
    # Date et heure de création du post (remplie 
    # automatiquement à l’insertion dans la base).
    # Ne se met PAS à jour par la suite.
    created = models.DateTimeField(auto_now_add=True)
    
    # Date et heure de la dernière modification.
    # Mise à jour automatiquement chaque fois
    # qu’on appelle `save()` sur l’objet
    updated = models.DateTimeField(auto_now=True)
    
    status = models.CharField(max_length=2,choices=Status,default=Status.DRAFT)
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_post'
    )
    
    class Meta:
        ordering=['-published']
        # index dans la bd
        indexes = [models.Index(fields=['-published'])]
        
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[
            self.published.year,
            self.published.month,
            self.published.day,
            self.slug])
    