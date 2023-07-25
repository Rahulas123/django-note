from django.urls import path
from .views import noteList, noteDetail, noteCreate, noteUpdate, DeleteView, CustomLoginView, RegisterPage, noteReorder
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),

    path('', noteList.as_view(), name='notes'),
    path('note/<int:pk>/', noteDetail.as_view(), name='note'),
    path('note-create/', noteCreate.as_view(), name='note-create'),
    path('note-update/<int:pk>/', noteUpdate.as_view(), name='note-update'),
    path('note-delete/<int:pk>/', DeleteView.as_view(), name='note-delete'),
    path('note-reorder/', noteReorder.as_view(), name='note-reorder'),
]
