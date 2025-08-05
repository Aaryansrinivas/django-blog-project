from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    path ('',views.home,name='home'),
    path('post/<int:post_id>/',views.post_detail,name='post_detail'),
    path('post/new/',views.post_new,name='post_new'),
    path('post/<int:post_id>/edit/',views.post_edit,name='post_edit'),
    path('post/<int:post_id>/delete/',views.post_delete,name='post_delete'),  
    path('like/<int:post_id>/', views.like_post, name='like_post'),   
    
     

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



