"""easy_learn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import learn_app.views as view

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', view.home_page, name='home'),

    path('lessons/', view.lessons_list, name='lessons'),
    path('lesson/<str:id>/', view.LessonDetail.as_view(), name='lesson_detail_url'),
    path('lesson/create', view.LessonCreate.as_view(), name='lesson_create_url'),

    path('courses/', view.courses_list, name='courses'),
    path('course/create', view.CourseCreate.as_view(), name='course_create_url'),
    path('course/<str:name>', view.CourseDetail.as_view(), name='course_detail_url'),

    path('test/create', view.TestCreate.as_view(), name='test_create_url'),
    path('test/<str:id>/', view.TestDetail.as_view(), name='test_detail_url'),

    path('registration/', view.RegistrationForm.as_view(), name='registration_url'),
    #path('login/', view.LoginForm.as_view(), name='registration_url'),
    #path('logout/', view.Logout.as_view(), name='registration_url'),



]
