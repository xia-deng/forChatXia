#-*- coding:utf-8 -*-
from __future__ import unicode_literals

import json

from django.core.exceptions import ValidationError
from wechatpy import WeChatComponent, WeChatClient
from django.conf import settings
from django.core.cache import caches
from django.utils.translation import gettext_lazy as _


def get_component():
    """
    获取开放平台API对象
    """
    component = WeChatComponent(
        settings.COMPONENT_APP_ID,
        settings.COMPONENT_APP_SECRET,
        settings.COMPONENT_APP_TOKEN,
        settings.COMPONENT_ENCODINGAESKEY,
        session=caches['wechat']
    )
    return component


def json_check(value):
    if not check_json_format(value):
        raise ValidationError(
            _('输入格式不是正确的Json，请重新输入'),
            params={'value': value},
        )


def check_json_format(raw_msg):
    """
    用于判断一个字符串是否符合Json格式
    :param self:
    :return:
    """
    if isinstance(raw_msg, str):  # 首先判断变量是否为字符串
        try:
            json.loads(raw_msg, encoding='utf-8')
        except ValueError:
            return False
        return True
    else:
        return False

def add_menu(menu_json):
    client = WeChatClient(settings.COMPONENT_APP_ID, settings.COMPONENT_APP_SECRET)
    client.menu.update(menu_json)

