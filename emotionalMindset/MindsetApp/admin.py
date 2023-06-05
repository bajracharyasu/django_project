from django.contrib import admin
from .models import Disease,Questions,Patient,Hospital,Contact
# Register your models here.
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ("name","description","symptoms","treatment")
admin.site.register(Disease,DiseaseAdmin)
class QuestionsAdmin(admin.ModelAdmin):
    fieldsets = [
        ("title",{"fields":["title"]}),
        ("disease",{"fields":["disease"]})
    ]
admin.site.register(Questions,QuestionsAdmin)
class PatientAdmin(admin.ModelAdmin):
    fieldsets = [
        ("name",{"fields":["name"]}),
        ("email",{"fields":["email"]}),
    ]
admin.site.register(Patient,PatientAdmin)
class HospitalAdmin(admin.ModelAdmin):
    fieldsets = [
        ("name",{"fields":["name"]}),
        ("address",{"fields":["address"]}),
        ("contact", {"fields":["contact"]}),
        ("picture",{"fields":["picture"]}),
    ]# Register your models here
admin.site.register(Hospital,HospitalAdmin)
class ContactAdmin(admin.ModelAdmin):
    fieldsets = [
        ("name",{"fields":["name"]}),
        ("email",{"fields":["email"]}),
        ("message", {"fields":["message"]}),
        ("phone",{"fields":["phone"]}),
    ]# Register your models here
admin.site.register(Contact,ContactAdmin)