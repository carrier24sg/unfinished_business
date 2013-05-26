from django import forms
from main.models import Project, MemberApplication

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields  = ['title', 'description', 'requirement', 'category', 'duration_month']

    def save(self, user):
        item = super(ProjectForm, self).save(commit = False)
        item.owner = user
        item.status = 1
        item.save()
        
        return item

class MemberApplicationForm(forms.ModelForm):
    class Meta:
        model = MemberApplication
        fields = ['project']

    def save(self, user):
        sub = super(MemberApplicationForm, self).save(commit = False)
        sub.user = user
        sub.status = 1
        sub.save()
        return sub
        

        
