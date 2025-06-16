from rest_framework import serializers
from .models import User, Session, Group, Homework, Submission, SubmissionFile, Grade

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    group_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'fullname', 'username', 'password', 'role', 'group', 'group_name', 'created_at']
        extra_kwargs = {'password_hash': {'write_only': True}}

    def get_group_name(self, obj):
        return obj.group.name if obj.group else None

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class TeacherSerializer(serializers.ModelSerializer):
    groups_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'fullname', 'username', 'role', 'groups_count', 'created_at']

    def get_groups_count(self, obj):
        return obj.teaching_groups.count()


class StudentSerializer(serializers.ModelSerializer):
    group_name = serializers.SerializerMethodField()
    total_score = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'fullname', 'username', 'group', 'group_name', 'total_score', 'created_at']

    def get_group_name(self, obj):
        return obj.group.name if obj.group else None

    def get_total_score(self, obj):
        submissions = obj.submissions.all()
        total = sum(s.final_grade or s.ai_grade or 0 for s in submissions)
        return total


class SessionSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = ['id', 'user', 'username', 'token', 'device_name', 'ip_address', 'last_login', 'expires_at']

    def get_username(self, obj):
        return obj.user.username


class GroupSerializer(serializers.ModelSerializer):
    teacher_name = serializers.SerializerMethodField()
    student_count = serializers.ReadOnlyField()

    class Meta:
        model = Group
        fields = ['id', 'name', 'teacher', 'teacher_name', 'student_count', 'created_at']

    def get_teacher_name(self, obj):
        return obj.teacher.fullname if obj.teacher else None


class HomeworkSerializer(serializers.ModelSerializer):
    teacher_name = serializers.SerializerMethodField()
    group_name = serializers.SerializerMethodField()
    submission_count = serializers.SerializerMethodField()

    class Meta:
        model = Homework
        fields = ['id', 'title', 'description', 'points', 'start_date', 'deadline',
                 'line_limit', 'teacher', 'teacher_name', 'group', 'group_name',
                 'file_extension', 'ai_grading_prompt', 'submission_count', 'created_at']

    def get_teacher_name(self, obj):
        return obj.teacher.fullname

    def get_group_name(self, obj):
        return obj.group.name

    def get_submission_count(self, obj):
        return obj.submissions.count()


class SubmissionFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionFile
        fields = ['id', 'file_name', 'content', 'line_count']


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'


class SubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    homework_title = serializers.SerializerMethodField()
    files = SubmissionFileSerializer(many=True, read_only=True)
    grade = GradeSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'homework', 'homework_title', 'student', 'student_name',
                 'submitted_at', 'ai_grade', 'final_grade', 'ai_feedback',
                 'files', 'grade', 'created_at']

    def get_student_name(self, obj):
        return obj.student.fullname

    def get_homework_title(self, obj):
        return obj.homework.title


class LeaderboardSerializer(serializers.ModelSerializer):
    rank = serializers.IntegerField()
    total_score = serializers.FloatField()

    class Meta:
        model = User
        fields = ['id', 'fullname', 'rank', 'total_score']
