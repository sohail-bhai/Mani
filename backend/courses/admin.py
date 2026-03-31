from django.contrib import admin
from .models import *


class CourseTopicInline(admin.TabularInline):
    model = Course_unit_topic
    extra = 0
class CourseUnitInline(admin.TabularInline):
    model = Course_Unit
    extra = 0
    inlines = [CourseTopicInline]
    
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'course_title', 'credits')
    search_fields = ('course_code', 'course_title')
    inlines = [CourseUnitInline]


@admin.register(Course_Objective)
class CourseObjectiveAdmin(admin.ModelAdmin):
    list_display = ('course', 'order', 'text')
    search_fields = ('course__course_code', 'course__course_title', 'text')

@admin.register(Course_Unit)
class CourseUnitAdmin(admin.ModelAdmin):
    list_display = ('course', 'unit_number', 'unit_title', 'unit_hours')
    search_fields = ('course__course_code', 'course__course_title', 'unit_title')

@admin.register(Course_unit_topic)
class CourseUnitTopicAdmin(admin.ModelAdmin):   
    list_display = ('unit', 'order', 'topic')
    search_fields = ('unit__course__course_code', 'unit__course__course_title', 'unit__unit_title', 'topic')    

@admin.register(practical)
class PracticalAdmin(admin.ModelAdmin):
    list_display = ('Course', 'order', 'exercise_number', 'title')
    search_fields = ('Course__course_code', 'Course__course_title', 'exercise_number', 'title')

class CourseSubcategoryInline(admin.TabularInline):
    model = Course_subcategory
    extra = 0
@admin.register(Course_category)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('short_code', 'name', 'priority')
    search_fields = ('name','short_code','priority')
    inlines = [CourseSubcategoryInline]

@admin.register(Course_subcategory)
class CourseSubcategoryAdmin(admin.ModelAdmin):
    list_display = ('short_code', 'name', 'category')
    search_fields = ('name','short_code')

@admin.register(Course_Type)
class CourseTypeAdmin(admin.ModelAdmin):
    list_display = ('short_code', 'name')
    search_fields = ('name','short_code')
    
