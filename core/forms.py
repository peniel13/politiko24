from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import CustomUser, Region, Cellule,CommentPost,RegionBlogPost,Post,RegionForumThread,CelluleBlogPost,CelluleForumThread,CommentForumRegion,CommentaireRegionBlog,CommentaireCelluleBlog,CommentForumCellule,Contribution

class RegisterForm(UserCreationForm):
    email= forms.CharField(widget=forms.EmailInput(attrs={"class": "form-control", "placeholder":"Enter email adress"}))
    username= forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder":"Enter username"}))
    password1= forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder":"Enter password"}))
    password2= forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder":"confirm password"}))
    class Meta:
        model = get_user_model()
        fields = ["email","username","password1","password2"]



class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter firstname"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter lastname"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter email address"}))
    profile_pic = forms.ImageField(required=True, widget=forms.FileInput(attrs={"class": "form-control", "placeholder": "Upload image"}))
    address = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter address"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter phone"}))
    bio = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter bio"}))
    role = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter role"}))

    # Adding the region and cellule fields
    region = forms.ModelChoiceField(queryset=Region.objects.all(), widget=forms.Select(attrs={"class": "form-control"}))
    cellule = forms.ModelChoiceField(queryset=Cellule.objects.none(), widget=forms.Select(attrs={"class": "form-control"}))

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "username", "email", "address", "bio", "phone", "role", "profile_pic", "region", "cellule"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Vérifie si l'instance a une région définie
        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['cellule'].queryset = Cellule.objects.filter(region_id=region_id).order_by('nom')
            except (ValueError, TypeError):
                pass  # Invalid input from the client; ignore and fallback to empty Cellule queryset
        elif self.instance.pk:
            # Vérifie si l'instance a une région avant d'accéder à cellule_set
            if self.instance.region:
                self.fields['cellule'].queryset = self.instance.region.cellule_set.order_by('nom')


class RegionBlogPostForm(forms.ModelForm):
    class Meta:
        model = RegionBlogPost
        fields = ['title', 'content', 'author', 'image', 'region']

class CommentaireRegionBlogForm(forms.ModelForm):
    class Meta:
        model = CommentaireRegionBlog
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Votre commentaire...'}),
        }

class CommentForumRegionForm(forms.ModelForm):
    class Meta:
        model = CommentForumRegion
        fields = ['content']  # Champ à inclure dans le formulaire
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Votre commentaire...'}),
        }

class RegionForumThreadForm(forms.ModelForm):
    class Meta:
        model = RegionForumThread
        fields = ['title', 'description', 'image', 'region']

class CelluleBlogPostForm(forms.ModelForm):
    class Meta:
        model = CelluleBlogPost
        fields = ['title', 'content', 'author', 'image', 'cellule']

class CelluleForumThreadForm(forms.ModelForm):
    class Meta:
        model = CelluleForumThread
        fields = ['title', 'description', 'image', 'cellule']


class CommentaireCelluleBlogForm(forms.ModelForm):
    class Meta:
        model = CommentaireCelluleBlog
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Votre commentaire...'}),
        }

class CommentForumCelluleForm(forms.ModelForm):
    class Meta:
        model = CommentForumCellule
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Écrivez votre commentaire ici...'}),
        }

class ContributionForm(forms.ModelForm):
    class Meta:
        model = Contribution
        fields = ['amount', 'device']
        widgets = {
            'amount': forms.NumberInput(attrs={'placeholder': 'Montant'}),
            'device': forms.TextInput(attrs={'placeholder': 'Appareil'}),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'image']

class CommentPostForm(forms.ModelForm):
    class Meta:
        model = CommentPost
        fields = ['content']