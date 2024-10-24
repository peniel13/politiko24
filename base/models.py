from django.db import models
from django.conf import settings
from django.utils import timezone



# Create your models here.

class Categoryblog(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Remplacé User par AUTH_USER_MODEL
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    category = models.ForeignKey(Categoryblog, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(BlogPost, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Remplacé User par AUTH_USER_MODEL
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"

class CommentForum(models.Model):
    thread = models.ForeignKey('ForumThread', related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment by {self.author} on {self.thread.title}'

class ForumThread(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)  # Champ pour la description
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='forum_images/', blank=True, null=True)

    def __str__(self):
        return self.title


class ForumPost(models.Model):
    thread = models.ForeignKey(ForumThread, related_name='posts', on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Remplacé User par AUTH_USER_MODEL
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='forum_post_images/', blank=True, null=True)

    def __str__(self):
        return f"Post by {self.author} in {self.thread}"


class Vote(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    date_debut_votes = models.DateTimeField(default=timezone.now)
    date_fin_votes = models.DateTimeField(null=True)  # Permettre NULL

    def __str__(self):
        return self.nom

    def votes_sont_ouverts(self):
        now = timezone.now()
        return self.date_debut_votes <= now <= self.date_fin_votes


class Candidat(models.Model): 
    nom = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    votes = models.IntegerField(default=0)
    vote = models.ForeignKey(Vote, related_name='candidats', on_delete=models.CASCADE, null=True)  # Permettre null

    def __str__(self):
        return self.nom

class UserVote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE)
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'vote') 

class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    email = models.EmailField(max_length=40)
    content = models.TextField(max_length=400)
    number  = models.CharField(max_length=10)

    def __str__(self):
        return (self.name)

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    position = models.CharField(max_length=40)
    email = models.EmailField(max_length=40)
    phone = models.CharField(max_length=15)  # Adjust length as needed
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    device = models.CharField(max_length=30)
    transaction_id = models.CharField(max_length=30)
    transaction_number = models.CharField(max_length=30)
    description = models.TextField(max_length=400)

    def __str__(self):
        return f"{self.name} - {self.amount}"

class Preinscription(models.Model):
    first_name = models.CharField(max_length=40)  # Nom à inscrire
    last_name = models.CharField(max_length=40)   # Postnom
    email = models.EmailField(max_length=40)       # Email
    description = models.TextField(max_length=400)  # Description
    document = models.FileField(upload_to='documents/')  # Champ pour télécharger un document

    def __str__(self):
        return f"{self.first_name} {self.last_name}"