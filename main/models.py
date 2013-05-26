from django.db import models
from django.conf import settings 
from django.core.urlresolvers import reverse

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
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    description = models.TextField()
    reputation_points = models.IntegerField(default= 0)

    def __unicode__(self):
        return self.user.username
    
    def get_started_projects(self):
        projects = Project.objects.filter(owner = self.user)
        return projects
    def get_involved_projects(self):
        projects = Project.objects.filter(projectmember = self.user)
        return projects
    
class Project(models.Model):
    status = models.IntegerField(choices = status_choice)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'owner')
    start_date  = models.DateField(auto_now_add = True)
    duration_month = models.IntegerField()

    title = models.CharField(max_length=450)
    description = models.TextField()
    requirement = models.TextField() 

    category = models.IntegerField(choices = category) 
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through = "ProjectMember")

    def get_application(self):
        return self.memberapplication_set

    def get_absolute_url(self):
        return '/project/%i/' %self.pk

    def __unicode__(self):
        return self.title

class UserReview(models.Model):
    rating = models.BooleanField()
    comments = models.TextField(null = True, blank = True)  
    project  = models.ForeignKey(Project)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    date = models.DateField(auto_now_add = True)


def generate_fn(instance, filename):
    uuid_str = str(uuid.uuid4()).replace("-", "")
    return uuid_str

class MemberApplication(models.Model):
    status_choice = ( (1, 'Pending'), (2, 'Rejected'), (3, 'approved'), )
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    project = models.ForeignKey(Project)
    date_submitted = models.DateField(auto_now_add = True)
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
    member = models.ForeignKey(settings.AUTH_USER_MODEL)
    join_date = models.DateField(auto_now_add = True)
    role = models.IntegerField(choices =  roles)

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


    
