from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=255)

    def str(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='groups')

    def str(self):
        return self.name


class Badge(models.Model):
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)  # Или models.ImageField если иконка — файл

    def str(self):
        return self.name


class User(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )

    fullname = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, related_name='users')
    level = models.IntegerField()
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)


class Assignment(models.Model):
    ASSIGNMENT_TYPE_CHOICES = (
        ('quiz', 'Quiz'),
        ('code', 'Code'),
        ('essay', 'Essay'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    difficulty = models.IntegerField()
    deadline = models.DateTimeField()
    assignment_type = models.CharField(max_length=20, choices=ASSIGNMENT_TYPE_CHOICES)


class Submission(models.Model):
    SUBMISSION_TYPE_CHOICES = (
        ('file', 'File'),
        ('link', 'Link'),
    )

    STATUS_CHOICES = (
        ('submitted', 'Submitted'),
        ('reviewed', 'Reviewed'),
        ('rejected', 'Rejected'),
    )

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    submission_type = models.CharField(max_length=20, choices=SUBMISSION_TYPE_CHOICES)
    github_link = models.URLField(null=True, blank=True)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
    detailed_review = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SubmissionFile(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='files')
    url = models.URLField()
    name = models.CharField(max_length=255)
    size = models.BigIntegerField()