STATUS_CHOICES = (
    ("d", "丢弃"),
    ("p", "发布"),
    ("w", "草稿"),
)

Column_CN = "文章类别"
Article_CN = "文章"
Lable_CN = "标签"
Comment_CN="评论"


OPERATION_CHOICES = (
    ("r", "访问"),
    ("c", "评论"),
    ("p", "点赞"),
    ("o", "其他")
)

default_app_config = 'blog.apps.BlogConfig'
