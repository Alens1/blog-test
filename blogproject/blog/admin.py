from django.contrib import admin
from .models import Post, Category, Tag


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category',  'author']  # 每条记录的属性
    fields = ['title', 'body', 'excerpt', 'category', 'tags']  # 后台添加数据时会显示出来的标签

    def save_model(self, request, obj, form, change):  # 将用户创建的数据保存到数据库
        obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)

