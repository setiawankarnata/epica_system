from django.urls import path
from . import views
import uuid

app_name = 'pica'

urlpatterns = [
    path('new_meeting/<str:cpy>/', views.NewMeetingView.as_view(), name='new_meeting'),
    path('edit_meeting/<uuid:pk>/', views.edit_meeting, name='edit_meeting'),
    path('delete_meeting/<uuid:pk>/<str:cpy>/', views.delete_meeting, name='delete_meeting'),
    path('meeting_detail/<uuid:pk>/', views.meeting_detail, name='meeting_detail'),
    path('input_internal_participant/<uuid:pk>/', views.input_internal_participant, name="input_internal_participant"),
    path('input_outside_participant/<uuid:pk>/', views.input_outside_participant, name="input_outside_participant"),
    path('add_internal_participant/<uuid:meet_pk>/<int:user_id>/', views.add_internal_participant,
         name='add_internal_participant'),
    path('add_outside_participant/<uuid:meet_pk>/<uuid:user_id>/', views.add_outside_participant,
         name='add_outside_participant'),
    path('new_topic/<uuid:pk>/', views.NewEntryTopicView.as_view(), name='new_topic'),
    path('update_topic/<uuid:tp>/', views.UpdateTopicView.as_view(), name='update_topic'),
    path('delete_topic/<uuid:mt>/<uuid:tp>/<str:fr>/', views.delete_topic, name='delete_topic'),
    path('delete_internal_participant/<uuid:mt>/<int:usr>/', views.delete_internal_participant,
         name='delete_internal_participant'),
    path('delete_outside_participant/<uuid:mt>/<uuid:usr>/', views.delete_outside_participant,
         name='delete_outside_participant'),
    path('input_pic_topic/<uuid:tp>/', views.input_pic_topic, name="input_pic_topic"),
    path('add_pic_topic/<uuid:meet_pk>/<uuid:tp>/<int:user_id>/', views.add_pic_topic,
         name='add_pic_topic'),
    path('delete_pic_topic/<uuid:meet_pk>/<uuid:tp>/<int:user_id>/', views.delete_pic_topic,
         name='delete_pic_topic'),
    path('user_activity/<int:pk>/', views.user_activity, name='user_activity'),
    path('input_user_activity/<uuid:tp>/<int:user_id>/', views.InputUserActivityView.as_view(),
         name='input_user_activity'),
    path('update_user_activity/<uuid:act>/<int:user_id>/', views.update_user_activity, name='update_user_activity'),
    path('details_user_activity/<uuid:act>/<int:user_id>/', views.details_user_activity, name='details_user_activity'),
    # Path for Search Pica
    path('search/', views.search_topic, name='search_topic'),
    # Path for Notify Topic
    path('notify/', views.notify_topic, name='notify_topic'),
    path('notify/all/', views.notify_all, name='notify_all'),
    # Path for Dashboard
    path('dashboard_mom/<str:cpy>/', views.dashboard_mom, name='dashboard_mom'),
    path('dashboard_mom_detail/<uuid:pk>/', views.dashboard_mom_detail, name='dashboard_mom_detail'),
    path('preview_pdf/<uuid:pk>/', views.preview_pdf, name='preview_pdf'),
    path('sending_pdf/<uuid:pk>/', views.sending_pdf, name='sending_pdf'),
    path('dashboard_pica/<str:cpy>/', views.dashboard_pica, name='dashboard_pica'),
    path('dashboard_pica_detail/<uuid:pk>/<str:cpy>/<int:from_to>/', views.dashboard_pica_detail,
         name='dashboard_pica_detail'),
    path('pica_close/<uuid:pk>/<str:cpy>/', views.pica_close, name='pica_close'),
    # Path for Outstanding
    path('outstanding_all_pica', views.outstanding_all_pica, name='outstanding_all_pica'),
    # Path for Register New External Participant
    path('new_external_participant/<uuid:pk>/', views.NewExternalParticipantView.as_view(),
         name='new_external_participant'),
    # Path for input bulk user
    path('input_user/', views.InputBulkUserView.as_view(), name="input_bulk_user"),
]
