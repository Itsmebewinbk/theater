from django.urls import path
from api.views import (UserRegistrationView, TheaterRegistrationView, AddListTheaterView, TheaterView,
                       ScreenView, SpecificScreenView, MovieView, DeleteMovieView, ShowView, DeleteShowView,
                       MovieListView, MovieDetailView, ShowDateView, BookingView, BookingListView, BookingCancellView, AdminApprovalList,
                       AdminApproval)
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,)


urlpatterns = [
    # registeration
    path('register/', UserRegistrationView.as_view(), name='registration'),
    path('theater_register/', TheaterRegistrationView.as_view(), name='Tregistration'),
    # theater
    path('theater/', AddListTheaterView.as_view(), name='add_list_theater'),
    path('theater/<int:id>', TheaterView.as_view(), name='theater'),
    path('theater/<int:id>/screen', ScreenView.as_view(), name='screen'),
    path('screen/<int:id>', SpecificScreenView.as_view(), name='specific_screen'),
    path('screen/<int:id>/movie', MovieView.as_view(), name='movie'),
    path('movie/<int:id>/delete', DeleteMovieView.as_view(), name='delete-movie'),
    path('movie/<int:id>/show', ShowView.as_view(), name='show'),
    path('show/<int:id>', DeleteShowView.as_view(), name='del-show'),
    # customer
    path('movie/list', MovieListView.as_view(), name='movie-list'),
    path('movie/detail/<int:pk>', MovieDetailView.as_view(),
         name='movie-list-detail'),
    path('movie/detail/<int:pk>/show', ShowDateView.as_view(), name='show-date'),
    path('show/<int:pk>/book', BookingView.as_view(), name='book-show'),
    path('book/list', BookingListView.as_view(), name="book-list"),
    path('book/delete/<int:id>', BookingCancellView.as_view(), name="book-cancel"),
    # admin
    path('admin/approval-list', AdminApprovalList.as_view(),
         name="admin-approval-list"),
    path('admin/approval/<int:id>', AdminApproval.as_view(), name="admin-approval"),
    # token
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    

]
