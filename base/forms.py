from django import forms
from .models import BlogPost, Comment, ForumThread, Preinscription,ForumPost,CommentForum,Vote,Candidat,UserVote,Contact,Payment
from django.utils import timezone

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'author', 'image', 'category']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class CommentForumForm(forms.ModelForm):
    class Meta:
        model = CommentForum
        fields = ['content']


class ForumThreadForm(forms.ModelForm):
    class Meta:
        model = ForumThread
        fields = ['title', 'description', 'image']

class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['thread', 'content', 'author', 'image']

# forms.py

class VoteForm(forms.ModelForm): 
    class Meta:
        model = Vote
        fields = ['nom', 'description', 'date_debut_votes', 'date_fin_votes']

class CandidatForm(forms.ModelForm):
    class Meta:
        model = Candidat
        fields = ['nom', 'image']


class UserVoteForm(forms.ModelForm):
    class Meta:
        model = UserVote
        fields = ['user', 'candidat', 'vote']


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'content', 'number']

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['name', 'position', 'email', 'phone', 'amount', 'device', 'transaction_id', 'transaction_number', 'description']

class PreinscriptionForm(forms.ModelForm):
    class Meta:
        model = Preinscription
        fields = ['first_name', 'last_name', 'email', 'description', 'document']
