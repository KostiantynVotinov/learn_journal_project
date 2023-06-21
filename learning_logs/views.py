from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry

from .forms import TopicForm, EntryForm


def index(request):
    """ГОЛОВНА СТОРІНКА learning_log."""
    return render(request, "learning_logs/index.html")

@login_required
def topics(request):
    """Відображає всі теми."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """Показати одну тему та всі записи до неї."""
    topic = get_object_or_404(Topic, id=topic_id)
    # Пересвідчетися, що тема належить поточному користувачеві.
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """Додати нову тему."""
    if request.method != 'POST':
        # No data sent. Create an empty form.
        form = TopicForm()
    else:
        # Send POST. Process the data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    # Показати порожню або невірну форму.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Додайте новий запис для певної теми."""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        # Жодних даних не надіслано; створити порожню форму.
        form = EntryForm()
    else:
        # Отримані дані у POST-запиті; обробити дані.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    # Показати породжню або недійсну форму.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Редагування існуючого запису."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Первинний запит; попередньо заповнена форма з поточним записом.
        form = EntryForm(instance=entry)
    else:
        # Надіслані POST-дані; оброблені дані.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'form': form, 'topic': topic}
    return render(request, 'learning_logs/edit_entry.html', context)
