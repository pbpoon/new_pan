from django.contrib import admin
from .models import Article, Author, Category, Tag, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    raw_id_fields = ['article']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'author', 'likes', 'views', 'publish', 'create_d', 'update_d']
    list_display_links = ['title', 'content', 'author']
    list_filter = ['tag', 'likes', 'views', 'publish', 'create_d', 'update_d']
    search_fields = ['title', 'content', 'author__name', 'tag__name']
    readonly_fields = ['likes', 'views']
    inlines = [CommentInline]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass



