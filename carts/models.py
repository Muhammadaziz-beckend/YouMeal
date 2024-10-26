from django.db import models

from main.models import Product
from account.models import User

class Cart(models.Model):

    product = models.ForeignKey('main.Product',models.CASCADE,'cart',verbose_name='Продукт')
    user = models.ForeignKey(User,models.CASCADE,'cart',verbose_name='Пользователь')
    count_product = models.PositiveIntegerField('Количество продуктов',default=1,)
    final_tootle_prise = models.DecimalField('Общяя сумма',max_digits=10, decimal_places=2,default=0.0)

    def save(self, *args, **kwargs):

        if self.product and self.product.price:
            self.final_total_price = self.product.price * self.count_product
        else:
            self.final_total_price = 0

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Карзинка'
        verbose_name_plural = 'Карзинки'
        db_table_comment = 'Карзина'

    def __str__(self):

        return  self.user.get_full_name