from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import AdditionalName, AgeRange, Herb, Disease, Suitability, SeasonalScore, JobScore, JobPollutionLevelScore
from .forms import HerbForm


class SuitabilityInline(admin.TabularInline):
    model = Suitability
    fields = ['disease', 'alert_states', 'score']
    can_delete = True
    search_fields = ("disease",)
    # raw_id_fields = ('disease',) 
    extra = 1 
    # min_num = 1
    # validate_min = True    


class SeasonalScoreInline(admin.TabularInline):
    model = SeasonalScore
    extra = 0
    # min_num = 1
    # validate_min = True

class JobScoreInline(admin.TabularInline):
    model = JobScore
    extra = 0
    # min_num = 1
    # validate_min = True


class JobPollutionLevelScoreInline(admin.TabularInline):
    model = JobPollutionLevelScore
    extra = 0
    # min_num = 1
    # validate_min = True


@admin.register(Herb)
class HerbAdmin(admin.ModelAdmin):
    form = HerbForm  # معرفی فرم سفارشی
    list_display = ('id', 'name', 'herb_flavor', 'temperament', 'get_inappropriate_age_ranges', 'get_interaction_herbs', )
    inlines = [SuitabilityInline, SeasonalScoreInline, JobScoreInline, JobPollutionLevelScoreInline]  

    # def save_model(self, request, obj, form, change):
    #     if not obj.pk:
    #         super().save_model(request, obj, form, change)
    #     if not obj.suitability_herb.exists():
    #         form.add_error(None, ValidationError('حداقل یک سطر برای "Suitability" باید وارد شود.'))
    #     if not obj.seasonal_scores.exists():
    #         form.add_error(None, ValidationError('حداقل یک سطر برای "SeasonalScore" باید وارد شود.'))
    #     if not obj.job_scores.exists():
    #         form.add_error(None, ValidationError('حداقل یک سطر برای "JobScore" باید وارد شود.'))
    #     if not obj.pollution_scores.exists():
    #         form.add_error(None, ValidationError('حداقل یک سطر برای "JobPollutionLevelScore" باید وارد شود.'))
   
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







# admin.site.register(Post)
# admin.site.register(Vote)
# admin.site.register(Comment)