from django.contrib import admin

# # Register your models here.
# #显示模型（app1
# from .models import *
#
# #方法一 但不显示多个字段
# # admin.site.register(Product)
#
# ##修改title header
# admin.site.site_title = "后台管理"
# admin.site.site_header = "MyDjango"
#
# #方法二 多个字段显示 装饰器  +可搜索功能
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     #显示的字段
#     list_display = ["id",'name','weight','size','type',]
#
#     #以下为可选的搜索功能
#     search_fields = ['id','name','type__type_name']
#     list_filter = ['name','type__type_name']
#     ordering = ['id'] #降序为'-id'
#     #时间选择器  如果字段有时间格式的话
#     # data_hierarchy= Field
#     fields = ['name','weight','size','type']
#     #只可读字段 大家都一样  另一种方法，通过重写get_readonly_fields函数实现
#     #readonly_fields = ['name']
#     def get_readonly_fields(self, request, obj=None):
#         if request.user.is_superuser:
#             self.readonly_fields = []
#         else:
#             self.readonly_fields = ['name','weight']
#         return self.readonly_fields