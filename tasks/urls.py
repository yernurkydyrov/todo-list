from django.urls import path
from .views import TaskCreate, TodoList, TaskDetail, TaskUpdate, TaskDelete, LoginView, RegisterPage
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', TodoList.as_view(), name='todo'),
    path('todo-create/', TaskCreate.as_view(), name='todo-create'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),

    path('todo/<int:pk>/', TaskDetail.as_view(), name='todo-detail'),
    path('todo-update/<int:pk>/', TaskUpdate.as_view(), name='todo-update'),
    path('todo-delete/<int:pk>/', TaskDelete.as_view(), name='todo-delete')

]
