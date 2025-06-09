from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from .models import *
from .forms import ChatMessageCreateForm


@login_required
def chat_view(request, chatroom_name='public-chat'):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    chat_messages = chat_group.chat_messages.all()[:200]
    form = ChatMessageCreateForm()

    other_user = None
    members = chat_group.members.all()
    if chat_group.is_private:
        if request.user not in members:
            raise Http404()
        for member in members:
            if member != request.user:
                other_user = member
                break

    if request.htmx:
        form = ChatMessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            context = {
                'message': message,
                'user': request.user,
            }
            return render(request, 'a_rtchat/partials/chat_message_p.html', context)

    context = {
        'chat_messages': chat_messages,
        'form': form,
        'other_user': other_user,
        'chatroom_name': chatroom_name,
    }

    return render(request, 'a_rtchat/chat.html', context)


@login_required
def get_or_create_chatroom(request, username):
    if request.user.username == username:
        # Если ты пытаешься открыть чат сам с собой — происходит редирект на главную
        return redirect('home')

    # Находит объект пользователя в базе по переданному имени. Это будет собеседник.
    other_user = User.objects.get(username=username)

    # Находит все приватные чаты, в которых состоит текущий пользователь.
    my_chatrooms = request.user.chat_groups.filter(is_private=True)

    if my_chatrooms.exists():
        for chatroom in my_chatrooms:
            if other_user in chatroom.members.all():
                # Если в комнате уже есть other_user — значит, приватный чат с этим человеком уже создан.
                chatroom = chatroom
                break
            else:
                chatroom = ChatGroup.objects.create(is_private=True)
                chatroom.members.add(other_user, request.user)
    else:
        chatroom = ChatGroup.objects.create(is_private=True)
        chatroom.members.add(other_user, request.user)

    return redirect('chatroom', chatroom.group_name)
