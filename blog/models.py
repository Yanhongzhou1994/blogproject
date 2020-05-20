from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import markdown
from django.utils.html import strip_tags

class Category(models.Model):
    """
    django需求模型必须继承 models.Model类
    Category只需要一个简单的分类name就可以了
    CharField制定了分类名name的数据类型，CharField是字符类型
    CharField 的max_length参数指定其最大长度，超过这个长度的分类名就不能被存入数据库
    当然，django还为我们提供了多种其它的数据类型，如日期时间类型DateTimeField、整数类型InterField等等。
    """
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Tag(models.Model):
    """
    标签Tag也比较简单，和Category一样
    """
    name= models.CharField(max_length=100)
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Post(models.Model):
    """
    文章的数据库表稍微复杂一点，主要是设计的字段更多
    """
    # 文章标题
    title= models.CharField('标题',max_length=70)
    
    #文章正文，使用TextFiled
    #存储比较短的字符串可以使用CharField，但对于文章的正文来说可能会是一大段文本
    body = models.TextField('中文')

    #这两个列分别表示文章的创建时间和最后一次修改时间，存储时间的字段用DateTimeField
    created_time = models.DateTimeField('创建时间',default=timezone.now)
    modified_time = models.DateTimeField('修改时间')

    #文章摘要
    excerpt = models.CharField('摘要',max_length=200,blank=True)

    #这是分类与标签
    #我们在这里把文章对应的数据库和分类、标签对应的数据关联起来
    #我们规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以我们使用的是Foreignkey
    #Foreignkey必须传入一个on_delete参数来指定但关联数据被删除时，被关联数据的行为
    #on_delete = models.CASCADE表示关联数据删除时，对应文章也被删除
    # ManyToManyField，表明的是多对多的关联关系。
    # 同时我们规定文章可以没有标签，因此标签tags指定了blank=True.
    category = models.ForeignKey(Category,verbose_name='分类',on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag,blank=True)

    # 文章作者，这里User是从django.contrib.auth.models导入的
    # django.contrib.auth是django内置的应用，专门用于处理网站用户的注册、登录等流程
    # 这里我们用ForeignKey把文章和User联系起来
    author = models.ForeignKey(User,verbose_name='作者',on_delete=models.CASCADE)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def save(self,*args, **kwargs):
        self.modified_time = timezone.now()

        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            ])
        if self.excerpt is "":
            self.excerpt = strip_tags(md.convert(self.body))[:5]

        super().save(*args,**kwargs)


    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})

    def __str__(self):
        return self.title




