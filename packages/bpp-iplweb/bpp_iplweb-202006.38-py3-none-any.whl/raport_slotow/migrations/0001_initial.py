# Generated by Django 2.2.8 on 2020-02-13 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("bpp", "0194_auto_20200213_2148"),
    ]

    operations = [
        migrations.CreateModel(
            name="RaportZerowyEntry",
            fields=[
                (
                    "autor",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        primary_key=True,
                        serialize=False,
                        to="bpp.Autor",
                    ),
                ),
                ("rok", models.IntegerField()),
            ],
            options={"ordering": ("autor", "rok"), "managed": False,},
        ),
    ]
