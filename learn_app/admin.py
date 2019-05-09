from django.contrib import admin
from .models import Course, Lesson, Test, Question, User, UserType, Group, TeacherGroup

# Register your models here.
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(User)
admin.site.register(UserType)
admin.site.register(Group)
admin.site.register(TeacherGroup)


