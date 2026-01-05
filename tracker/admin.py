from django.contrib import admin
from .models import (
    VisibilityProject, Brand, Competitor, AIModel, Prompt,
    ModelSelection, PromptResponse, BrandMention, SentimentScore,
    VisibilityScore, DetailedReport, ExecutionLog
)


@admin.register(VisibilityProject)
class VisibilityProjectAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'user', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['company_name', 'area_of_work']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'project']


@admin.register(Competitor)
class CompetitorAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'is_ai_suggested', 'is_validated']
    list_filter = ['is_ai_suggested', 'is_validated']


@admin.register(AIModel)
class AIModelAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'name', 'weight', 'is_active']
    list_filter = ['is_active']


@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ['text', 'project', 'is_ai_generated', 'is_selected']
    list_filter = ['is_ai_generated', 'is_selected']
    search_fields = ['text']


@admin.register(PromptResponse)
class PromptResponseAdmin(admin.ModelAdmin):
    list_display = ['prompt', 'model', 'status', 'created_at']
    list_filter = ['status', 'model']


@admin.register(BrandMention)
class BrandMentionAdmin(admin.ModelAdmin):
    list_display = ['brand_name', 'position', 'is_main_brand', 'response']
    list_filter = ['is_main_brand']


@admin.register(SentimentScore)
class SentimentScoreAdmin(admin.ModelAdmin):
    list_display = ['mention', 'sentiment', 'confidence']
    list_filter = ['sentiment']


@admin.register(VisibilityScore)
class VisibilityScoreAdmin(admin.ModelAdmin):
    list_display = ['brand_name', 'project', 'normalized_score', 'total_mentions']
    list_filter = ['is_main_brand']
    ordering = ['-normalized_score']


@admin.register(DetailedReport)
class DetailedReportAdmin(admin.ModelAdmin):
    list_display = ['project', 'created_at']


@admin.register(ExecutionLog)
class ExecutionLogAdmin(admin.ModelAdmin):
    list_display = ['project', 'level', 'module', 'message', 'timestamp']
    list_filter = ['level', 'module']
    search_fields = ['message']
