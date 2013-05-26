from django import forms
from main.model import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields  = ['title', 'description', 'requirement', 'category']

    def save(self, user):
        item = super(ProjectForm, self).save(commit = False)
        item.owner = user
        
