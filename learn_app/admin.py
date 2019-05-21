from django.contrib import admin
from .models import Course, Lesson, Test, Question, User, UserType, Group, TeacherGroup, TestResult, UserAnswer, UserGroup, Material, MaterialType

# Register your models here.
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(User)
admin.site.register(UserType)
admin.site.register(Group)
admin.site.register(TeacherGroup)
admin.site.register(TestResult)
admin.site.register(UserAnswer)
admin.site.register(UserGroup)
admin.site.register(Material)
admin.site.register(MaterialType)


