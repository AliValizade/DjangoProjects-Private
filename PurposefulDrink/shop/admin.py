from django.contrib import admin


from . import models


class SuitabilityInline(admin.TabularInline):
    model = models.Suitability
    fields = ['disease', 'score']
    extra = 1 


@admin.register(models.Herb)
class HerbAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'temperament', 'suitable_season', ]
    inlines = [SuitabilityInline]  



@admin.register(models.Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]


@admin.register(models.Suitability)
class SuitabilityAdmin(admin.ModelAdmin):
    list_display = ['id', 'herb', 'disease', 'score', ]


@admin.register(models.NeutralPackage)
class NeutralAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]
