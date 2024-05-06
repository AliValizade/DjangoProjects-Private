from django.contrib import admin

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
    list_display = ('id', 'name', 'temperament', 'get_inappropriate_age_ranges', 'get_interaction_herbs', )
    fields = ['name', 'temperament', 'inappropriate_age_ranges', 'interaction_herb']
    inlines = [SuitabilityInline, SeasonalScoreInline]  

    def get_inappropriate_age_ranges(self, obj):
        return ", ".join([str(range) for range in obj.inappropriate_age_ranges.all()])
    
    def get_interaction_herbs(self, obj):
        return ", ".join([herb.name for herb in obj.interaction_herb.all()])
    
    get_inappropriate_age_ranges.short_description = 'بازه‌های سنی نامناسب'
    get_interaction_herbs.short_description = 'تداخل گیاهان'

@admin.register(models.Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]

@admin.register(models.AgeRange)
class AgeRangeAdmin(admin.ModelAdmin):
    list_display = ['id', 'min_age', 'max_age',]

@admin.register(models.SeasonalScore)
class SeasonalScoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'herb', 'season', 'score', ]


@admin.register(models.Suitability)
class SuitabilityAdmin(admin.ModelAdmin):
    list_display = ['id', 'herb', 'disease', 'score', ]


@admin.register(models.NeutralPackage)
class NeutralAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]
