from django.urls import path 
from .import views

urlpatterns= [
    path('',views.index, name= 'index'),
    path('base/blog/', views.BlogView.as_view(), name='blog'),
    path('base/forum/', views.ForumView.as_view(), name='forum'),
    path('blog/<int:post_id>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('forum/<int:thread_id>/', views.forum_detail, name='forum_detail'),
    path('base/creer-vote/', views.creer_vote, name='creer_vote'),
    path('base/ajouter-candidat/<int:vote_id>/', views.ajouter_candidat, name='ajouter_candidat'),  
    path('base/votes/', views.liste_votes, name='liste_votes'),
    path('vote/<int:vote_id>/', views.detail_vote, name='detail_vote'), 
    path('voter/<int:vote_id>/', views.voter_candidat_view, name='voter_candidat'),
    path('preinscription/', views.preinscription, name='preinscription'),
    path('paye-en-ligne/', views.payment, name='paye_en_ligne'),
    path('contact/', views.contact, name='contact'),
    path('apropos/', views.apropos, name='apropos'),
]