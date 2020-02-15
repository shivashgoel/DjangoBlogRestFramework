from django.urls import path,include
from . import views
from .views import PostListView,PostDetailView,post_list_update,PostAPIView,PostDetailsView,GenericAPIView

urlpatterns = [
    path('', PostListView.as_view() ,name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(),name='post-detail'),
    path('about/', views.about ,name='blog-about'),

    #Restful
    #path('api/v1/posts/list/', posts_list),
    path('api/v1/posts/update/', post_list_update),
    path('api/v1/post/apiview/' , PostAPIView.as_view()),
    path('api/v1/post/<int:id>/' , PostDetailsView.as_view()),
    path('api/v1/post/generic_view/<int:id>/' , GenericAPIView.as_view())
]
