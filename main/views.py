from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.views.generic import DetailView
from django.forms.models import modelformset_factory
from django.forms.models import inlineformset_factory
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse


from main.forms import ProjectForm, MemberApplicationForm
from main.models import Project, ProjectImage



def homepage(request):
    return render_to_response('index.html',
            context_instance = RequestContext(request))

def user_panel(request):
    user = request.user
    observed_proj = []
    started_proj = user.userprofile.get_started_projects()
    involved_proj = user.userprofile.get_involved_projects()

    return render_to_response('user/user_home.html', 
            {'started_projects': started_proj,
                'involved_projects': involved_proj,
                'observe_projects': observed_proj,
            },
            context_instance = RequestContext(request))


#class ProjectDetailView(DetailView):
#    context_object_name = 'project'
#    model = Project


def create_new_project(request):
    PicsFormset  = inlineformset_factory(Project, ProjectImage, can_delete=False)
    if request.method == 'GET':
        form = ProjectForm() 
        formset = PicsFormset(instance = Project())  
        return render_to_response('project/create_project.html',
                {'form': form, 'formset': formset},
                context_instance = RequestContext(request))
    
    else:
        form = ProjectForm(request.POST)
        if form.is_valid():
            project_instance = form.save(request.user)
            formset = PicsFormset(request.POST, request.FILES, instance = project_instance)
            if formset.is_valid():
                formset.save()
                return redirect(project_instance)
        else:
            return render_to_response('project/create_project.html',
                {'form': form },
                context_instance = RequestContext(request))

def apply_project(request):
    if request.method == "POST":
        form = MemberApplicationForm(request.POST) 
        if form.is_valid():
            instance = form.save()
            return redirect()

        else:
            pass
    

"""
def add_project_images(request, pid):
    PicsFormset  = inlineformset_factory(Project, ProjectImage)
    project = get_object_or_404(Project, pk = pid)
    
    formset = PicsFormset(instance = project)

    return render_to_response("project/create_project_images.html", {'formset': formset}, context_instance = RequestContext(request))
"""    
    
