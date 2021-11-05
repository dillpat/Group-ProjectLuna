from django.contrib import admin
from .models import Department, Course, Module, StudentModuleEnrolment, ModulePosts

admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(StudentModuleEnrolment)
