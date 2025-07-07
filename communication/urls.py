from django.urls import path
from .views import (
    SendMessageView,
    InboxView,
    SentMessagesView,
    MarkMessageAsReadView,
    compose_message_view
)

urlpatterns = [
    path('send/', SendMessageView.as_view(), name='send-message'),
    path('inbox/', InboxView.as_view(), name='inbox'),
    path('sent/', SentMessagesView.as_view(), name='sent-messages'),
    path('<int:pk>/mark-read/', MarkMessageAsReadView.as_view(), name='mark-message-read'),
    path('compose/', compose_message_view, name='compose-message'),

]