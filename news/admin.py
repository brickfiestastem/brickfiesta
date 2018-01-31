from django.contrib import admin
from .models import Article, QuestionAnswer
# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    # List display for the admin
    date_hierarchy = 'created'
    list_display = ('title', 'body', 'created')


admin.site.register(Article, ArticleAdmin)
admin.site.register(QuestionAnswer)
