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
    list_display = ('id', 'name', 'temperament')
    fields = ('name', 'temperament')
    inlines = [SuitabilityInline, SeasonalScoreInline]  


@admin.register(models.Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]


@admin.register(models.HerbInteraction)
class HerbInteractionAdmin(admin.ModelAdmin):
    list_display = ['id', 'herb1', 'herb2', 'description', ]


@admin.register(models.SeasonalScore)
class SeasonalScoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'herb', 'season', 'score', ]


@admin.register(models.Suitability)
class SuitabilityAdmin(admin.ModelAdmin):
    list_display = ['id', 'herb', 'disease', 'score', ]


@admin.register(models.NeutralPackage)
class NeutralAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]
