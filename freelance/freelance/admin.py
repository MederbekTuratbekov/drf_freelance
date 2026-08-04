from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Skill, UserProfile, SocialLinks, Category, Project, Offer, Review


class SocialLinksInlines(admin.TabularInline):
    model = SocialLinks
    extra = 3

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    inlines = [SocialLinksInlines]
    list_display = ('username', 'role', 'email')
    fields = ('username', 'email', 'password', 'first_name', 'last_name', 'role', 'bio', 'avatar', 'skills')
    filter_horizontal = ('skills',)

@admin.register(Skill, Category, Project, Offer)
class TranslateAdmin(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

admin.site.register(Review)
