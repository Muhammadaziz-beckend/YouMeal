from django.db import models
from django_resized import ResizedImageField

class Date_of_create_update(models.Model):
    date_create = models.DateField('Дата создания',auto_now_add=True)
    date_update = models.DateField('Дата обнавления',auto_now=True)

    class Meta:
        abstract = True

class Product(Date_of_create_update):
    image = ResizedImageField(
        verbose_name='Изображение',
        upload_to='eat/',
        size=[276,220],
        quality=90,
        force_format="WEBP",
    )
    name = models.CharField('Название',max_length=75)
    description = models.CharField(verbose_name='Описание',max_length=150)
    weight = models.PositiveIntegerField('вес в граммах',)
    calories = models.PositiveIntegerField('сколько ккалории')
    price = models.PositiveIntegerField('Цена')
    category = models.ForeignKey('Category',models.CASCADE,'cat',verbose_name='Катигория')
    product_composition = models.ManyToManyField('Product_composition','product_composition',verbose_name='Состав')
    is_publish = models.BooleanField('Продаётся',default=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return  self.name

class Product_composition(Date_of_create_update):
    name = models.CharField('Названия',max_length=65)
    compound = models.ForeignKey('Product',models.CASCADE,'product',)

    class Meta:
        verbose_name = 'Состав продукта'
        verbose_name_plural = 'Составы продуктов'

    def __str__(self):
        return  self.name

class Category(Date_of_create_update):
    icon = ResizedImageField(
        verbose_name='Иконка',
        upload_to='icon/',
        size=[24, 24],
        quality=90,
        force_format="WEBP",
        null=True
    )
    name = models.CharField('Названия',max_length=65)

    class Meta:
        verbose_name = 'Катигория'
        verbose_name_plural = 'Катигории'

    def __str__(self):
        return  self.name
