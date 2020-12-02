from django.conf.urls import url
from Restaurant import views
from django.conf.urls.static import static
from django.conf import settings

# 1.在应用中进行urls配置的时候;
# (1)严格匹配开头和结尾

urlpatterns = [

                  url(r'^signin$', views.signin),  # 登录
                  url(r'^signup$', views.signup),  # 注册
                  url(r'^logout$', views.logout),  # 注销

                  url(r'^index$', views.index),  # 主页面
                  url(r'^about$', views.about),
                  url(r'^index_food$', views.index_food),
                  url(r'^about_food$', views.about_food),
                  url(r'^del_searchInfo$', views.del_searchInfo),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
