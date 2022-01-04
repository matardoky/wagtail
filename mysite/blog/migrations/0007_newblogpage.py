# Generated by Django 3.2.10 on 2022-01-04 10:14

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0066_collection_management_permissions'),
        ('blog', '0006_auto_20220101_1934'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewBlogPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('author', models.CharField(max_length=255)),
                ('date', models.DateField(verbose_name='Post date')),
                ('body', wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.CharBlock(form_classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())])),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
