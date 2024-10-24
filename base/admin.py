from django.contrib import admin
from .models import BlogPost, Comment, ForumThread, Preinscription,ForumPost,Categoryblog,CommentForum,Candidat,Vote,UserVote,Contact,Payment
from .forms import BlogPostForm, CommentForm, ForumThreadForm, PreinscriptionForm ,ForumPostForm,UserVoteForm,ContactForm,PaymentForm

@admin.register(Categoryblog)
class CategoryblogAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostForm
    list_display = ('title', 'author', 'created_at', 'published')
    search_fields = ('title', 'content')
    list_filter = ('published', 'created_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    form = CommentForm
    list_display = ('post', 'author', 'created_at')
    search_fields = ('content',)

class CommentForumAdmin(admin.ModelAdmin):
    list_display = ('thread', 'author', 'created_at')  # Champs à afficher dans l'admin
    search_fields = ('content',)  # Champs à rechercher
    list_filter = ('thread', 'author')  # Options de filtrage

admin.site.register(CommentForum, CommentForumAdmin)

@admin.register(ForumThread)
class ForumThreadAdmin(admin.ModelAdmin):
    form = ForumThreadForm
    list_display = ('title', 'author', 'created_at')  # Colonnes affichées
    search_fields = ('title', 'description')  # Recherche par titre et description
    fields = ('title', 'description', 'author', 'image')  # Excluez 'created_at' et 'updated_at'

    def save_model(self, request, obj, form, change):
        if not obj.author:  # Si l'auteur n'est pas défini
            obj.author = request.user  # Assigne l'utilisateur connecté comme auteur
        super().save_model(request, obj, form, change)

@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    form = ForumPostForm
    list_display = ('thread', 'author', 'created_at')
    search_fields = ('content',)

class CandidatInline(admin.TabularInline):
    model = Candidat
    extra = 1

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date_debut_votes', 'date_fin_votes')
    search_fields = ('nom',)
    list_filter = ('date_debut_votes', 'date_fin_votes')

@admin.register(Candidat)
class CandidatAdmin(admin.ModelAdmin):
    list_display = ('nom', 'vote', 'votes')
    search_fields = ('nom',)
    list_filter = ('vote',)

@admin.register(UserVote)
class UserVoteAdmin(admin.ModelAdmin):
    form = UserVoteForm  # Utiliser le formulaire personnalisé
    list_display = ('user', 'candidat', 'vote')
    search_fields = ('user__username', 'candidat__nom')
    list_filter = ('vote',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    form = ContactForm  # Utiliser le formulaire personnalisé
    list_display = ('name', 'email', 'number')  # Champs à afficher dans la liste
    search_fields = ('name', 'email')  # Champs de recherche
    ordering = ('name',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    form = PaymentForm
    list_display = ('name', 'email', 'amount', 'transaction_id')
    search_fields = ('name', 'email', 'transaction_id')
    ordering = ('name',)

@admin.register(Preinscription)
class PreinscriptionAdmin(admin.ModelAdmin):
    form = PreinscriptionForm  # Utiliser le formulaire personnalisé
    list_display = ('first_name', 'last_name', 'email')  # Champs à afficher dans la liste
    search_fields = ('first_name', 'last_name', 'email')  # Champs de recherche
    ordering = ('first_name',) 