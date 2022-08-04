from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.http import Http404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm



# Create your views here.
def index(request):
    """Home page fpr my web app"""
    return render(request, 'WebLog/index.html')

@login_required
def topics(request):
    """Show all topics"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'WebLog/topics.html',context)

@login_required
def topic(request, topic_id):
    """Show a topic"""
    topic = get_object_or_404(Topic,id=topic_id)
    # Make sure topic belongs to current user
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries':entries}
    return render(request, 'WebLog/topic.html',context)

@login_required
def new_topic(request):
    """Create a new topic"""
    if request.method != 'POST':
        #No data submitted create empty form
        form = TopicForm()
    else:
        # POST data submitted process data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('WebLog:topics')

    # Display a blank or invalid form
    context = {'form': form}
    return render(request,'WebLog/new_topic.html',context)

@login_required
def new_entry(request,topic_id):
    """Create a new entry for specific topic"""
    topic = Topic.objects.get(id=topic_id)
   
    if request.method != 'POST':
        #No data submitted create empty form
        form = EntryForm()
    else:
        # POST data submitted process data
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('WebLog:topic',topic_id=topic_id)

    # Display a blank or invalid form
    context = {'topic':topic, 'form': form}
    return render(request,'WebLog/new_entry.html',context)

@login_required
def edit_entry(request,entry_id):
    """edit an entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    """Ensure entry belong to current user"""
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        #First request, prefill form with current entry
        form = EntryForm(instance=entry)
    else:
        # POST data submitted process data
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('WebLog:topic',topic_id=topic.id)

    # Display a blank or invalid form
    context = {'entry':entry, 'topic':topic, 'form': form}
    return render(request,'WebLog/edit_entry.html',context)