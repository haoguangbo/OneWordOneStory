"""OneWordOneStory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include,url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^account/', include('account.urls')),
    url(r'^', include('main.urls')),
]


# 配置media路径（仅debug使用，deploy的时候使用nginx处理请求）
# 获取图片的url样例：http://www.hsyksx.com/media/good_pictures/图片名称.jpg
from django.conf import settings
if settings.DEBUG:
    # urlpatterns += [
    #         url(r"^media/(?P<path>.*)$", include("django.views.static.serve"), {"document_root": settings.MEDIA_ROOT,}),
    # ]
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

