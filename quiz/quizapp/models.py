from django.db import models
from django.contrib.auth.models import User
# Create your models here.
LEIXING_CHOICES = (
(1, "SC"),
(2, "MC"),
(3, "Priority Order"),
)

#user models
class UserProfile(models.Model):
    belong_to = models.OneToOneField(User, related_name = 'profile')
    #用户名
    name = models.CharField(null = True, blank = True,max_length =20)
    #用户邮箱
    email = models.EmailField(null = True)
    #用户描述信息
    desc = models.CharField(null = True, blank = True,max_length =1000)

    def __str__(self):
        return self.name

# 题所属的章节
class ZhangJie(models.Model):
    zhangjie_title = models.CharField(max_length = 100)
    slug = models.SlugField(max_length =100,default='')

    def __str__(self):
        return self.zhangjie_title


# 问题
class Question(models.Model):
    zhangjie = models.ForeignKey(ZhangJie)
    question_text = models.CharField(max_length=1000)
    explanation = models.TextField()
    right_count = models.IntegerField(default = 0)
    wrong_count = models.IntegerField(default=0)
    #题的类型 单选题 多选题
    leixing = models.IntegerField(null = False, choices=LEIXING_CHOICES, default=1)
    pub_date = models.DateTimeField(auto_now_add=True)
    #有的题 是会有图片的
    image = models.ImageField(upload_to='photos/%Y/%m/%d',null = True, blank = True)
    #题的笔记   比如说做错了  可以记录错误的原因等等
    #ote = models.

    def __str__(self):
        return '{}{}'.format(self.id,self.question_text)

    def get_answer_choice(self):
        return self.answer_set.all()

    def get_right_answer(self):
        return self.answer_set.filter(isRight=True)

class Answer(models.Model):
    question = models.ForeignKey(Question)
    title = models.CharField(max_length=100)
    isRight = models.BooleanField()

    def __str__(self):
        #return self.title
        return '{}--{}'.format(self.id,self.title)

class userFenshu(models.Model):
    user = models.ForeignKey(User)
    pub_date = models.DateTimeField()
    fenshu = models.IntegerField()
    zhangjie = models.CharField(max_length=100)
    wrong_question = models.ManyToManyField(Question,related_name='wrong_question')
    #right_question = models.ManyToManyField(Question,related_name='right_question')
    notes = models.TextField()

    def __str__(self):
        #return "result:%d @ %s " % (self.fenshu , self.pub_date)
        return "{}'s result:{}".format(self.user , self.fenshu)
    def get_time(self):
        return "%s:%s:%s" % (self.pub_date.hour,self.pub_date.minute,self.pub_date.second)

    def get_question_zhangjie(self):
        if self.fenshu == 0 or self.fenshu == 100:
            pass
        else:
            return self.wrong_question.all()[0].zhangjie
