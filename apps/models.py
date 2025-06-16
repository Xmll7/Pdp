from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
import uuid


class User(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]

    fullname = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=128)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    group = models.ForeignKey('Group', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)

    def __str__(self):
        return f"{self.fullname} ({self.username})"

    class Meta:
        ordering = ['fullname']


class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    token = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    device_name = models.CharField(max_length=100, blank=True)
    ip_address = models.GenericIPAddressField()
    last_login = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.user.username} - {self.device_name}"

    class Meta:
        ordering = ['-last_login']


class Group(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                limit_choices_to={'role': 'teacher'}, related_name='teaching_groups')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def student_count(self):
        return self.user_set.filter(role='student').count()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Homework(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    points = models.PositiveIntegerField()
    start_date = models.DateTimeField()
    deadline = models.DateTimeField()
    line_limit = models.PositiveIntegerField(null=True, blank=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE,
                                limit_choices_to={'role': 'teacher'}, related_name='homeworks')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='homeworks')
    file_extension = models.CharField(max_length=10, default='.py')
    ai_grading_prompt = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.group.name}"

    class Meta:
        ordering = ['-created_at']


class Submission(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE,
                                limit_choices_to={'role': 'student'}, related_name='submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)
    ai_grade = models.FloatField(null=True, blank=True)
    final_grade = models.FloatField(null=True, blank=True)
    ai_feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.fullname} - {self.homework.title}"

    class Meta:
        unique_together = ['homework', 'student']
        ordering = ['-submitted_at']


class SubmissionFile(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='files')
    file_name = models.CharField(max_length=255)
    content = models.TextField()
    line_count = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if self.content:
            self.line_count = len(self.content.split('\n'))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.file_name} - {self.submission}"

    class Meta:
        ordering = ['file_name']


class Grade(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='grade')
    ai_task_completeness = models.FloatField(null=True, blank=True)
    ai_code_quality = models.FloatField(null=True, blank=True)
    ai_correctness = models.FloatField(null=True, blank=True)
    ai_total = models.FloatField(null=True, blank=True)
    final_task_completeness = models.FloatField(null=True, blank=True)
    final_code_quality = models.FloatField(null=True, blank=True)
    final_correctness = models.FloatField(null=True, blank=True)
    teacher_total = models.FloatField(null=True, blank=True)
    ai_feedback = models.TextField(blank=True)
    task_completeness_feedback = models.TextField(blank=True)
    code_quality_feedback = models.TextField(blank=True)
    correctness_feedback = models.TextField(blank=True)
    modified_by_teacher = models.BooleanField(default=False)

    def __str__(self):
        return f"Grade for {self.submission}"

