from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# django要求模型必须继承models.Model类。
# Category只需要一个简单的分类名name就可以了。
# CharField指定了分类名name的数据类型，CharField是字符型，CharField的max_length参数指定其最大长度，超过这个长度的分类名就不能被存入数据库。
# 当然django还为我们提供了多种其它的数据类型，如日期时间类型DateTimeField、整数类型IntegerField等等。
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    标签 Tag 也比较简单，和 Category 一样。
    再次强调一定要继承 models.Model 类！
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# class Post(models.Model):
#     # 文章标题
#     title = models.CharField(max_length=70)
#     # 文章正文，我们使用了 TextField。若内容不多也可以使用charfield
#     body = models.TextField()
#
#     # 这两个列分别表示文章的创建时间和最后一次修改时间，存储时间的字段用 DateTimeField 类型。
#     created_time = models.DateTimeField()
#     modified_time = models.DateTimeField()
#     # 文章摘要，可以没有文章摘要，但默认情况下 CharField 要求我们必须存入数据，否则就会报错。
#     # 指定 CharField 的 blank=True 参数值后就可以允许空值了。
#     excerpt = models.CharField(max_length=200, blank=True)
#
#     # 我们在这里把文章对应的数据库表和分类、标签对应的数据库表关联了起来，但是关联形式稍微有点不同。
#     # 我们规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以我们使用的是 ForeignKey，即一
#     # 对多的关联关系。且自 django 2.0 以后，ForeignKey 必须传入一个 on_delete 参数用来指定当关联的
#     # 数据被删除时，被关联的数据的行为，我们这里假定当某个分类被删除时，该分类下全部文章也同时被删除，因此
#     # 使用 models.CASCADE 参数，意为级联删除。
#     # 而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以我们使用
#     # ManyToManyField，表明这是多对多的关联关系。
#     # 同时我们规定文章可以没有标签，因此为标签 tags 指定了 blank=True。
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     tags = models.ManyToManyField(Tag, blank=True)
#
#     # django.contrib.auth 是 django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是
#     # django 为我们已经写好的用户模型。 这里我们通过 ForeignKey 把文章和 User 关联了起来。
#     # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和Category 类似。
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     def __str__(self):
#         return self.title


class Post(models.Model):
    title = models.CharField('标题', max_length=70)
    body = models.TextField('正文')
    modified_time = models.DateTimeField('修改时间')
    excerpt = models.CharField('摘要', max_length=200, blank=True)
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    created_time = models.DateTimeField('创建时间', default=timezone.now)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        super().save(*args, **kwargs)  # 覆写数据，只修改了modified_time
