import hashlib

from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserForm, RegisterForm
from login import models

from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url


# def login(request):
#     # 验证码图片生成
#     hashkey = CaptchaStore.generate_key()
#     imgage_url = captcha_image_url(hashkey)
#
#
#     if request.method == "POST":
#         username = request.POST.get('username', None)
#         password = request.POST.get('password', None)
#         vcode = request.POST.get('vcode')
#         vcode_key = request.POST.get('hashkey')
#         # 验证查询数据库生成正确的码
#         get_captcha = CaptchaStore.objects.get(hashkey=vcode_key)
#
#         message = "所有字段都必须填写！"
#         if username and password:  # 确保用户名和密码都不为空
#             username = username.strip()
#             # 用户名字符合法性验证
#             # 密码长度验证
#             # 更多的其它验证.....
#             try:
#                 user = models.User.objects.get(name=username)
#                 if user.password == password:
#                     if vcode.lower() == get_captcha.response:
#                         messages.add_message(request, messages.SUCCESS, '用户登录成功！', extra_tags='success')
#                         return redirect('/index')
#                     else:
#                         return render(request, 'login/login.html', locals())
#                 else:
#                     message = "密码不正确！"
#             except:
#                 message = "用户名不存在！"
#             return render(request, 'login/login.html', locals())
#     login_form = UserForm()
#     return render(request, 'login/login.html', locals())


def login(request):
    if request.session.get('is_login', None):
        return redirect('/index')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            try:
                user = models.User.objects.get(name=username)
                if user.password == hash_code(password):  # 哈希值和数据库内的值进行比对
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    request.session['user_avatar'] = str(user.avatar)
                  #  headimage = user.avatar
                    # return render(request, 'blog/index.html', locals())
                    return redirect("/index")
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login/login.html', locals())

    login_form = UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST, request.FILES)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            avatar = register_form.cleaned_data['avatar']

            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = hash_code(password1)  # 使用加密密码
                new_user.email = email
                new_user.sex = sex
                new_user.avatar = avatar
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    else:

        register_form = RegisterForm()
    print(register_form.errors)
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/index")


def hash_code(s, salt='mysite'):  # 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()
