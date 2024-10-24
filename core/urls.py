from django.urls import path
from . import views 

urlpatterns = [
path('signup',views.signup, name='signup'),
path('signin',views.signin, name='signin'),
path('signout',views.signout, name='signout'),
path('profile/', views.profile, name='profile'),
path('profile/<int:user_id>/', views.profile, name='user_profile'),
path('update_profile',views.update_profile, name='update_profile'),
path('api/cellules/', views.get_cellules, name='get_cellules'),
path('load-cellules/', views.load_cellules, name='load_cellules'),
path('users/', views.user_list, name='user_list'),
path('regions/', views.list_regions, name='list_regions'),
path('cellules/', views.list_cellules, name='list_cellules'),
path('regions/<int:region_id>/blogs/', views.region_blog_list, name='blogregion'),
path('regions/<int:region_id>/forum/', views. forum_region, name='forumregion'),
path('cellules/<int:cellule_id>/blogs/', views.cellule_blog_list, name='blogcellule'),
path('cellules/<int:cellule_id>/forum/', views.forum_cellule, name='forum_cellule'),
path('region/<int:region_id>/users/', views.partisan_region, name='partisan_region'),
path('cellule/<int:cellule_id>/users/', views.partisan_cellule, name='partisan_cellule'),
path('forum/thread/<int:thread_id>/', views.forum_region_detail, name='forum_region_detail'),
path('blog/<int:post_id>/', views.region_blog_detail, name='region_blog_detail'),
path('cellule/<int:cellule_id>/blogs/', views.cellule_blog_list, name='cellule_blog_list'),
path('cellule/blog/<int:post_id>/', views.cellule_blog_detail, name='cellule_blog_detail'),
path('cellule/thread/<int:thread_id>/', views.cellule_forum_thread_detail, name='cellule_forum_thread_detail'),
path('user/<int:user_id>/contributions/', views.contribution_detail, name='contribution_detail'),  # Pour la liste de contributions
path('user/contribution_detail/<int:contribution_id>/', views.contribution_detail_view, name='contribution_detail_view'),  # Pour les détails d'une contribution
path('user/<int:user_id>/post_detail/', views.post_detail, name='post_detail'),
path('post/<int:post_id>/', views.post_detail_view, name='post_detail_view'),
path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
] 