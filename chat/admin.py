import wechatpy
from django.contrib import admin

# Register your models here.
from chat import MENU_CHOICES
from chat.models import ChatMenu
from chat.utils import add_menu
from forChatXia.settings import PER_PAGE_SHOW


class MenuAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'status', 'create_date')
    list_per_page = PER_PAGE_SHOW
    radio_fields = {"menu_status": admin.HORIZONTAL}
    exclude = ("chat_enable",)

    # 自定义操作
    actions = ['make_enable', 'chat_publish']

    def make_enable(self, request, queryset):
        if (len(queryset) > 1):
            self.message_user(request, "一次只能有一个菜单被激活.", extra_tags=", fail_silently=False")

        else:
            exsitUsing = ChatMenu.objects.filter(menu_status=MENU_CHOICES[0][0])
            message_bit=""
            if len(exsitUsing) > 0:
                message_bit = "菜单：%s 被关闭，" % exsitUsing[0]
                exsitUsing.update(menu_status=MENU_CHOICES[1][0])
            if queryset[0].menu_status is not MENU_CHOICES[0][0]:
                rows_updated = queryset.update(menu_status=MENU_CHOICES[0][0])
            message_bit = message_bit + '菜单：%s 被激活' % queryset[0]
            self.message_user(request, message_bit)

    make_enable.short_description = "激活本地菜单"

    def chat_publish(self, request, queryset):
        if (len(queryset) > 1 or not (queryset[0].menu_status).__eq__(MENU_CHOICES[0][0])):
            self.message_user(request, "只能同步一个[激活菜单]到微信公众号.", extra_tags=", fail_silently=False")
        else:
            try:
                existChat = ChatMenu.objects.filter(chat_enable=True)
                message_bit = ""
                if len(existChat) > 0:
                    message_bit = "菜单：%s 被取消同步，" % existChat[0]
                    existChat.update(chat_enable=False)
                if queryset[0].chat_enable is None or queryset[0].chat_enable is False:
                    rows_updated = queryset.update(chat_enable=True)
                message_bit = message_bit + '菜单：%s 被同步到微信' % queryset[0]
                self.message_user(request, message_bit)
                # add_menu(str(queryset[0].menu_json).encode("utf-8"))
                wechatpy.messages.TextMessage("测试菜单")
            except Exception as e:
                print(e)
                self.message_user(request, "同步菜单到微信失败")

    chat_publish.short_description = "同步菜单到微信"


admin.site.register(ChatMenu, MenuAdmin)
