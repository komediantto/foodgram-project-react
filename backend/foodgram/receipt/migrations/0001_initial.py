# Generated by Django 4.0.1 on 2022-02-08 15:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранное',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Ингредиент', max_length=20, verbose_name='Название')),
                ('measurement_unit', models.CharField(choices=[('г', 'Грамм'), ('кг', 'Килограмм'), ('cт.л.', 'Столовая ложка'), ('мл', 'Миллилитр'), ('л', 'Литр'), ('шт', 'Штука'), ('ч.л.', 'Чайная ложка'), ('щепотка', 'Щепотка')], default='г', max_length=20, verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='Название рецепта')),
                ('text', models.TextField(help_text='Опишите ваш рецепт', verbose_name='Ваш рецепт')),
                ('image', models.ImageField(help_text='Добавьте изображение', upload_to='receipt/images/', verbose_name='Загрузить фото')),
                ('time', models.PositiveIntegerField(verbose_name='Время приготовления')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(verbose_name='Количество')),
            ],
            options={
                'verbose_name': 'Количество ингредиентов',
                'verbose_name_plural': 'Количество ингредиентов',
                'ordering': ('-ingredient',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='Название')),
                ('color', models.CharField(max_length=20, unique=True, verbose_name='Цвет')),
                ('slug', models.SlugField(unique=True, verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'Тэг',
                'verbose_name_plural': 'Тэги',
            },
        ),
        migrations.CreateModel(
            name='ShoppingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_list', to='receipt.recipe', verbose_name='Рецепты')),
            ],
            options={
                'verbose_name': 'Список покупок',
                'verbose_name_plural': 'Список покупок',
            },
        ),
    ]
