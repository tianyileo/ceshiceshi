
from django.conf.urls import url
from django.contrib import admin

from .views import home,practice,quiz,quiz_create,register,index_login,show_record,show_question_by_id,show_question_by_zhangjie

urlpatterns = [
    url(r'^home', home,name='home'),
    #url(r'^admin/', admin.site.urls),
    url(r'^practice/$', practice, name='practice'),
    #下面这个还没有搞出来？？？？
    #url(r'^practice/(?P<fenlei>)/(?P<q_id>\d+)', show_question_by_zhangjie_id, name='show_question_by_zhangjie_id'),
    url(r'^quiz/$',quiz,name='quiz'),
    url(r'^quiz/create/$',quiz_create,name='quiz_create'),
    url(r'^login/$',index_login,name='login'),
    url(r'^register/$',register,name='register'),
    url(r'^record/$',show_record,name='show_record'),
    url(r'^q/(?P<id>\d+)$',show_question_by_id,name='show_question_by_id'),
    #url(r'^practice/(?P<zhangjie>\w+)/$',show_question_by_zhangjie,name='show_question_by_zhangjie'),
    url(r'^practice/(?P<zhangjie>[\w\ -/:]+)/$',show_question_by_zhangjie,name='show_question_by_zhangjie'),
    #url(r'^practice/(?P<slug>.+)/$',show_question_by_zhangjie,name='show_question_by_zhangjie'),

    #以下为复制的以前的项目地址
    # url(r'$^',direct_to_template,{'template':'index.html'}),
	#url(r'^q/(?P<q_id>\d+)/$',show_question_by_id,name='show_question_by_id'),
	# url(r'^qall/$',show_all_questions,name='show_all_questions'),
	# url(r'^quiz/create/$',quiz_create,name='quiz_create'),
	# url(r'^quiz/$',quiz,name='quiz'),
	# url(r'^help/$',direct_to_template,{'template':'help.html'}),
	# url(r'^record/$',show_record,name='show_record'),
    # #以上为复制的以前的地址
]
