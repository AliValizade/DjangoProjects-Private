
from django.db import migrations, models

def copy_herb_interactions_to_interaction_herb(apps, schema_editor):
    Herb = apps.get_model('cms', 'Herb')
    # اطمینان حاصل کنید که مدل HerbInteraction هنوز حذف نشده است
    HerbInteraction = apps.get_model('cms', 'HerbInteraction')

    for interaction in HerbInteraction.objects.all():
        herb1 = interaction.herb1
        herb2 = interaction.herb2
        herb1.interaction_herb.add(herb2)
        # برای symmetrical=False، نیازی به اضافه کردن herb2 به herb1 نیست

class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0004_agerange_herb_inappropriate_age_ranges'),
    ]

    operations = [
        migrations.AddField(
            model_name='herb',
            name='interaction_herb',
            field=models.ManyToManyField(blank=True, to='cms.herb', verbose_name='تداخل گیاهان'),
        ),
        migrations.RunPython(copy_herb_interactions_to_interaction_herb),
        migrations.DeleteModel(
            name='HerbInteraction',
        ),
    ]
