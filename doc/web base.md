# Django基础

- [初始化](#初始化)
- [创建模型](#创建模型)
    - [配置sqlite3](#配置sqlite3)
    - [创建app](#创建app)
    - [配置Model](#配置Model)
- [视图和URL配置](#视图和URL配置)
- [Django站点管理](#Django站点管理)
- [HTML相关](#HTML相关)
    - [css js使用](#css js使用)
- [插件](#插件)
- [杂谈](#杂谈)

## 初始化

使用以下命令新建django项目, 之后可用manage.py启动服务.
```
django-admin startproject yourprojectname
```

## 创建模型

### 配置sqlite3

在settings.py内DATABASES中配置数据库连接属性
```python
DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_name',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '192.168.1.89',
        'PORT': '3306',
    }
}
```
随后在django目录(your project name)下的init.py添加以下代码.
```python
import pymysql

# 将所有调用的import MySQLdb导入至pymysql
pymysql.install_as_MySQLdb()
```

### 创建app

使用命令创建app, 并将你的app注册至settings.py内的INSTALLED_APPS中
```
# manage.py为项目中的manage.py(项目创建时自动创建, 用来方便与Django项目进行交互, 
# 使用python manage.py help 查看详情)
python manage.py startapp your_app
```

### 配置Model

在app内的models.py, 添加model来映射数据库表.
```python
from django.db import models

class Author(models.Model):
    """
    Django Model学习
    """
    user_id = models.CharField(max_length=36, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
```

随后使用以下命令将model同步至数据库, 实际上执行了创建表等操作.
- 创建同步命令
```
python manage.py makemigrations App
# 可以用以下命令查看执行的sql语句
    python manage.py sqlmigrate App 0001
```
- 同步至数据库
```
python manage.py migrate
```
- 点击创建项目时自动生成db.sqlite3, 配置连接属性, 无此步骤无法同步至数据库.</br><br>![配置](picture/sqlite%20cfg.png)</br>

#### Admin Model

在admin.py中使用
```python
from django.contrib import admin
from zkWeb.App.models import User, UserNode, Node

class UserNodeInline(admin.TabularInline):
    """
    根据用户管理节点信息记录(要求删除用户时, 所有与该用户相关的UserNode表记录都要删除掉)
    """
    model = UserNode
    list_display = ("node", )
    list_filter = ("user", )

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     url_path_dict = parse_url_path(request.path)
    #     if db_field.name == "user":
    #         kwargs['queryset'] = UserNode.objects.select_related("user").filter(user_id=url_path_dict[-2])
    #         return super(UserNodeInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
    #     else:
    #         return db_field.formfield(**kwargs)

class UserAdmin(admin.ModelAdmin):
    """
    用户注册信息表
    """
    inlines = [UserNodeInline]
    list_display = ("user_id", "user_name", "password", "email")        # 需要显示的字段
    search_fields = ("user_id", )                                       # 页面添加查询栏
    # list_filter = ()                                                  # 过滤

    # exclude = ("user_id", )                                           # 排除掉哪些字段可以编辑, 与fields功能相反
    fields = ("user_name", "password", "email", )

# 最后将User注册到管理后台, 就可以在后台进行管理了.
admin.site.register(User, UserAdmin)
```

## 视图和URL配置

## Django站点管理

创建超级用户可以使用命令, 也是直接登录数据库进行修改
```
python manage.py createsuperuser
```

## HTML相关

创建你的模板目录后, 在settings.py内设置模板路径. 
```
# HTML模板绝对路径
tem_path = os.path.join(os.path.join(BASE_DIR, "zkWeb"), "Templates")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 添加目录
        'DIRS': [tem_path.replace("/", "\\") if platform.architecture()[1].rfind("Windows") == 0 else tem_path],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

### css js使用

在settings.py中设置, 设置完成后可以运行python manage.py collectstatic将项目中的静态文件收集至
STATIC_ROOT中
```
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "zkWeb", "template_app", "Templates", "statics_env", "static_root")
STATICFILES_DIRS = [
    # statics下的my_static为自己的css目录, static_root为第三方模板css(内包含video js等)
    os.path.join(BASE_DIR, "zkWeb", "template_app", "Templates", "statics", "my_static")
]
```

## 插件

在MIDDLEWARE中SessionMiddleware后面添加语言可选项
```
'django.middleware.locale.LocaleMiddleware',            # 添加该项设置浏览器语言, 该项必须在SessionMiddleware之后
```

## 杂谈

为了编辑HTML文件更加方便, 请设置pycharm
<br>![pycharm settings](picture/pycharm%20settings.png)</br>
