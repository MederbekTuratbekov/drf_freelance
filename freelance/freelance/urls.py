from django.urls import path
from .views import RegisterView, CustomLoginView, LogoutView
from .views import (UserProfileViewSet, OtherUserProfileRetrieveAPIView,
                    ProjectAPIView, ProjectDetailAPIView, UserProjectsListAPIView,
                    OfferListAPIView, UserOfferListAPIView, OfferUpdateAPIView,
                    ReviewCreateAPIView,
                    CategoryListAPIView, CategoryRetrieveAPIView,
                    SkillListAPIView)


urlpatterns = [
    path('register/', RegisterView.as_view(), name = 'register'),
    path('login/', CustomLoginView.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(), name = 'logout'),

    path('users/me/', UserProfileViewSet.as_view({'get': 'list', 'put': 'update'}), name = 'user'),
    path('users/<int:pk>/', OtherUserProfileRetrieveAPIView.as_view(), name = 'other_user'),

    path('projects/', ProjectAPIView.as_view(), name = 'projects'),
    path('projects/<int:pk>/', ProjectDetailAPIView.as_view(), name = 'project_detail'),
    path('projects/my/', UserProjectsListAPIView.as_view(), name = 'user_projects'),

    path('offers/', OfferListAPIView.as_view(), name = 'offer_click'),
    path('offers/my/', UserOfferListAPIView.as_view(), name = 'user_offers'),
    path('offers/<int:pk>/', OfferUpdateAPIView.as_view(), name = 'update_offers'),

    path('reviews/', ReviewCreateAPIView.as_view(), name = 'create_review'),

    path('categories/', CategoryListAPIView.as_view(), name='category_list'),
    path('categories/<int:pk>/', CategoryRetrieveAPIView.as_view(), name='category_detail'),

    path('skills/', SkillListAPIView.as_view(), name = 'skill_list'),
]
