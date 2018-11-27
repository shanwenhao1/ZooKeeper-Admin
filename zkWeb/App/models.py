from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from utils.uuid import new_uuid
from utils.time_utils import get_now_time

# Create your models here.


class User(models.Model):
    """
    用户信息表
    """
    class Meta:
        verbose_name = "ZK用户管理"
        verbose_name_plural = "ZK用户管理"

    user_id = models.CharField(max_length=36, primary_key=True, default=new_uuid)
    user_name = models.CharField(max_length=36, unique=True)
    # 性别0: 为男性, 1: 为女性
    sex = models.IntegerField(default=0, validators=[MaxValueValidator(1), MinValueValidator(0)])
    password = models.CharField(max_length=36)
    email = models.EmailField(blank=True)
    create_time = models.DateTimeField(default=get_now_time)

    def __unicode__(self):
        return self.user_id


class NodeManager(models.Manager):
    """
    为Node添加额外的方法
    """

    def node_count(self, keyword):
        return self.filter(title__icontains=keyword).count()


class Node(models.Model):
    """
    节点记录表
    """
    class Meta:
        verbose_name = "ZK节点管理"
        verbose_name_plural = "ZK节点管理"

    node_id = models.CharField(max_length=36, primary_key=True, default=new_uuid)
    node_path = models.CharField(max_length=256)
    node_name = models.CharField(max_length=128)
    # 将NodeManager()赋值给模型的objects属性
    objects = NodeManager()

    # # ManyToManyField自动维护关联表, through_fields表明Django使用那些外键
    # user_node = models.ManyToManyField(User, through='UserNode', through_fields=('node', 'user'))

    def __unicode__(self):
        return self.node_id


class UserNode(models.Model):
    """
    节点归属信息表
    """
    class Meta:
        verbose_name = "ZK节点分配管理"
        verbose_name_plural = "ZK节点分配管理"
        unique_together = ("user", "node", )

    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="用户信息")
    node = models.ForeignKey('Node', on_delete=models.CASCADE, verbose_name="节点信息")


class Contact(models.Model):
    """
    联系email类
    """
    class Meta:
        verbose_name = "contact us"
        verbose_name_plural = "contact us"

    contact_id = models.BigAutoField(primary_key=True)
    email = models.EmailField()
    full_name = models.CharField(max_length=20, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)  # 一次创建初始时间后面不会改变
    message = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.contact_id
