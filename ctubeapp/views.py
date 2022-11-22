from contextvars import Context
from re import template
from django.db.models import Q
from django.shortcuts import render, redirect  #renderメソッドでhtmlへ飛ばす
from django.http import HttpResponse
import json
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView,LogoutView #auth.viewsの中のLoginviewをインポート
from django.contrib.auth import views as auth_views #viewsをインポート↑の一歩手前
from django.contrib.auth.decorators import login_required#ログインしてない時に強制リダイレクトさせる
from .models import user_expansions, category, video
from .forms import SerchForm #ユーザー登録フォームをインポート

from django.views.decorators.csrf import csrf_exempt #CSRF認証を切りたい
from django.utils.decorators import method_decorator
# Create your views here.

def zikken(request):
    group_ID= 4
    categorys = category.objects.filter(group_ID__group_ID=group_ID)
    video_infomation = video.objects.order_by("video_rank").filter(group_ID=group_ID)#.values()
    video_infomation_category1 = video.objects.filter(group_ID=group_ID, category_ID__category_ID=1)#.values()
    video_infomation_category2 = video.objects.filter(group_ID=group_ID, category_ID__category_ID=2)
    video_infomation_category3 = video.objects.filter(group_ID=group_ID, category_ID__category_ID=3)
    video_infomation_category4 = video.objects.filter(group_ID=group_ID, category_ID__category_ID=4)
    for_range = list(range(1,len(categorys)+1))
    # for i in len(categorys):
    #     exec("video_info_category{}=video.objects.filter(group_ID=group_ID, category_ID__category_ID=i)".format(i))
    context = {
            'for_range': for_range,
            'video_infomation':video_infomation,
    }

    return render(request, 'demo/zikken.html', context) 

class LogoutView(LogoutView):
    template_name = "demo/logout.html"

#初期画面。各画面に遷移するテスト用
def shokifunction(request):
    return render(request, 'j4design/shokigamen.html')
#クラスベースのログイン画面.予め用意されたものを継承して使用
@method_decorator(csrf_exempt, name='dispatch')
class Login(LoginView): 
    template_name = 'demo/login.html'

#メディアプレイヤーのviewについて
"""今はメインページからパラメータでURLを受け取っているが、ゆくゆくは、ユニークなキーを受け取って、
それでvideoテーブルをフィルターして、動画の補足情報とかも集めてプレイヤーに表示する形にしたい..。"""
#MediaPlayerのVIEW
def player_view(request):
    video_info = request.GET.get('video_info', '') #動画のURLを格納する変数.URLのパラメーターで、/?video_info=で指定した値を受け取る
    context = {'video_info': video_info}            #URLから受け取った値をparams:video_infoとして定義(辞書型)
    return render(request, 'demo/playerr.html',context )  #player.htmlにURLパラメータから受け取った値を渡す


#MediaPlayerを閉じるためのview
def close_view(request):
    return render(request, 'demo/close.html')


#メイン画面のview
@login_required
def mainpage_view(request):
#検索前か後かで分岐。セッションに保存されたフラグの存在確認を行った後、真偽判定。
    if 'search_flag' in request.session and request.session.get('search_flag') == True:
        data = request.session.get('search_info')#フォームに入力された値をセッションから取得
        form = SerchForm(data)#入力済みデータを検索窓に保持
        serch_name = data.get("Name")#検索条件が複数になった場合の処理。現状無意味。
        serch_category = data.get("category")
        str_user = str(request.user)   #ログイン中のユーザー情報の取得、以下IDの照合など
        login_user     = User.objects.get(username=str_user)
        group_ID= login_user.user_expansions.group_ID

#検索処理。動画情報とタイトルに対し、部分一致検索をかける。
        video_infomation = video.objects.order_by("video_rank").filter(
            Q(group_ID=group_ID),Q(video_info__icontains=serch_name)|
            Q(group_ID=group_ID),Q(title__icontains=serch_name)
        )
#非検索状態の処理。
    else:
        str_user = str(request.user)   #ログイン中のユーザー情報の取得
        login_user     = User.objects.get(username=str_user)
        group_ID= login_user.user_expansions.group_ID
        video_infomation = video.objects.order_by("video_rank").filter(group_ID=group_ID).values()
        video_infomation_category1 = video.objects.filter(group_ID=group_ID, category_ID__category_ID=1).values()
        video_infomation_category2 = video.objects.filter(group_ID=group_ID, category_ID__category_ID=2).values()
        video_infomation_category3 = video.objects.filter(group_ID=group_ID, category_ID__category_ID=3).values()
        video_infomation_category4 = video.objects.filter(group_ID=group_ID, category_ID__category_ID=4).values()


 #フォームに関する記述。フォームを画面に表示するときの処理と、送信ボタン押下時の処理を、requestオブジェクトによって判定 

    if request.method == 'GET':
        if request.session: #入力中のデータがあるかどうか
            form = SerchForm(request.session.get('search_info'))
        else:
            form = SerchForm()
    else:# 入力してPOSTで送信した場合
        form = SerchForm(request.POST)
        if form.is_valid():#バリデーションを通した後のデータをsessionに保存
            request.session['search_info'] = request.POST
            request.session['search_flag'] = True #検索フラグをTrueに変える。
            return redirect('main_page') #このView自身にリダイレクトする。(リダイレクトは関数の再読み込みであるので、Local変数はリセットされるよ。)

#レンダリング処理。検索したかどうかによって扱う変数が異なるので、ifで分けて記述する。
    if 'search_flag' in request.session and request.session.get('search_flag') == True:
        request.session['search_flag'] = False
        context = {
                'str_user':str_user,
                'group_ID':group_ID,
                'login_user':login_user,
                'video_infomation':video_infomation,
                'form': form,
        }
        return render(request, 'demo/main_page.html', context)
        
    else:
        context = {
                'str_user':str_user,
                'group_ID':group_ID,
                'login_user':login_user,
                'video_infomation':video_infomation,
                'video_infomation_category1':video_infomation_category1,
                'video_infomation_category2':video_infomation_category2,
                'video_infomation_category3':video_infomation_category3,
                'video_infomation_category4':video_infomation_category4,
                'form': form,
        }
        return render(request, 'demo/main_page.html', context)








"""ddddddddd"""
#ここから先j4デザイン実装

class login_j_view(LoginView):
    template_name = 'j4design/login.html'





@login_required
def main_j_view(request):
#検索前か後かで分岐。セッションに保存されたフラグの存在確認を行った後、真偽判定。
    if 'search_flag' in request.session and request.session.get('search_flag') == True:
        data = request.session.get('search_info')#フォームに入力された値をセッションから取得
        form = SerchForm(data)#入力済みデータを検索窓に保持
        serch_name = data.get("Name")#検索条件が複数になった場合の処理。現状無意味。
        str_user = str(request.user)   #ログイン中のユーザー情報の取得、以下IDの照合など
        login_user     = User.objects.get(username=str_user)
        group_ID= login_user.user_expansions.group_ID#onetooneの値を属性として取得
        categorys = category.objects.order_by("category_ID").filter(group_ID__group_ID=group_ID)

#検索処理。動画情報とタイトルに対し、部分一致検索をかける。
        video_infomation = video.objects.order_by("video_rank").filter(
            Q(group_ID=group_ID),Q(video_info__icontains=serch_name)|
            Q(group_ID=group_ID),Q(title__icontains=serch_name)
        )
#非検索状態の処理。
    else:
        str_user = str(request.user)   #ログイン中のユーザー情報の取得
        login_user     = User.objects.get(username=str_user)
        group_ID= login_user.user_expansions.group_ID
        categorys = category.objects.filter(group_ID__group_ID=group_ID)
        video_infomation = video.objects.order_by("video_rank").filter(group_ID=group_ID)#.values()



 #フォームに関する記述。フォームを画面に表示するときの処理と、送信ボタン押下時の処理を、requestオブジェクトによって判定 

    if request.method == 'GET':
        if request.session: #入力中のデータがあるかどうか
            form = SerchForm(request.session.get('search_info'))
        else:
            form = SerchForm()
    else:# 入力してPOSTで送信した場合
        form = SerchForm(request.POST)
        if form.is_valid():#バリデーションを通した後のデータをsessionに保存
            request.session['search_info'] = request.POST
            request.session['search_flag'] = True #検索フラグをTrueに変える。
            return redirect('main_j') #このView自身にリダイレクトする。(リダイレクトは関数の再読み込みであるので、Local変数はリセットされるよ。)


#レンダリング処理。検索したかどうかによって扱う変数が異なるので、ifで分けて記述する。
    if 'search_flag' in request.session and request.session.get('search_flag') == True:
        request.session['search_flag'] = False
        for_range = list(range(1,len(categorys)+1))
        context = {
                'categorys': categorys,
                'for_range': for_range,
                'str_user':str_user,
                'group_ID':group_ID,
                'login_user':login_user,
                'video_infomation':video_infomation,
                'form': form,
        }
        return render(request, 'j4design/list_base.html', context)
        
    else:
        for_range = list(range(1,len(categorys)+1))
        context = {
                'categorys': categorys,
                'for_range': for_range,
                'str_user':str_user,
                'group_ID':group_ID,
                'login_user':login_user,
                'video_infomation':video_infomation,
                'form': form,
        }
        return render(request, 'j4design/list_base.html', context)
        
        #return render(request, 'j4design/list.html', )

def palayer_j(request, pk):
    video_info = video.objects.get(id=pk)
    context = {'video_info': video_info}            #URLから受け取った値をparams:video_infoとして定義(辞書型)
    return render(request, 'j4design/player.html', context)




    # video_info = request.GET.get('video_info', '') #動画のURLを格納する変数.URLのパラメーターで、/?video_info=で指定した値を受け取る
    # context = {'video_info': video_info}            #URLから受け取った値をparams:video_infoとして定義(辞書型)
    # return render(request, 'j4design/player.html', context)
   





