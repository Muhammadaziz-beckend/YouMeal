from random import randint, choice
from django.db import transaction
from main.models import Product, Category, Product_composition


def clone(id_product, count):
    try:
        chooses = list(Category.objects.all())
        product_compositions = list(Product_composition.objects.all())

        with transaction.atomic():
            cloned_products = []
            for _ in range(count):
                # Получаем оригинальный продукт
                cloned_product: Product = Product.objects.get(pk=id_product)

                # Обнуляем первичный ключ, чтобы создать новый объект
                cloned_product.pk = None

                # Присваиваем случайную категорию
                cloned_product.category = choice(chooses)

                cloned_product.price = randint(100, 1000)
                # Сохраняем продукт перед добавлением ManyToMany полей
                cloned_product.save()

                # Для ManyToManyField используем метод .set()
                chosen_composition = [choice(product_compositions)]
                cloned_product.product_composition.set(chosen_composition)

                # Изменяем цену и сохраняем продукт

                cloned_product.save()

                # Добавляем клонированный продукт в список
                cloned_products.append(cloned_product)

            return cloned_products
    except Product.DoesNotExist:
        print("Продукт с указанным ID не найден.")
        return None
