from django.db import models
import django.utils.timezone as timezone


# Create your models here.
class Restaurant(models.Model):
    '''餐馆表'''
    id = models.AutoField(primary_key=True)
    business_id = models.CharField(max_length=50, verbose_name='ID', unique=True)
    name = models.CharField(max_length=100, verbose_name='餐馆名称')
    address = models.CharField(max_length=500, verbose_name='餐厅地址')
    city = models.CharField(max_length=500, verbose_name='所在城市')
    state = models.CharField(max_length=500, verbose_name='所在州')
    postal_code = models.CharField(max_length=100, verbose_name='邮编')
    latitude = models.CharField(max_length=40, verbose_name='经度')
    longitude = models.CharField(max_length=40, verbose_name='纬度')
    stars = models.CharField(max_length=20, verbose_name='星级')
    review_count = models.CharField(max_length=20, verbose_name='评论计数')
    is_open = models.CharField(max_length=20, verbose_name='是否开业')
    categories = models.CharField(max_length=20, verbose_name='分类')

    class Meta:
        managed: True
        verbose_name = '餐馆信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Atttributes(models.Model):
    '''atttributes息表'''

    id = models.AutoField(primary_key=True)
    business_id = models.ForeignKey(to='Restaurant', to_field='id', on_delete=models.CASCADE, verbose_name='餐馆id')
    BusinessAcceptsCreditCards = models.CharField(max_length=20, verbose_name='商业信用状态')
    BikeParking = models.CharField(max_length=20, verbose_name='是否有自行车停车位')
    GoodForKids = models.CharField(max_length=20, verbose_name='对孩子是否友好')
    BusinessParking = models.CharField(max_length=20, verbose_name='商业停车')
    ByAppointmentOnly = models.CharField(max_length=20, verbose_name='未知')
    RestaurantsPriceRange2 = models.CharField(max_length=20, verbose_name='价格')

    class Meta:
        managed: True
        verbose_name = 'atttributes信息'
        verbose_name_plural = verbose_name


class Hours(models.Model):
    '''开业时间信息表'''

    id = models.AutoField(primary_key=True)
    business_id = models.ForeignKey(to='Restaurant', to_field='id', on_delete=models.CASCADE, verbose_name='餐馆id')
    Monday = models.CharField(max_length=100, verbose_name='周一开业时间')
    Tuesday = models.CharField(max_length=100, verbose_name='周二开业时间')
    Wednesday = models.CharField(max_length=100, verbose_name='周三开业时间')
    Thursday = models.CharField(max_length=100, verbose_name='周开四业时间')
    Friday = models.CharField(max_length=100, verbose_name='周五开业时间')
    Saturday = models.CharField(max_length=100, verbose_name='周六开业时间')
    Sunday = models.CharField(max_length=100, verbose_name='周日开业时间')

    class Meta:
        managed: True
        verbose_name = '开业时间信息表'
        verbose_name_plural = verbose_name


class NewCov(models.Model):
    """新冠情况"""
    id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=100, verbose_name='城市')
    case_rate = models.CharField(max_length=100, verbose_name='新冠情况')
    cases = models.CharField(max_length=100, verbose_name='现有新冠')
    zipcode = models.CharField(max_length=100, verbose_name='邮编')

    class Meta:
        managed: True
        verbose_name = '新冠情况'
        verbose_name_plural = verbose_name


class Foods(models.Model):
    """食物信息表"""
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=20, verbose_name='食物编码')
    creator = models.CharField(max_length=100, verbose_name='创作人')
    created_datetime = models.CharField(max_length=100, verbose_name='创作时间')
    product_name = models.CharField(max_length=100, verbose_name='食物名称')
    countries = models.CharField(max_length=100, verbose_name='国家')
    energy_100g = models.IntegerField(max_length=100, verbose_name='100g所含能量', default=0)
    fat_100g = models.FloatField(max_length=100, verbose_name='100g所含脂肪', default=0)

    class Meta:
        managed: True
        verbose_name = '食物信息表'
        verbose_name_plural = verbose_name


class User(models.Model):
    '''用户信息表'''

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32, verbose_name="用户名", unique=True)
    password = models.CharField(max_length=32, verbose_name="密码")

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


class SearchRecords(models.Model):
    '''检索记录表'''

    id = models.AutoField(primary_key=True)
    SearchInfo = models.CharField(max_length=255, verbose_name="检索信息")
    user = models.ForeignKey(to='User', to_field='id', verbose_name="用户", on_delete=models.CASCADE)

    class Meta:
        verbose_name = '检索记录表'
        verbose_name_plural = verbose_name
