from django.contrib import admin

from .models import student, subject, attendance, StudentsR, AdminR, adminsubject


admin.site.register(adminsubject)
admin.site.register(StudentsR)
admin.site.register(AdminR)
admin.site.register(student)
admin.site.register(subject)
admin.site.register(attendance)

# Register your models here.
