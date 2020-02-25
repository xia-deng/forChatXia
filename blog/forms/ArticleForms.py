from django import forms

from blog.forms import ArticleSelectWidget
from blog.forms.ArticleSelectWidget import ArticleLabelSelectWidgt
from blog.models import Label, Article


class ArticleForm(forms.ModelForm):
    #label = forms.CharField(widget=ArticleLabelSelectWidgt, label="标签")

    label = forms.CharField(widget=ArticleLabelSelectWidgt, label="标签")


    def modelform_factory(self):
        data = self.cleaned_data['label']
        if len(data) < 1:  # 如果data不满足满足条件
            raise forms.ValidationError('请选择栏目名称')
        return data

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        #self.fields['address'].required = False

    class Meta:
        forms.model = Article
        fields = '__all__'
