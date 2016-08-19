from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User,AnonymousUser
from django.views.decorators.http import require_http_methods
import django.contrib.auth as auth #用户登录认证
from django.contrib.auth.decorators import login_required,permission_required
from main.models import *
import datetime
from django.utils import timezone
import json

import logging
from django.shortcuts import redirect

# Get an instance of a logger
logger = logging.getLogger('django')

def user_identify(request):
    return {
        'has_logged_in': not isinstance(request.user,AnonymousUser),
        'user':request.user
    }



@require_http_methods(["GET"])
def index(request):
    context=user_identify(request)
    context['stories']=Story.objects.order_by('-publish_time')[:30]
    return render(request,'index.html',context)



@login_required
@require_http_methods(["GET","POST"])
def story_add(request):
    if request.method=='GET': #GET请求
        context = user_identify(request)
        res=render(request,'story_add.html',context)
    else: #POST请求
        story=Story.objects.create(first_word=request.POST['first_word'],create_user=request.user)
        data={
            'status':'success',
            'story_id':story.id
        }
        res=HttpResponse(json.dumps(data), content_type="application/json")
    return res



@require_http_methods(["GET"])
def story_detail(request,story_id):
    context = user_identify(request)
    story=Story.objects.get(id=story_id)
    context['story']=story
    context['words']=story.words.order_by('publish_time')
    return render(request,'story_detail.html',context)


@login_required
@require_http_methods(["POST"])
def story_reply(request,story_id):
    if request.POST['word']:
        Word.objects.create(text=request.POST['word'],story=Story.objects.get(id=story_id),user=request.user)
        res=HttpResponse('success', content_type="text/plain")
    else:
        res=HttpResponse('fail', content_type="text/plain")
    return res


@login_required
@require_http_methods(["GET"])
def me_created(request):
    context = user_identify(request)
    context['stories']=request.user.stories.order_by('-publish_time')[:30]
    return render(request, 'me_created.html', context)


@login_required
@require_http_methods(["GET"])
def me_participated(request):
    context = user_identify(request)
    context['words']=request.user.words.order_by('-publish_time')[:30]
    return render(request, 'me_participated.html', context)


@login_required
@require_http_methods(["GET"])
def me_setting(request):
    context = user_identify(request)
    return render(request, 'me_setting.html', context)


@login_required
@require_http_methods(["GET","POST"])
def me_modify(request):
    context = user_identify(request)
    return render(request, 'me_modify.html', context)


@login_required
@require_http_methods(["POST"])
def me_avatar(request):
    context = user_identify(request)
    if request.FILES['avatar']:
        context['status'] = 'fail' #默认状态是fail
        logger.info(request.FILES['avatar'])
        if request.FILES['avatar'].size>204000:
            context['status'] = 'too_big'
        else:
            avatar = request.user.person.avatar
            logger.info(request.FILES['avatar'].size)
            # 如果原来的不是默认头像，就把旧头像先删掉
            if avatar.url != '/media/avatar_default.png':
                avatar.delete()  # 删除旧的头像
            avatar.save(request.FILES['avatar'].name, request.FILES['avatar'])
            context['status'] = 'success'

    return render(request, 'me_avatar.html', context)



@login_required
@require_http_methods(["GET"])
def about(request):
    context = user_identify(request)
    return render(request, 'about.html', context)