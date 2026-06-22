from django.urls import path
from proctor import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('exam/', views.exam, name='exam'),
    path('start_detection/', views.start_detection, name='start_detection'),
    path('stop_detection/', views.stop_detection, name='stop_detection'),
]


if __name__ == '__main__':
    print('proctor.urls is not intended to be run directly. Include it in Django urlpatterns instead.')