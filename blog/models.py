from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
# Create your models here.
from django.db.models.fields import CharField
from django.utils.html import format_html

from blog import STATUS_CHOICES, Column_CN, Lable_CN, Article_CN, OPERATION_CHOICES, Comment_CN
from forChatXia.settings import IS_POLL_NUM_EDIT, IS_COMMENT_NUM_EDIT
from froala_editor.fields import FroalaField
from utils.file import FileUtil


class Column(models.Model):
    name = models.CharField("栏目名称", max_length=56)
    # db_index创建索引字段
    slug = models.CharField("栏目索引", max_length=128, db_index=True)
    intro = models.CharField("栏目简介", default='', max_length=512)
    created_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = Column_CN
        verbose_name_plural = Column_CN
        ordering = ["created_time"]


class Label(models.Model):
    name = models.CharField("主题名称", max_length=56)
    # db_index创建索引字段
    slug = models.CharField("主题索引", max_length=128, db_index=True)
    intro = models.CharField("主题简介", default='', max_length=512)
    created_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = Lable_CN
        verbose_name_plural = Lable_CN
        ordering = ["created_time"]


# 扩展Article的manager
class ArticleManager(models.Manager):
    # 根据文章类型来查询文章
    def query_by_column(self, column_id):
        query = self.get_queryset().filter(column_id=column_id)
        return query

    # 根据用户来获取和用户相关的文章
    def query_by_user(self, user_id):
        query = User.objects.get(id=user_id)
        article_list = query.article_set.all()
        return article_list

    # 根据点赞数来排行文章列表
    def query_by_polls(self):
        query = self.get_queryset().order_by('poll_num')
        return query

    # 根据发表时间来排行文章列表
    def query_by_time(self):
        query = self.get_queryset().order_by('-pub_date')
        return query

    # 根据文章标题或内容查询文章
    def query_by_keyword(self, keyword):
        query = (self.get_queryset().filter(title__contains=keyword) |
                 self.get_queryset().filter(content__contains=keyword)).distinct()
        return query


class Article(models.Model):
    column = models.ForeignKey(Column, on_delete=models.CASCADE, verbose_name=Column_CN)
    label = models.ManyToManyField(Label, verbose_name=Lable_CN, blank=True,null=True)
    title = models.CharField("标题", max_length=128)
    slug = models.CharField("文章索引", max_length=128, db_index=True, editable=False)

    author = models.ForeignKey('auth.User', blank=True, null=True, verbose_name="作者", on_delete=models.CASCADE)
    # content = UEditorField('内容', height=300, width=800,
    #                        default=u'', blank=True, imagePath="uploads/images/",
    #                        toolbars='besttome', filePath='uploads/files/', upload_settings={"imageMaxSize":2048}, settings={}, command=None,)
    content = FroalaField('内容', theme='gray', options={'toolbarInline': False, 'height': 500})
    publish_status = CharField('状态', max_length=1, choices=STATUS_CHOICES, default= STATUS_CHOICES[2][0])

    pub_date = models.DateTimeField('发表时间', auto_now_add=True, editable=True)
    update_date = models.DateTimeField('更新时间', auto_now=True, null=True)
    read_records = models.IntegerField('阅读数', default=0, validators=[MinValueValidator(limit_value=0)])
    poll = models.IntegerField('点赞数', editable=IS_POLL_NUM_EDIT, default=0, validators=[MinValueValidator(limit_value=0)])
    comment = models.ManyToManyField('Comment', verbose_name='评论', editable=IS_COMMENT_NUM_EDIT, blank=True,null=True)

    # 定义发布状态的显示方式
    def publishStatus(self):
        html = ""
        if (self.publish_status == 'p'):
            html = '<img src="/static/admin/img/icon-yes.svg" alt="True"/>发布'
        elif (self.publish_status == 'd'):
            html = '<img src="/static/admin/img/icon-no.svg" alt="True"/>丢弃'
        else:
            html = "<i class='changelink'>草稿</i>"
        return format_html(html)

    publishStatus.short_description = '状态'
    publishStatus.admin_order_field = 'publish_status'
    status = property(publishStatus)

    def articleContent(self):
        return FileUtil.readFileLines(self.content)

    # content = property(articleContent)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = Article_CN
        verbose_name_plural = Article_CN

    # 申明自定义的Manger管理器
    objects = ArticleManager()


# 文章评论模块
class Comment(models.Model):
    author = models.CharField("发表人",null=True, max_length=128)
    content = models.CharField("评论内容",max_length=500, null=False)
    pub_date = models.DateTimeField("发表时间",auto_now_add=True, editable=False)
    # article = models.ManyToManyField(Article, verbose_name="文章", on_delete=models.CASCADE)
    poll = models.IntegerField(verbose_name="点赞", default=0, validators=[MinValueValidator(limit_value=0)])
    ip=models.GenericIPAddressField("发表地址", blank=True, null=True)
    commentChild = models.ManyToManyField('Comment', verbose_name='评论', editable=IS_COMMENT_NUM_EDIT, blank=True,null=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = Comment_CN
        verbose_name_plural = Comment_CN
        ordering = ["pub_date"]


# 点赞模块
# class Poll(models.Model):
#     author = models.CharField(null=True, max_length=128)
#     pub_date = models.DateTimeField(auto_now_add=True, editable=False)
#     comment = models.ForeignKey('Comment', verbose_name='评论', on_delete=models.CASCADE)
#     article = models.ForeignKey(Article, verbose_name="文章", on_delete=models.CASCADE)
#
# class Article_Read_Records(models.Model):
#     records_count=models.IntegerField('阅读数',default=0)

class Visit(models.Model):
    ip = models.GenericIPAddressField(verbose_name="IP")
    record_date = models.DateTimeField('记录时间', auto_now_add=True, editable=True)
    operation = models.CharField('动作', max_length=1, choices=OPERATION_CHOICES)
