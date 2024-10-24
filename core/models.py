from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.


class Region(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Cellule(models.Model):
    nom = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to="p_img", blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    cellule = models.ForeignKey(Cellule, on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    def __str__(self):
        return self.email



# class Contribution(models.Model):
#     partisan = models.ForeignKey(Partisan, on_delete=models.CASCADE)
#     montant = models.DecimalField(max_digits=10, decimal_places=2)
#     date = models.DateTimeField(auto_now_add=True)

# class Adhésion(models.Model):
#     partisan = models.ForeignKey(Partisan, on_delete=models.CASCADE)
#     date_demande = models.DateTimeField(auto_now_add=True)
#     date_livraison = models.DateTimeField(null=True, blank=True)





class RegionBlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)
    image = models.ImageField(upload_to='region_blog_images/', blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class CommentaireRegionBlog(models.Model):
    post = models.ForeignKey(RegionBlogPost, related_name='commentaires', on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Utilisation de AUTH_USER_MODEL
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"

class CommentForumRegion(models.Model):
    thread = models.ForeignKey('RegionForumThread', related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Utilisation de AUTH_USER_MODEL
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.author} on {self.thread.title}"


class RegionForumThread(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='region_forum_images/', blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class CelluleBlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)
    image = models.ImageField(upload_to='cellule_blog_images/', blank=True, null=True)
    cellule = models.ForeignKey(Cellule, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class CommentaireCelluleBlog(models.Model):
    post = models.ForeignKey(CelluleBlogPost, related_name='commentaires', on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Utilisation de AUTH_USER_MODEL
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"


class CelluleForumThread(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='cellule_forum_images/', blank=True, null=True)
    cellule = models.ForeignKey(Cellule, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class CommentForumCellule(models.Model):
    thread = models.ForeignKey('CelluleForumThread', related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Utilisation de AUTH_USER_MODEL
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.author} on {self.thread.title}"


class Contribution(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contributions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    device = models.CharField(max_length=100)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} on {self.device} at {self.date_time}"

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class CommentPost(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'