from django.contrib import admin
from .models import Category, Tag, Post, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'publish_date', 'views_count', 'created_at')
    search_fields = ('title', 'content', 'author__username', 'category__name')
    list_filter = ('status', 'created_at', 'publish_date', 'author', 'category', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author', 'category')
    date_hierarchy = 'publish_date'
    ordering = ('-publish_date', '-created_at')
    list_per_page = 20
    actions = ['publish_posts', 'unpublish_posts']
    
    def publish_posts(self, request, queryset):
        """批量发布文章"""
        queryset.update(status='published')
    publish_posts.short_description = '批量发布所选文章'
    
    def unpublish_posts(self, request, queryset):
        """批量取消发布文章"""
        queryset.update(status='draft')
    unpublish_posts.short_description = '批量取消发布所选文章'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'parent', 'is_approved', 'created_at')
    search_fields = ('author__username', 'post__title', 'content')
    list_filter = ('is_approved', 'created_at', 'author', 'post')
    raw_id_fields = ('post', 'author', 'parent')
    ordering = ('-created_at',)
    actions = ['approve_comments', 'disapprove_comments']
    
    def approve_comments(self, request, queryset):
        """批量批准评论"""
        queryset.update(is_approved=True)
    approve_comments.short_description = '批量批准所选评论'
    
    def disapprove_comments(self, request, queryset):
        """批量拒绝评论"""
        queryset.update(is_approved=False)
    disapprove_comments.short_description = '批量拒绝所选评论'
