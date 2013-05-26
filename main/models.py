from django.db import models
#from django.contrib.auth.models import User
from settings import AUTH_USER_MODEL as User

import uuid

# Create your models here.

status_choice = (
        (1, 'Started'),
        (2, 'Incubating'),
        (3, 'Abandoned'),
        (4, 'In progress'),
        (5, 'Completed'),
)

category = (
    (1, 'Software'),
    (2, 'Hardware'),
    (3, 'Others'),
)

roles = (
        (1, 'Contributor'),
        (2, 'Observer'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    description = models.TextField()
    reputation_points = models.IntegerField(default= 0)

    def __unicode__(self):
        return self.user.username

class Project(models.Model):
    status = models.IntegerField(choices = status_choice)
    owner = models.ForeignKey(User)
    start_date  = models.DateField(auto_now_add = True)
    duration_month = models.IntegerField()

    title = models.CharField(max_length=450)
    description = models.TextField()
    requirement = models.TextField() 

    category = models.IntegerField(choices = category) 
    members = models.ManyToManyField(User, through = "ProjectMember")

    def __unicode__(self):
        return self.title

class UserReview(models.Model):
    rating = models.BooleanField()
    comments = models.TextField(null = True, blank = True)  
    project  = models.ForeignKey(Project)
    user = models.ForeignKey(User)
    date = models.DateField(auto_add_now = True)


def generate_fn(instance, filename):
    uuid_str = str(uuid.uuid4()).replace("-", "")
    return uuid_str

class MemberApplication(models.Model):
    status_choice = ( (1, 'Pending'), (2, 'Rejected'), (3, 'approved'), )
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    date_submitted = models.DateField(auto_add_now = True)
    status = models.IntegerField(choices = status_choice)

    def approve_application(self):
        self.status = 3
        self.save()

        new_member = ProjectMember(project = self.project, member = self.user, role = 1)
        new_member.save()

    def reject_application(self):
        self.status = 2
        self.save()
    

class ProjectMember(models.Model):
    project = models.ForeignKey(Project)
    member = models.ForeignKey(User)
    join_date = models.DateField(auto_add_now = True)
    role = models.IntegerField(choice =  roles)

class ProjectUpdate(models.Model):
    project = models.ForeignKey(Project)
    update = models.TextField()
    
class ProjectUpdateImage(models.Model):
    update = models.ForeignKey(ProjectUpdate)
    caption = models.CharField(max_length = 150, null = True, blank = True )
    image = models.ImageField(upload_to = generate_fn)

class ProjectImage(models.Model):
    update = models.ForeignKey(Project)
    image = models.ImageField(upload_to= generate_fn)


    
