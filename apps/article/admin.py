from django.contrib import admin
from .models import Article, Category, Tag, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    raw_id_fields = ['article']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'author', 'views', 'publish', 'create_d', 'tag_list']
    list_display_links = ['title', 'content', 'author']
    list_filter = ['tag', 'views', 'publish', 'create_d', 'update_d']
    search_fields = ['title', 'content', 'author__name', 'tag__name']
    readonly_fields = ['views']
    inlines = [CommentInline]

    def get_queryset(self, request):
        return super(ArticleAdmin, self).get_queryset(request).prefetch_related('tag')

    def tag_list(self, Article):
        return u", ".join(o.name for o in Article.tag.all())


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
