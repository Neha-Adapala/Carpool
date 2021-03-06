# Generated by Django 4.0.6 on 2022-07-12 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carpool_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='make_year',
            field=models.IntegerField(choices=[(2011, '2011'), (2012, '2012'), (2013, '2013'), (2014, '2014'), (2015, '2015'), (2016, '2016'), (2017, '2017'), (2018, '2018'), (2019, '2019'), (2020, '2020'), (2021, '2021'), (2022, '2022')]),
        ),
        migrations.AlterField(
            model_name='car',
            name='max_passengers',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6')]),
        ),
    ]
