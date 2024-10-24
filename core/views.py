from django.shortcuts import render,redirect, get_object_or_404
from .forms import RegisterForm,  UpdateProfileForm,CommentForumRegionForm,CommentPostForm ,CommentaireRegionBlogForm,CommentaireCelluleBlogForm,CommentaireCelluleBlogForm,CommentForumCelluleForm,ContributionForm,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse
from .models import Cellule,RegionBlogPost,CelluleBlogPost,Region,RegionForumThread,CommentaireRegionBlog,CommentaireCelluleBlog,CelluleForumThread,Contribution, Post,CommentForumRegion




def signup(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
            return redirect("signup")
        
    context = {"form":form}
    return render(request, "core/signup.html", context)

def signin (request):
    if request.method == 'POST':
        email = request.POST["email"]
        password= request.POST["password"]

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    context= {}
    return render(request, "core/login.html", context)

def signout(request):
    logout(request)
    return redirect("index")

@login_required(login_url="signin")
def profile(request, user_id=None):
    if user_id:
        user = get_object_or_404(CustomUser, id=user_id)
    else:
        user = request.user

    contribution_count = user.contributions.count()  # Utilisez le related_name si vous l'avez défini
    posts = Post.objects.filter(user=user)
    post_count = posts.count() 
    context = {
        "user": user,
        "contribution_count": contribution_count,
        'post_count': post_count,
    }
    return render(request, "core/profile.html", context)

@login_required(login_url="signin")
def contribution_detail(request, user_id=None):
    if user_id:
        user = get_object_or_404(CustomUser, id=user_id)
    else:
        user = request.user

    contributions = user.contributions.all()  # Utilisez le related_name si défini
    form = ContributionForm()

    if request.method == 'POST':
        form = ContributionForm(request.POST)
        if form.is_valid():
            contribution = form.save(commit=False)
            contribution.user = user  # Associer la contribution à l'utilisateur connecté
            contribution.save()
            return redirect('contribution_detail', user_id=user.id)

    contribution_count = contributions.count()

    context = {
        'user': user,
        'contributions': contributions,
        'form': form,
        'contribution_count': contribution_count,
    }
    return render(request, "core/contribution_detail.html", context)

@login_required(login_url="signin")
def contribution_detail_view(request, contribution_id):
    contribution = get_object_or_404(Contribution, id=contribution_id)
    context = {
        'contribution': contribution,
    }
    return render(request, "core/contribution_detail_view.html", context)


@login_required(login_url="signin")
def update_profile(request):
    user = request.user
    form = UpdateProfileForm(instance=user)

    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
            return redirect("profile")
    
    context = {"form": form}
    return render(request, "core/update_profile.html", context)

# AJAX
def load_cellules(request):
    region_id = request.GET.get('region_id')
    cellules = Cellule.objects.filter(region_id=region_id).all()
    return render(request, 'core/cellule_dropdown_list_options.html', {'cellules': cellules})



def get_cellules(request):
    region_id = request.GET.get('region')
    cellules = Cellule.objects.filter(region_id=region_id).values('id', 'nom')
    return JsonResponse(list(cellules), safe=False)


# @login_required
# def profil_partisan(request):
#     partisan = Partisan.objects.get(user=request.user)
#     contributions = Contribution.objects.filter(partisan=partisan)
#     return render(request, 'membres/profil.html', {'partisan': partisan, 'contributions': contributions})

# @login_required
# def ajouter_contribution(request):
#     if request.method == 'POST':
#         montant = request.POST.get('montant')
#         contribution = Contribution(partisan=request.user.partisan, montant=montant)
#         contribution.save()
#         return redirect('profil_partisan')
#     return render(request, 'membres/ajouter_contribution.html')

# @login_required
# def demander_adherence(request):
#     if request.method == 'POST':
#         adhésion = Adhésion(partisan=request.user.partisan)
#         adhésion.save()
#         return redirect('profil_partisan')
#     return render(request, 'membres/demander_adherence.html')


@login_required(login_url="signin")
def user_list(request):
    query = request.GET.get('q', '')
    users = CustomUser.objects.all()

    if query:
        users = users.filter(
            Q(username__icontains=query) | 
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) |
            Q(region__nom__icontains=query) |
            Q(cellule__nom__icontains=query)
        )

    context = {
        'users': users,
        'query': query,
    }
    return render(request, "core/user_list.html", context)



def list_regions(request):
    query = request.GET.get('search', '')
    regions = Region.objects.all()

    if query:
        regions = regions.filter(nom__icontains=query)

    context = {
        'regions': regions,
    }
    return render(request, 'core/list_regions.html', context)

def list_cellules(request):
    query = request.GET.get('search', '')
    cellules = Cellule.objects.all()

    if query:
        cellules = cellules.filter(nom__icontains=query)

    context = {
        'cellules': cellules,
    }
    return render(request, 'core/list_cellules.html', context)



# Vue pour afficher les blogs d'une région
def region_blog_list(request, region_id):
    blogs = RegionBlogPost.objects.filter(region_id=region_id)
    context = {'blogs': blogs, 'region': get_object_or_404(Region, id=region_id)}
    return render(request, 'core/region_blog_list.html', context)

# Vue pour afficher les blogs d'une cellule
def cellule_blog_list(request, cellule_id):
    blogs = CelluleBlogPost.objects.filter(cellule_id=cellule_id)
    context = {'blogs': blogs, 'cellule': get_object_or_404(Cellule, id=cellule_id)}
    return render(request, 'core/cellule_blog_list.html', context)

def forum_region(request, region_id):
    # Récupérer les discussions du forum pour cette région
    discussions = RegionForumThread.objects.filter(region_id=region_id)
    # Récupérer la région
    region = get_object_or_404(Region, id=region_id)
    
    # Passer les données au template
    context = {
        'forum_threads': discussions,
        'region': region
    }
    
    return render(request, 'core/forum_region.html', context)


# Vue pour afficher le forum d'une cellule
def forum_cellule(request, cellule_id):
    discussions = CelluleForumThread.objects.filter(cellule_id=cellule_id)
    cellule = get_object_or_404(Cellule, id=cellule_id)

    context = {
        'forum_threads': discussions,
        'cellule': cellule
    }

    return render(request, 'core/forum_cellule.html', context)

@login_required(login_url="signin")
def partisan_region(request, region_id):
    query = request.GET.get('q', '')
    region = get_object_or_404(Region, id=region_id)
    users = CustomUser.objects.filter(region=region)

    if query:
        users = users.filter(
            Q(username__icontains=query) | 
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)
        )

    context = {
        'users': users,
        'query': query,
        'region': region,
    }
    return render(request, "core/liste_user_region.html", context)


@login_required(login_url="signin")
def partisan_cellule(request, cellule_id):
    query = request.GET.get('q', '')
    cellule = get_object_or_404(Cellule, id=cellule_id)
    users = CustomUser.objects.filter(cellule=cellule)  # Assurez-vous que le modèle CustomUser a un champ cellule

    if query:
        users = users.filter(
            Q(username__icontains=query) | 
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)
        )

    context = {
        'users': users,
        'query': query,
        'cellule': cellule,
    }
    return render(request, "core/liste_user_cellule.html", context)


def forum_region_detail(request, thread_id):
    thread = get_object_or_404(RegionForumThread, id=thread_id)
    comments_count = thread.comments.count()  # Compte les commentaires ici

    if request.method == 'POST':
        parent_comment_id = request.POST.get('parent_comment_id')
        form = CommentForumRegionForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.thread = thread
            comment.author = request.user

            if parent_comment_id:
                comment.parent_comment = get_object_or_404(CommentForumRegion, id=parent_comment_id)

            comment.save()
            return redirect('forum_region_detail', thread_id=thread.id)

    else:
        form = CommentForumRegionForm()

    comments = thread.comments.filter(parent_comment=None)
    return render(request, 'core/forum_region_detail.html', {
        'thread': thread,
        'comments': comments,
        'form': form,
        'comments_count': comments_count  # Passer le nombre de commentaires au template
    })

 

def region_blog_detail(request, post_id):
    post = get_object_or_404(RegionBlogPost, id=post_id)
    
    if request.method == 'POST':
        form = CommentaireRegionBlogForm(request.POST)
        if form.is_valid():
            commentaire = form.save(commit=False)
            commentaire.post = post
            commentaire.author = request.user
            commentaire.save()
            return redirect('region_blog_detail', post_id=post.id)  # Redirige vers la même page pour voir le commentaire ajouté
    else:
        form = CommentaireRegionBlogForm()

    comments = post.commentaires.all()  # Récupère tous les commentaires pour ce post
    return render(request, 'core/region_blog_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })

def cellule_blog_list(request, cellule_id):
    blogs = CelluleBlogPost.objects.filter(cellule_id=cellule_id, published=True)
    cellule = get_object_or_404(Cellule, id=cellule_id)
    context = {
        'blogs': blogs,
        'cellule': cellule,
    }
    return render(request, 'core/cellule_blog_list.html', context)

def cellule_blog_detail(request, post_id):
    post = get_object_or_404(CelluleBlogPost, id=post_id)
    
    if request.method == 'POST':
        form = CommentaireCelluleBlogForm(request.POST)
        if form.is_valid():
            commentaire = form.save(commit=False)
            commentaire.post = post
            commentaire.author = request.user
            commentaire.save()
            return redirect('cellule_blog_detail', post_id=post.id)  # Redirige vers la même page pour voir le commentaire ajouté
    else:
        form = CommentaireCelluleBlogForm()

    comments = post.commentaires.all()  # Récupère tous les commentaires pour ce post
    return render(request, 'core/cellule_blog_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })

 # Assurez-vous d'avoir ce formulaire

def cellule_forum_thread_detail(request, thread_id):
    thread = get_object_or_404(CelluleForumThread, id=thread_id)
    comments_count = thread.comments.count()

    if request.method == 'POST':
        form = CommentForumCelluleForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.thread = thread
            comment.author = request.user
            comment.save()
            return redirect('cellule_forum_thread_detail', thread_id=thread.id)
    else:
        form = CommentForumCelluleForm()

    comments = thread.comments.filter(parent_comment=None)  # Récupère les commentaires principaux
    return render(request, 'core/cellule_forum_thread_detail.html', {
        'thread': thread,
        'comments': comments,
        'form': form,
        'comments_count': comments_count
    })

@login_required(login_url="signin")
def post_detail(request, user_id=None):
    user = get_object_or_404(CustomUser, id=user_id) if user_id else request.user
    posts = Post.objects.filter(user=user)
    form = PostForm()

    if request.method == 'POST' and user == request.user:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = user
            post.save()
            return redirect('post_detail', user_id=user.id)

    contribution_count = user.contributions.count()  # Ajuste cette ligne si nécessaire
    post_count = posts.count()

    context = {
        'user': user,
        'posts': posts,
        'form': form if user == request.user else None,  # Afficher le formulaire seulement pour le propriétaire
        'contribution_count': contribution_count,
        'post_count': post_count,
    }
    return render(request, "core/post_detail.html", context)



@login_required(login_url="signin")
def post_detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentPostForm()

    if request.method == 'POST':
        form = CommentPostForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail_view', post_id=post.id)  # Redirection après le commentaire

    context = {
        'post': post,
        'form': form,
    }
    return render(request, "core/post_detail_view.html", context)


@login_required(login_url="signin")
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentPostForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail_view', post_id=post.id)
    return redirect('post_detail_view', post_id=post.id)  # Redirige si pas de POST

