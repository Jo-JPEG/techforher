from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('mentor', 'Mentor'),
        ('mentee', 'Mentee'),
    ]
    LANGUAGE_CHOICES = [
        ('Python', 'Python'),
        ('JavaScript', 'JavaScript'),
        ('Java', 'Java'),
        ('CSS', 'CSS'),
        ('HTML', 'HTML'),
        ('PHP', 'PHP'),
        ('C#', 'C#'),
        ('Other', 'Other'),
    ]
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='mentee'
    )
    preferred_languages = models.ManyToManyField(
        'Language',
        blank=True,
        help_text="Select the languages the user is proficient in."
    )

    # Add related_name to avoid clashes with auth.User
    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="accounts_users_groups", # Unique related_name
        related_query_name="accounts_user",    # Unique related_query_name
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name="accounts_users_permissions", # Unique related_name
        related_query_name="accounts_user",        # Unique related_query_name
    )

    def __str__(self):
        return self.username


class Language(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Mentorship(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]
    LANGUAGE_CHOICES = [
        ('Python', 'Python'),
        ('JavaScript', 'JavaScript'),
        ('Java', 'Java'),
        ('CSS', 'CSS'),
        ('HTML', 'HTML'),
        ('PHP', 'PHP'),
        ('C#', 'C#'),
        ('Other', 'Other'),
    ]
    mentor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='mentorships_as_mentor')
    mentee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='mentorships_as_mentee')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
    preferred_language = models.CharField(
        max_length=20,
        choices=LANGUAGE_CHOICES
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mentorship between {self.mentor} and {self.mentee}"


class ForumPost(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_anonymous = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Reply(models.Model):
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Reply by {self.user} on {self.post}"


class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False, blank=True, null=True)  

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"


class ContactRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'