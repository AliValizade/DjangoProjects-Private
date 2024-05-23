from django.contrib import admin
from .models import AdditionalName, AgeRange, Herb, Disease, Suitability, Post, Comment, Vote, SeasonalScore, JobScore, JobPollutionLevelScore


class SuitabilityInline(admin.TabularInline):
    model = Suitability
    fields = ['disease', 'alert_states', 'score']
    can_delete = True
    search_fields = ("disease",)
    # raw_id_fields = ('disease',) 
    extra = 1 


class SeasonalScoreInline(admin.TabularInline):
    model = SeasonalScore
    extra = 2

class JobScoreInline(admin.TabularInline):
    model = JobScore
    extra = 1


class JobPollutionLevelScoreInline(admin.TabularInline):
    model = JobPollutionLevelScore
    extra = 1


@admin.register(Herb)
class HerbAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'herb_flavor', 'temperament', 'get_inappropriate_age_ranges', 'get_interaction_herbs', )
    inlines = [SuitabilityInline, SeasonalScoreInline, JobScoreInline, JobPollutionLevelScoreInline]  
    
    def get_inappropriate_age_ranges(self, obj):
        return ", ".join([str(range) for range in obj.inappropriate_age_ranges.all()])

    def get_interaction_herbs(self, obj):
        return ", ".join([herb.name for herb in obj.interaction_herb.all()])

    get_inappropriate_age_ranges.short_description = 'بازه‌های سنی نامناسب'
    get_interaction_herbs.short_description = 'تداخل گیاهان'



class AdditionalNameInline(admin.TabularInline):
    model = AdditionalName
    extra = 2


@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    inlines = [AdditionalNameInline]  


@admin.register(AgeRange)
class AgeRangeAdmin(admin.ModelAdmin):
    list_display = ['id', 'min_age', 'max_age', ]

@admin.register(Suitability)
class SuitabilityAdmin(admin.ModelAdmin):
    list_display = ['id', 'herb', 'disease', 'score', 'alert_states', ]

@admin.register(SeasonalScore)
class SeasonalScoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'herb', 'season', 'score', ]







admin.site.register(Post)
admin.site.register(Vote)
admin.site.register(Comment)