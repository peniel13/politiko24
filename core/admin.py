from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Region, Cellule, CustomUser,CommentPost,RegionForumThread,Post,RegionBlogPost,CelluleBlogPost,CelluleForumThread,CommentForumRegion, CommentaireRegionBlog,CommentaireCelluleBlog,CommentForumCellule,Contribution
from .forms import  RegionBlogPostForm,RegionForumThreadForm,CelluleForumThreadForm,CelluleBlogPostForm
# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'profile_pic', 'is_active',
                    'is_staff', 'is_superuser', 'last_login',)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2", "profile_pic"),
            },
        ),
    )



class RegionAdmin(admin.ModelAdmin):
    list_display = ('nom',)

class CelluleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'region')

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'region', 'cellule', 'first_name', 'last_name')
    list_filter = ('region', 'cellule')
    search_fields = ('email', 'username', 'first_name', 'last_name')

# Enregistre les modèles
admin.site.register(Region, RegionAdmin)
admin.site.register(Cellule, CelluleAdmin)



@admin.register(RegionBlogPost)
class RegionBlogPostAdmin(admin.ModelAdmin):
    form = RegionBlogPostForm
    list_display = ('title', 'author', 'created_at', 'published', 'region')
    search_fields = ('title', 'content')
    list_filter = ('published', 'created_at', 'region')

@admin.register(CommentForumRegion)
class CommentForumRegionAdmin(admin.ModelAdmin):
    list_display = ('author', 'thread', 'created_at')
    list_filter = ('thread', 'author')
    search_fields = ('content',)
    ordering = ('-created_at',)

    def author(self, obj):
        return obj.author.username  # Affiche le nom d'utilisateur de l'auteur

    author.short_description = 'Auteur'

@admin.register(RegionForumThread)
class RegionForumThreadAdmin(admin.ModelAdmin):
    form = RegionForumThreadForm
    list_display = ('title', 'author', 'created_at', 'region')
    search_fields = ('title', 'description')
    fields = ('title', 'description', 'author', 'image', 'region')

@admin.register(CelluleBlogPost)
class CelluleBlogPostAdmin(admin.ModelAdmin):
    form = CelluleBlogPostForm
    list_display = ('title', 'author', 'created_at', 'published', 'cellule')
    search_fields = ('title', 'content')
    list_filter = ('published', 'created_at', 'cellule')

@admin.register(CelluleForumThread)
class CelluleForumThreadAdmin(admin.ModelAdmin):
    form = CelluleForumThreadForm
    list_display = ('title', 'author', 'created_at', 'cellule')
    search_fields = ('title', 'description')
    fields = ('title', 'description', 'author', 'image', 'cellule')


class CommentaireRegionBlogAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    search_fields = ('content', 'author__username')  # Assurez-vous que l'utilisateur a un champ username
    list_filter = ('post', 'created_at')

admin.site.register(CommentaireRegionBlog, CommentaireRegionBlogAdmin)

class CommentaireCelluleBlogAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    search_fields = ('content', 'author__username')  # Assurez-vous que l'utilisateur a un champ username
    list_filter = ('post', 'created_at')

admin.site.register(CommentaireCelluleBlog, CommentaireCelluleBlogAdmin)

class CommentForumCelluleAdmin(admin.ModelAdmin):
    list_display = ('thread', 'author', 'created_at')
    search_fields = ('content', 'author__username')
    list_filter = ('thread', 'created_at')

admin.site.register(CommentForumCellule, CommentForumCelluleAdmin)

class ContributionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'device', 'date_time')
    list_filter = ('user',)
    search_fields = ('user__username', 'device')

admin.site.register(Contribution, ContributionAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'timestamp', 'image')
    list_filter = ('user', 'timestamp')
    search_fields = ('title', 'description')
    ordering = ('-timestamp',) # Si tu as un champ slug

admin.site.register(Post, PostAdmin)


class CommentPostAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')
    list_filter = ('post', 'user')
    search_fields = ('content',)
    ordering = ('-created_at',)

admin.site.register(CommentPost, CommentPostAdmin)
