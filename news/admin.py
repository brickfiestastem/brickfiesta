from django.contrib import admin

from .models import Article, QuestionAnswer


# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    # List display for the admin
    date_hierarchy = 'created'
    list_display = ('title', 'created')
    list_display_links = ('title',)


class QuestionAdmin(admin.ModelAdmin):
    ordering = ('question_type', 'question')
    list_filter = ('question_type',)
    list_display = ('question_type', 'question')
    list_display_links = ('question',)


admin.site.register(Article, ArticleAdmin)
admin.site.register(QuestionAnswer, QuestionAdmin)
