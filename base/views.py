
from django.shortcuts import render, get_object_or_404,redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import BlogPost, Comment, ForumThread,Contact,Payment,Preinscription,Categoryblog,CommentForum,Vote,Candidat,UserVote
from .forms import CommentForm,ForumPostForm,ForumThreadForm,CommentForumForm,CandidatForm,PaymentForm
import string  



def index(request):
    blog_posts = BlogPost.objects.filter(published=True).order_by('-created_at')[:3]  # Récupérer les 3 derniers articles publiés
    return render(request, "base/index.html", {'blog_posts': blog_posts})

def apropos(request):
    return render(request, 'base/apropos.html')

class BlogView(View):
    def get(self, request):
        blog_posts = BlogPost.objects.all()
        comments = Comment.objects.all()
        return render(request, 'base/blog.html', {'blog_posts': blog_posts, 'comments': comments})

class ForumView(View):
    def get(self, request):
        forum_threads = ForumThread.objects.all()
        return render(request, 'base/forum.html', {'forum_threads': forum_threads})

# class VoteView(View):
#     def get(self, request):
#         voting_sessions = VotingSession.objects.all()
#         return render(request, 'base/vote.html', {'voting_sessions': voting_sessions})



class BlogDetailView(View):
    def get(self, request, post_id):
        post = get_object_or_404(BlogPost, id=post_id)
        comments = post.comments.all()
        form = CommentForm()
        return render(request, 'base/blog_detail.html', {
            'post': post,
            'comments': comments,
            'form': form,
        })

    def post(self, request, post_id):
        post = get_object_or_404(BlogPost, id=post_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog_detail', post_id=post.id)
        comments = post.comments.all()
        return render(request, 'base/blog_detail.html', {
            'post': post,
            'comments': comments,
            'form': form,
        })


# class VoteDetailView(View):
#     def get(self, request, id):
#         session = get_object_or_404(VotingSession, id=id)
#         votes = Vote.objects.filter(session=session)
#         form = VoteForm()  # Le formulaire de vote

#         return render(request, 'base/vote_detail.html', {
#             'session': session,
#             'votes': votes,
#             'form': form,
#         })

#     def post(self, request, id):
#         session = get_object_or_404(VotingSession, id=id)
#         form = VoteForm(request.POST)
        
#         if form.is_valid():
#             vote = form.save(commit=False)
#             vote.session = session
#             vote.voter = request.user  # L'utilisateur connecté
#             vote.save()
#             return redirect('vote_detail', id=session.id)  # Rediriger vers la page de détail

#         # Si le formulaire n'est pas valide, renvoyer les données existantes
#         votes = Vote.objects.filter(session=session)
#         return render(request, 'base/vote_detail.html', {
#             'session': session,
#             'form': form,
#             'votes': votes,
#         })

def add_forum_post(request):
    if request.method == 'POST':
        form = ForumPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('forum')  # Redirige après le succès
    else:
        form = ForumPostForm()
    
    return render(request, 'base/add_forum_post.html', {'form': form})


def add_forum_thread(request):
    if request.method == 'POST':
        form = ForumThreadForm(request.POST, request.FILES)
        if form.is_valid():
            forum_thread = form.save(commit=False)  # Ne sauvegarde pas tout de suite
            forum_thread.author = request.user  # Associe l'auteur
            forum_thread.save()  # Maintenant, sauvegarde
            return redirect('forum')  # Redirige après le succès
    else:
        form = ForumThreadForm()
    
    return render(request, 'base/add_forum_thread.html', {'form': form})
  # Mettez à jour l'import
def forum_detail(request, thread_id):
    thread = get_object_or_404(ForumThread, id=thread_id)

    if request.method == 'POST':
        parent_comment_id = request.POST.get('parent_comment_id')
        form = CommentForumForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.thread = thread
            comment.author = request.user

            if parent_comment_id:  # Vérifie s'il s'agit d'une réponse
                comment.parent_comment = get_object_or_404(CommentForum, id=parent_comment_id)

            comment.save()
            return redirect('forum_detail', thread_id=thread.id)

    else:
        form = CommentForumForm()

    # Filtre les commentaires pour ne récupérer que ceux de premier niveau
    comments = thread.comments.filter(parent_comment=None)
    return render(request, 'base/forum_detail.html', {'thread': thread, 'comments': comments, 'form': form})


def creer_vote(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        date_debut = request.POST.get('date_debut_votes')
        date_fin = request.POST.get('date_fin_votes')
        vote = Vote.objects.create(nom=nom, description=description, date_debut_votes=date_debut, date_fin_votes=date_fin)
        return redirect('ajouter_candidat', vote_id=vote.id)
    return render(request, 'base/creer_vote.html')

def ajouter_candidat(request, vote_id):
    vote = Vote.objects.get(id=vote_id)
    if request.method == 'POST':
        form = CandidatForm(request.POST, request.FILES)
        if form.is_valid():
            candidat = form.save(commit=False)
            candidat.vote = vote  # Lier le candidat au vote
            candidat.save()
            return redirect('ajouter_candidat', vote_id=vote.id)  # Rediriger pour ajouter d'autres candidats
    else:
        form = CandidatForm()
    return render(request, 'base/ajouter_candidat.html', {'form': form, 'vote': vote})



def liste_votes(request):
    votes = Vote.objects.all()
    return render(request, 'base/liste_votes.html', {'votes': votes})

def detail_vote(request, vote_id):
    vote = Vote.objects.get(id=vote_id)
    return render(request, 'base/detail_vote.html', {'vote': vote})

@login_required
def voter_candidat_view(request, vote_id):
    vote = get_object_or_404(Vote, id=vote_id)

    if request.method == 'POST':
        candidat_id = request.POST.get('candidat_id')
        candidat = get_object_or_404(Candidat, id=candidat_id)

        # Vérifie si l'utilisateur a déjà voté pour ce vote
        user_vote, created = UserVote.objects.get_or_create(user=request.user, vote=vote)

        if not created:
            # Si l'utilisateur a déjà voté, on décrémente le vote de l'ancien candidat
            old_candidat = user_vote.candidat
            if old_candidat:
                old_candidat.votes -= 1  # Décrémente le vote de l'ancien candidat
                old_candidat.save()

        # Met à jour le vote de l'utilisateur avec le nouveau candidat
        user_vote.candidat = candidat
        user_vote.save()

        # Incrémente le vote du nouveau candidat
        candidat.votes += 1
        candidat.save()

        return redirect('detail_vote', vote_id=vote.id)

    return render(request, 'voter.html', {'vote': vote})



punc = string.punctuation  
def contact(request):
    # return HttpResponse('contact')
    if request.method=="POST":
        print('post')
        name = request.POST['name']
        email = request.POST['email']
        number = request.POST['number']
        content = request.POST['content']
        print(name,email,content,number)
        if len(name) >1 and len(name) < 30:
            pass
        else:
            messages.error(request,'length of Name should be greater than 2 and less than 30')
            return render(request,'base/contact.html')

        if len(email) >1 and len(email) < 30:
            pass
        else:
            messages.error(request,'email is not correct try again!!')
            return render(request,'base/contact.html')
        print(len(number))
        if len(number) > 9 and len(number) < 13:
            pass
        else:
            messages.error(request,'number not correct try again!!')
            return render(request,'base/contact.html')
        ins = Contact(name=name,email=email,content=content,number=number)
        ins.save()
        messages.success(request,'Thank You for contacting me!! Your message has been saved ')
        print('data has been saved to database')
    else:
        print('not post')
    return render(request,'base/contact.html')


def preinscription(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        description = request.POST['description']
        document = request.FILES.get('document')  # Pour récupérer le fichier

        # Ajoute ici des validations si nécessaire
        if len(first_name) < 2 or len(first_name) > 30:
            messages.error(request, 'Le prénom doit avoir entre 2 et 30 caractères.')
            return render(request, 'base/preinscription.html')

        if len(last_name) < 2 or len(last_name) > 30:
            messages.error(request, 'Le nom de famille doit avoir entre 2 et 30 caractères.')
            return render(request, 'base/preinscription.html')

        # Ajoute d'autres validations si nécessaire ici

        # Enregistrement dans la base de données
        ins = Preinscription(first_name=first_name, last_name=last_name, email=email, description=description, document=document)
        ins.save()
        messages.success(request, 'Merci pour votre préinscription ! Votre message a été enregistré.')
        return render(request, 'base/preinscription.html')  # Redirige ou retourne la même page

    # Si la méthode n'est pas POST, retourne le formulaire vide
    return render(request, 'base/preinscription.html')


def payment(request):
    if request.method == "POST":
        # Récupération des données du formulaire
        transaction_id = request.POST.get('transaction_id')
        transaction_number = request.POST.get('transaction_number')

        # Ajoutez ici des validations si nécessaire
        if not transaction_id or not transaction_number:
            messages.error(request, 'Veuillez remplir tous les champs.')
            return render(request, 'base/payment.html', {'form': PaymentForm()})

        # Enregistrement dans la base de données ou traitement du paiement
        # Assurez-vous de créer une logique pour sauvegarder le paiement
        # Par exemple :
        # payment_instance = Payment(transaction_id=transaction_id, transaction_number=transaction_number)
        # payment_instance.save()

        messages.success(request, 'Votre paiement a été effectué avec succès !')
        return render(request, 'base/payment.html', {'form': PaymentForm()})

    # Si la méthode n'est pas POST, retourne le formulaire vide
    return render(request, 'base/payment.html', {'form': PaymentForm()})


