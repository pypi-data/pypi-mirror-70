# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-14 08:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bpp', '0082_konferencja_opcjonalne'),
    ]

    operations = [
        migrations.AddField(
            model_name='patent_autor',
            name='afiliuje',
            field=models.BooleanField(default=True, help_text='Afiliuje \n    się do jednostki podanej w przypisaniu'),
        ),
        migrations.AddField(
            model_name='wydawnictwo_ciagle_autor',
            name='afiliuje',
            field=models.BooleanField(default=True, help_text='Afiliuje \n    się do jednostki podanej w przypisaniu'),
        ),
        migrations.AddField(
            model_name='wydawnictwo_zwarte_autor',
            name='afiliuje',
            field=models.BooleanField(default=True, help_text='Afiliuje \n    się do jednostki podanej w przypisaniu'),
        ),
        migrations.AlterField(
            model_name='patent_autor',
            name='zatrudniony',
            field=models.BooleanField(default=False, help_text='Pracownik \n    jednostki podanej w przypisaniu'),
        ),
        migrations.AlterField(
            model_name='wydawnictwo_ciagle_autor',
            name='zatrudniony',
            field=models.BooleanField(default=False, help_text='Pracownik \n    jednostki podanej w przypisaniu'),
        ),
        migrations.AlterField(
            model_name='wydawnictwo_zwarte_autor',
            name='zatrudniony',
            field=models.BooleanField(default=False, help_text='Pracownik \n    jednostki podanej w przypisaniu'),
        ),
    ]
