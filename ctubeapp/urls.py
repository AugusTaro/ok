from telnetlib import LOGOUT
from django.urls import URLPattern, path     
from .views import shokifunction#ここでVIEWS内で定義したモジュールをインポートする
from .import views
from django.contrib.auth import views as auth_views

#クラスベースで継承する場合は、views.使うview名.as_view。自分で作ったやつはviews.自分でつけた名前
urlpatterns = [
    path('',shokifunction),#各ページに遷移するテスト画面
    path('shoki/', shokifunction),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login/', views.Login.as_view(), name='login'), #クラスベースのログインページ
    path('player/', views.player_view, name='player'),#メディアプレーヤー
    path('close/', views.close_view, name='close'),
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DB改訂以降~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    path('mainpage/', views.mainpage_view, name='main_page'),
]