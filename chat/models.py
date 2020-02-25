# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging

from django.core.validators import validate_comma_separated_integer_list
from django.db import models
from jsonschema import ValidationError

from chat import choices
from chat import consts, MENU_CHOICES
from chat.utils import get_component, json_check
from django.db.models import F

model_logger = logging.getLogger('django.db.wechat')


class ChatMenu(models.Model):
    """菜单格式"""
    """自定义Model的校验和返回错误"""
    menu_json = models.TextField('菜单Json', max_length=10240, null=False, validators=[json_check])
    create_date = models.DateTimeField("创建时间", auto_now_add=True, editable=False)
    short_name = models.CharField("菜单名", max_length=32, null=False, blank=False)
    short_description = models.TextField("菜单描述", max_length=256, null=True, blank=True)
    menu_status = models.CharField("菜单状态", choices=MENU_CHOICES, default=MENU_CHOICES[1][0], max_length=16)
    chat_enable = models.NullBooleanField("同步到微信")

    # 定义发布状态的显示方式
    def menuStatus(self):
        html = ""
        if (self.menu_status == 'using'):
            html = '使用中'
        elif (self.menu_status == 'pending'):
            html = '未使用'
        return (html)

    menuStatus.short_description = '状态'
    menuStatus.admin_order_field = 'menu_status'
    status = property(menuStatus)

    class Meta:
        verbose_name = "公众号菜单"
        verbose_name_plural = "公众号菜单"
        ordering = [F('menu_status').desc(nulls_last=True), "create_date"]

    def __str__(self):
        return self.short_name


class Wechat(models.Model):
    """
    公众号
    """
    appid = models.CharField('公众号 ID', max_length=20, default='')
    alias = models.CharField('公众号名称', max_length=20, null=True, blank=True)
    service_type = models.IntegerField(
        '公众号类型', choices=choices.WECHAT_TYPE_CHOICES,
        default=consts.WECHAT_TYPE_SUB
    )
    nick_name = models.CharField('昵称', max_length=32, null=True, blank=True)
    head_img = models.URLField('头像', max_length=256, null=True, blank=True)
    user_name = models.CharField('内部名称', max_length=32)
    qrcode_url = models.URLField(
        '二维码URL', max_length=256, null=True, blank=True)
    authorized = models.BooleanField('授权')
    verify_type = models.PositiveIntegerField(
        '认证类型', choices=choices.VERIFY_TYPE_CHOICES)
    funcscope_categories = models.CharField(
        '权限集', max_length=64, validators=[validate_comma_separated_integer_list])
    join_time = models.DateTimeField('授权时间', auto_now_add=True)

    class Meta:
        get_latest_by = 'join_time'
        verbose_name = '公众号'
        verbose_name_plural = '公众号'

    def __unicode__(self):
        return '公众号 {0}'.format(self.alias)

    def __str__(self):
        return self.__unicode__().encode('utf-8')

    def is_valid(self):
        return self.authorized

    @property
    def client(self):
        component = get_component()
        return component.get_client_by_appid(self.appid)
