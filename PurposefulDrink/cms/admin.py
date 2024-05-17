from django.contrib import admin
from django import forms

from . import models


class SuitabilityInline(admin.TabularInline):
    model = models.Suitability
    fields = ['disease', 'negative_effects', 'score']
    extra = 1 
    

class SeasonalScoreInline(admin.TabularInline):
    model = models.SeasonalScore
    extra = 2


@admin.register(models.Herb)
class HerbAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'herb_flavor', 'temperament', 'get_inappropriate_age_ranges', 'get_interaction_herbs', )
    fields = ['name', 'temperament', 'herb_flavor', 'inappropriate_age_ranges', 'interaction_herb']
    inlines = [SuitabilityInline, SeasonalScoreInline]  

    def get_inappropriate_age_ranges(self, obj):
        return ", ".join([str(range) for range in obj.inappropriate_age_ranges.all()])
    
    def get_interaction_herbs(self, obj):
        return ", ".join([herb.name for herb in obj.interaction_herb.all()])
    
    get_inappropriate_age_ranges.short_description = 'بازه‌های سنی نامناسب'
    get_interaction_herbs.short_description = 'تداخل گیاهان'


class DiseaseAdminForm(forms.ModelForm):
    class Meta:
        model = models.Disease
        fields = '__all__'
        widgets = {
            'similar_names': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        }

@admin.register(models.Disease)
class DiseaseAdmin(admin.ModelAdmin):
    form = DiseaseAdminForm
    list_display = ['id', 'name', 'similar_names', ]


@admin.register(models.AgeRange)
class AgeRangeAdmin(admin.ModelAdmin):
    list_display = ['id', 'min_age', 'max_age', ]


@admin.register(models.SeasonalScore)
class SeasonalScoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'herb', 'season', 'score', ]


@admin.register(models.Suitability)
class SuitabilityAdmin(admin.ModelAdmin):
    list_display = ['id', 'herb', 'disease', 'score', 'alert_states', ]


@admin.register(models.NeutralPackage)
class NeutralAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]
