from modeltranslation.translator import TranslationOptions, register
from .models import Skill, Category, Project, Offer, UserProfile


@register(Skill)
class SkillTranslationOptions(TranslationOptions):
    fields = ('skill_name',)

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)

@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(Offer)
class OfferTranslationOptions(TranslationOptions):
    fields = ('message',)