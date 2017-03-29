from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from quizapp.models import UserProfile,Question,Answer,userFenshu,ZhangJie
from import_export.widgets import ForeignKeyWidget

# Register your models here.
class QuestionResource(resources.ModelResource):
    class Meta:
        model = Question
        skip_unchanged = True
        report_skipped = False
        fields = ('id', 'question_text', 'explanation','zhangjie','leixing')



class AnswerResource(resources.ModelResource):
    question = fields.Field(column_name='question', attribute='question', widget=ForeignKeyWidget(Question, 'question_text'))
    class Meta:
        model = Answer
        skip_unchanged = True
        report_skipped = False
        fields = ('id', 'question', 'title','isRight')

class QuestionAdmin(ImportExportModelAdmin):
    resource_class = QuestionResource
    #一般的admin配置 写在这里就可以
    search_fields = ('question_text',)
    list_display = ('question_text', 'zhangjie', 'right_count','wrong_count','leixing')

class AnswerAdmin(ImportExportModelAdmin):
    resource_class = AnswerResource
    #一般的admin配置 写在这里就可以
    search_fields = ('title',)
    #list_display = ('question','title','isRight')
    list_display = ('title','isRight')

class zhangjieAdmin(admin.ModelAdmin):
    list_display = ('zhangjie_title', 'slug')
    search_fields = ('zhangjie_title', )

    prepopulated_fields = {'slug': ('zhangjie_title', )}

admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer,AnswerAdmin)
admin.site.register(userFenshu)
admin.site.register(UserProfile)
admin.site.register(ZhangJie,zhangjieAdmin)
