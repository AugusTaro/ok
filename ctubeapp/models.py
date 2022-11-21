from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ちゃんとしたDBスタート~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#1グループ：１ユーザー想定（仮にユーザーが増える場合、ユーザーの持つGIDがユニークでなくなくなる？）
class user_expansions(models.Model):
    GROUPID = (
        (1,"JA1"),
        (2,"JA2"),
        (3,"JA3"),
        (4,"JA4")
    ) 
    user       = models.OneToOneField(User, related_name='user_expansions', on_delete=models.CASCADE,null=True)#ログインユーザーの名前と結びついたkey
    user_name  = models.CharField(max_length=200,unique=True) 
    group_ID  = models.IntegerField(unique=True, choices=GROUPID)#利用するグループ数だけ選択式
    is_active = models.BooleanField(default=True, help_text='アクティブならTrue')
    def __str__(self):
        return self.user_name
class category(models.Model):
    CATEGORY = (
        (1,"カテゴリー１"),
        (2,"カテゴリー２"),
        (3,"カテゴリー３"),
        (4,"カテゴリー４")
    )
    group_ID  = models.ForeignKey(user_expansions,on_delete=models.CASCADE,db_column='group_ID', to_field='group_ID')#ユーザーに持たれる多側。カテゴリ数分だけ同名のGIDが存在。
    category_ID     = models.IntegerField(unique=True, )#ユニークであり、カテゴリに属する多数のビデオを持つ
    category_info     = models.CharField(max_length=200)#カテゴリの情報を保持
    category_rank     = models.IntegerField(default=1)
    def __str__(self):
        return str(self.category_info)

class video(models.Model):

    group_ID  = models.ForeignKey(user_expansions,on_delete=models.CASCADE,to_field='group_ID', null=True)
    category_ID= models.ForeignKey(category, on_delete=models.CASCADE, to_field='category_ID',null=True)#カテゴリ情報にアクセス
    title      = models.CharField(max_length=50)
    video_info = models.CharField(max_length=200)
    video_URL  = models.URLField(null=True)
    img_URL    = models.URLField(null=True)
    video_rank = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True, help_text='アクティブならTrue')
    def __str__(self):
        return self.title
