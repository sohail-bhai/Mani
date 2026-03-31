from django.db import models

# Create your models here.
class Course(models.Model):
    course_code=models.CharField(max_length=20, unique=True)
    course_title=models.CharField(max_length=255)
    lecture_hours       = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    tutorial_hours      = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    practical_hours     = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    self_study_hours    = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    independent_hours   = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    
    @property
    def credits(self):
        return (
            self.lecture_hours*1
            + self.tutorial_hours*1
            + self.practical_hours*0.5
            + self.self_study_hours*0.5
        )
        
        # change the formula for calculating credits as per our requirements. 

    pre_requisite       = models.CharField(max_length=300, blank=True)
    co_requisite        = models.CharField(max_length=300, blank=True)
    course_description  = models.TextField(blank=True)
    
class Course_Objective(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='objectives')
    order   = models.PositiveIntegerField(default=0)
    text    = models.TextField()
    class Meta:
        ordering = ['order']
    def __str__(self):
        return f"Objective {self.order} : {self.text[:60]}..."

class Course_Unit(models.Model):
    course=models.ForeignKey(Course, on_delete=models.CASCADE, related_name='units')
    unit_number=models.PositiveIntegerField()
    unit_title=models.CharField(max_length=255)
    unit_hours=models.DecimalField(max_digits=5, decimal_places=1, default=0)
    def __str__(self):
        return f"Unit {self.unit_number} : {self.unit_title[:60]}..."
    class Meta:
        ordering = ['unit_number']
        unique_together = ('course', 'unit_number')

class Course_unit_topic(models.Model):
    unit=models.ForeignKey(Course_Unit, on_delete=models.CASCADE, related_name='topics')
    order=models.PositiveIntegerField()
    topic=models.CharField(max_length=255)
    class Meta:
        ordering = ['order']
        unique_together = ('unit', 'order')

class practical(models.Model):
    Course=models.ForeignKey(Course, on_delete=models.CASCADE, related_name='practicals')
    order=models.PositiveIntegerField()
    exercise_number=models.CharField(max_length=20)
    title=models.CharField(max_length=255)
    class Meta:
        ordering = ['order']
        unique_together = ('Course', 'order')
    def __str__(self):
        return f"Practical {self.exercise_number} : {self.title[:60]}..."

class Textbook(models.Model):
    course=models.ForeignKey(Course, on_delete=models.CASCADE, related_name='textbooks')
    order=models.PositiveIntegerField()
    author=models.CharField(max_length=255)
    title=models.CharField(max_length=255)
    publisher=models.CharField(max_length=255)
    year_of_publication=models.PositiveIntegerField()
    class Meta:
        ordering = ['order']
        unique_together = ('course', 'order')
    def __str__(self):
        return f"Textbook {self.author} , {self.title[:60]}... , {self.publisher} , {self.year_of_publication}."

class ReferenceBook(models.Model):
    course=models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reference_books')
    order=models.PositiveIntegerField()
    author=models.CharField(max_length=255)
    title=models.CharField(max_length=255)
    publisher=models.CharField(max_length=255)
    year_of_publication=models.PositiveIntegerField()
    class Meta:
        ordering = ['order']
        unique_together = ('course', 'order')
    def __str__(self):
        return f"Reference Book {self.author} , {self.title[:60]}... , {self.publisher} , {self.year_of_publication}."

class Course_outcome(models.Model):
    Bloom_Levels=[
        ('L1', 'L1 — Remember'),
        ('L2', 'L2 — Understand'),
        ('L3', 'L3 — Apply'),
        ('L4', 'L4 — Analyze'),
        ('L5', 'L5 — Evaluate'),
        ('L6', 'L6 — Create'),       
    ]
    
    course=models.ForeignKey(Course, on_delete=models.CASCADE, related_name='outcomes')
    order=models.PositiveIntegerField()
    text=models.TextField()
    bloom=models.CharField(max_length=2,choices=Bloom_Levels,blank=True,default='')
    class Meta:
        ordering = ['order']
    def __str__(self):
        return f"Course Outcome {self.order} : {self.text[:60]}..."
    
class Articulation(models.Model):
    course=models.ForeignKey(Course, on_delete=models.CASCADE, related_name='articulations')
    co=models.OneToOneField(Course_outcome, on_delete=models.CASCADE, related_name='articulation')
    po1=models.IntegerField(blank=True,null=True)
    po2=models.IntegerField(blank=True,null=True)
    po3=models.IntegerField(blank=True,null=True)
    po4=models.IntegerField(blank=True,null=True)
    po5=models.IntegerField(blank=True,null=True)
    po6=models.IntegerField(blank=True,null=True)
    po7=models.IntegerField(blank=True,null=True)
    po8=models.IntegerField(blank=True,null=True)
    po9=models.IntegerField(blank=True,null=True)
    po10=models.IntegerField(blank=True,null=True)
    po11=models.IntegerField(blank=True,null=True)
    pso1=models.IntegerField(blank=True,null=True)
    pso2=models.IntegerField(blank=True,null=True)
    
    
    po_fields = ['po1', 'po2', 'po3', 'po4', 'po5', 'po6', 'po7', 'po8', 'po9', 'po10', 'po11', 'pso1', 'pso2']
    po_labels = ['PO1', 'PO2', 'PO3', 'PO4', 'PO5', 'PO6', 'PO7', 'PO8', 'PO9', 'PO10', 'PO11', 'PSO1', 'PSO2']
    class Meta:
        ordering = ['order']
    def get_values_dict(self):
        return {label: getattr(self, field) for field, label in zip(self.po_fields, self.po_labels)}
    
class SDGMAPPING(models.Model):
    Course=models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sdg_mappings')
    order=models.PositiveIntegerField()
    sdg_number=models.CharField(max_length=20)
    sdg_theme=models.CharField(max_length=255)
    sdg_title=models.CharField(max_length=255)
    class Meta:
        ordering = ['order']
        unique_together = ('Course', 'order')

class SMEDetails(models.Model):
    course=models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sme_details')
    name=models.CharField(max_length=255)
    designation=models.CharField(max_length=255)
    email=models.EmailField()


class Course_category(models.Model):
    name=models.CharField(max_length=255, unique=True)
    short_code = models.CharField(max_length=20, unique=True, db_index=True, blank=True, null=True)
    priority = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['priority', 'name']
    def __str__(self):
        return f"{self.short_code} - {self.name}"
    
class Course_subcategory(models.Model):
    category=models.ForeignKey(Course_category, on_delete=models.CASCADE, related_name='subcategories')
    name=models.CharField(max_length=255)
    short_code = models.CharField(max_length=20, blank=True, null=True)
    priority = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['priority', 'name']
    def __str__(self):
        return f"{self.short_code} - {self.name}"    
    
class CourseType(models.Model):
    name=models.CharField(max_length=255, unique=True)
    short_code = models.CharField(max_length=20, unique=True, db_index=True, blank=True, null=True)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return f"{self.short_code} - {self.name}"


