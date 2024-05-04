from django.contrib import admin

from . import models


class SuitabilityInline(admin.TabularInline):
    model = models.Suitability
    fields = ['disease', 'negative_effects', 'score']
    extra = 1 
    

class SeasonalScoreInline(admin.TabularInline):
    model = models.SeasonalScore
    extra = 4


@admin.register(models.Herb)
class HerbAdmin(admin.ModelAdmin):
    list_display = ('name', 'temperament')
    fields = ('name', 'temperament')
    inlines = [SuitabilityInline, SeasonalScoreInline]  


@admin.register(models.Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]


@admin.register(models.SeasonalScore)
class SeasonalScoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'herb', 'season', 'score', ]


@admin.register(models.Suitability)
class SuitabilityAdmin(admin.ModelAdmin):
    list_display = ['id', 'herb', 'disease', 'score', ]


@admin.register(models.NeutralPackage)
class NeutralAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]
