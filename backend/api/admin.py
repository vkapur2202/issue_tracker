from django.contrib import admin

# Register your models here.
from api.models import Issue, GithubUser, Label

admin.site.register(Issue)
admin.site.register(GithubUser)
admin.site.register(Label)
