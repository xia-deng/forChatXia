from math import ceil

from django import forms
from django.utils.safestring import mark_safe

from blog.models import Label
from forChatXia.settings import STATICFILES_DIRS, SELECT_INPUT_COLUMN_NUMBER, STATIC_URL
from utils.commonUtil import CommonUtil


class ArticleLabelSelectWidgt(forms.Widget):
    class Media:
        js = ('%sjs/jQuery-2.1.1.js' % STATIC_URL, '%sjs/article/inputAndCheckBox.js' % STATIC_URL)

    def __init__(self, attrs=None):

        super(ArticleLabelSelectWidgt, self).__init__(attrs)

    def get_name(self, labels):
        list_result=[]
        if type(labels) is str:
            for i in labels.split(","):
                list_result.append(str(i).strip())
        else:
            for i in labels:
                list_result.append(i)
        return list_result


    def render(self, name, value, attrs=None):
        # value=Article.objects.filter(title=value)#Column.objects.all()
        allLabel = Label.objects.all()
        print(type(value))
        names = self.get_name(value) if value is not None and len(value) > 0 else []
        allNames = self.get_name(allLabel)
        # html='<div style="position: relative; display: inline-block; width:100%">'
        # html+='<input class="txtValue text validation-passed" id=%s name=%s size="30" type="text" value="">' % ('id_'+name,name+'[]')
        # html+='<ul class="more_categories" id="blog_category_checkbox">'https
        # for qs in value:
        #     html+='<li><label><input type="checkbox" data-type="checkbox" data-value=%s value=%s>%s</label></li>' % (qs.namehttps,qs.id,qs.name)
        # html+='</ul></div>'
        # return html
        print(allNames)
        number = SELECT_INPUT_COLUMN_NUMBER
        html = '<table cellpadding="0" style="border:0;" cellspacing="0" class="tablist"><tr><td colspan=\"%s\">' \
               '<input class="text-field admintextinputwidget form-control txtValue" maxlength="256" required type="text" id=\"%s\" name=\"%s\" value=\"%s\" /></td></tr>' % (
               number, 'id_' + name, name, ','.join(names) + ',' if len(names) > 0 else '')

        tempHtml = html
        rows = ceil(len(allLabel) / number);
        print('rows is %s' % rows)
        for i in range(rows):
            oneRow = len(allLabel) - (i * number) if len(allLabel) - (i * number) <= number else number
            print('i is %s' % i)
            print('oneRow is %s' % oneRow)
            tempHtml += '<tr>'
            print(range(oneRow))
            for j in range(oneRow):
                print('j is %s' % j)
                index = i * number + j
                if value is not None and len(value) > 0 and len(value) > index and value[index].name in allNames:
                    tempHtml += '<td ><input type="checkbox" checked  data-type="checkbox" data-value=%s value=%s />%s </td>' % (
                        value[index].name, value[index].id, value[index].name)
                else:
                    tempHtml += '<td ><input type="checkbox"  data-type="checkbox" data-value=%s value=%s />%s </td>' % (
                             allLabel[index].name, allLabel[index].id, allLabel[index].name)

            #for j in range(oneRow):
                #print(j)
                #print('j is %s' % j)
                # index = i * number + j
                # if value is not None and len(value) > 0 and value[index].name in allNames:
                #     tempHtml += '<td ><input type="checkbox" checked  data-type="checkbox" data-value=%s value=%s />%s </td>' % (
                #         allLabel[index].name, allLabel[index].id, allLabel[index].name)
                # else:
                #     tempHtml += '<td ><input type="checkbox"  data-type="checkbox" data-value=%s value=%s />%s </td>' % (
                #     allLabel[index].name, allLabel[index].id, allLabel[index].name)
            tempHtml += '</tr>'
        tempHtml += '</table> '
        print("html is:" + tempHtml)
        return mark_safe(tempHtml)
