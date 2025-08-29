from django.contrib import admin

from .models import Post

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','slug','author','published','status']
    list_filter = ['status','created','published','author']
    search_fields = ['title','body']
    # Pour le remplissage automatique du champ 'slug' en utilisant une version slugifier du champ title
    prepopulated_fields = {'slug':('title',)}
    # Affiche un champ de saisie d’ID brut (plutôt qu’un menu déroulant) pour le champ ForeignKey “author”.
    raw_id_fields = ['author']
    date_hierarchy = 'published'
    ordering = ['status','published']
    # Affiche les differents nombres deveant les filtres 
    show_facets=admin.ShowFacets.ALWAYS
    
    