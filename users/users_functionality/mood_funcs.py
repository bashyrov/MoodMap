from django.shortcuts import get_object_or_404, render, redirect
from users.models import Message, DiaryEntry
from users.forms import MessageForm, DiaryEntryForm, UserLoginForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from datetime import datetime
from .openai_bot import get_openai_response


@login_required
def chat_view(request):
    messages = Message.objects.all().order_by('-timestamp')

    if request.method == 'POST':
        if 'clear' in request.POST:
            Message.objects.all().delete()
            return redirect('users:chat')

        form = MessageForm(request.POST)

        if form.is_valid():
            user_message = form.cleaned_data['content']
            message = form.save(commit=False)
            message.user = request.user
            message.save()

            try:
                moodmap_user = get_user_model().objects.get(email="MoodMap@gmail.com")
            except get_user_model().DoesNotExist:
                moodmap_user = get_user_model().objects.create_user(email="MoodMap@gmail.com", password="moodmappassword")
            message_moodmap = Message(user=moodmap_user, content=get_openai_response("chat", user_message))
            message_moodmap.save()

            return redirect('users:chat')
    else:
        form = MessageForm()

    return render(request, 'users/chat.html', {'messages': messages, 'form': form})


@login_required
def diary_view(request):
    current_year = datetime.now().year
    current_month = datetime.now().month

    selected_year = request.GET.get('year', current_year)
    selected_month = request.GET.get('month', 'all')

    diary_entries = DiaryEntry.objects.filter(user=request.user).order_by('-id')
    diary_entries = diary_entries.filter(date__year=selected_year)

    if selected_month != 'all':
        diary_entries = diary_entries.filter(date__month=selected_month)

    if request.method == 'POST':
        if 'delete_entry' in request.POST:
            entry_id = request.POST.get('entry_id')
            entry = get_object_or_404(DiaryEntry, id=entry_id, user=request.user)
            entry.delete()
            return redirect('users:diary')

        form = DiaryEntryForm(request.POST)
        if form.is_valid():
            diary_entry = form.save(commit=False)
            diary_entry.user = request.user
            diary_entry.recommendation = get_openai_response("dairy", diary_entry.content)
            diary_entry.save()
            return redirect('users:diary')
    else:
        form = DiaryEntryForm()

    return render(request, 'users/diary.html', {
        'diary_entries': diary_entries,
        'form': form,
        'selected_year': selected_year,
        'selected_month': selected_month,
        'current_year': current_year,
    })