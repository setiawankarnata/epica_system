from django.shortcuts import render
from django.views.generic import View
from .forms import NewMeetingForm, EntryTopicsForm, MultiUploadFileForm, EntryActivityForm, \
    MultiUploadActivityFileForm, TopicActivityForm, UpdateActivityForm, UpdateTopicsForm
from django.shortcuts import get_object_or_404, redirect
from .models import Company, Meeting, Outside, Topic, TopicFile, Activity, ActivityFile
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from datetime import datetime, date
from django.http import HttpResponse
from weasyprint import HTML, CSS
import tempfile
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .utils import create_pdf, send_pdf


def outstanding_all_pica(request):
    tta_topics = Topic.objects.filter(
        Q(status="O") & Q(topic2company__short_code="TTA")
    )
    abb_topics = Topic.objects.filter(
        Q(status="O") & Q(topic2company__short_code="ABB")
    )
    smm_topics = Topic.objects.filter(
        Q(status="O") & Q(topic2company__short_code="SMM")
    )
    top_topics = Topic.objects.filter(
        Q(status="O") & Q(topic2company__short_code="TOP")
    )
    kcm_topics = Topic.objects.filter(
        Q(status="O") & Q(topic2company__short_code="KCM")
    )
    pmm_topics = Topic.objects.filter(
        Q(status="O") & Q(topic2company__short_code="PMM")
    )
    other_topics = Topic.objects.filter(
        Q(status="O") & Q(topic2company__short_code="OTHER")
    )
    context = {
        'tta': tta_topics,
        'abb': abb_topics,
        'smm': smm_topics,
        'top': top_topics,
        'kcm': kcm_topics,
        'pmm': pmm_topics,
        'other': other_topics,
        'from_to': 1,
    }
    return render(request, 'pica/outstanding_topic_company.html', context)


def dashboard_pica(request, cpy):
    company = get_object_or_404(Company, short_code=cpy)
    topics = Topic.objects.filter(
        Q(topic2company__short_code=cpy) & Q(status="O")
    )
    context = {
        'topics': topics,
        'company': company,
        'from_to': 2,
    }
    return render(request, 'pica/dashboard_pica.html', context)


def dashboard_pica_detail(request, pk, cpy, from_to):
    topic = get_object_or_404(Topic, pk=pk)
    company = get_object_or_404(Company, short_code=cpy)
    meet = get_object_or_404(Meeting, meeting2topic=topic)
    activities = Activity.objects.filter(activity2topic=topic)
    context = {
        'topic': topic,
        'company': company,
        'meet': meet,
        'activities': activities,
        'from_to': from_to,
    }
    return render(request, 'pica/dashboard_pica_detail.html', context)


def pica_close(request, pk, cpy):
    topic = get_object_or_404(Topic, pk=pk)
    company = get_object_or_404(Company, short_code=cpy)
    if request.method == "POST":
        topic.status = "C"
        topic.save()
        messages.success(request, "PICA has been closed!")
        return redirect('pica:dashboard_pica', company.short_code)
    context = {
        'topic': topic,
        'company': company,
    }
    return render(request, 'pica/close_pica_confirmation.html', context)


def dashboard_mom(request, cpy):
    today = date.today()
    company = get_object_or_404(Company, short_code=cpy)
    last_meets = Meeting.objects.filter(
        Q(meeting_date__lt=today) & Q(meeting2company__short_code=cpy))
    # incoming_meets = Meeting.objects.filter(meeting_date__gte=today)

    context = {
        'company': company,
        'last_meets': last_meets,
        # 'incoming_meets': incoming_meets,
        'cpy': cpy,
    }
    return render(request, 'pica/dashboard_mom.html', context)


def dashboard_mom_detail(request, pk):
    meet = get_object_or_404(Meeting, pk=pk)
    internal_participants = meet.meeting2user.all()
    outside_participants = meet.meeting2outside.all()
    topics = Topic.objects.filter(topic2meeting=meet)
    cpy = meet.meeting2company.short_code
    context = {
        'meet': meet,
        'internal_participants': internal_participants,
        'outside_participants': outside_participants,
        'topics': topics,
        'cpy': cpy,
    }
    return render(request, 'pica/dashboard_mom_detail.html', context)


def user_activity(request, pk):
    usr = get_object_or_404(User, pk=pk)
    topic_open = Topic.objects.filter(
        Q(topic2user=usr) & Q(status='O'))
    topic_close = Topic.objects.filter(
        Q(topic2user=usr) & Q(status='C'))
    total_topic = len(topic_open) + len(topic_close)
    total_open = len(topic_open)
    total_close = len(topic_close)
    context = {
        'total_topic': total_topic,
        'total_open': total_open,
        'total_close': total_close,
        'topic_open': topic_open,
        'usr': usr,
    }
    return render(request, 'pica/user_activity.html', context)


class InputUserActivityView(View):
    def get(self, request, tp, user_id):
        today = date.today()
        topic = get_object_or_404(Topic, pk=tp)
        usr = get_object_or_404(User, pk=user_id)
        meet = topic.topic2meeting
        form = EntryActivityForm()
        form_file = MultiUploadActivityFileForm()
        form_topic = TopicActivityForm(instance=topic)
        activities = Activity.objects.filter(activity2topic=topic).order_by('-activity_date')[:10]
        context = {
            'form': form,
            'meet': meet,
            'usr': usr,
            'form_file': form_file,
            'form_topic': form_topic,
            'today': today,
            'topic': topic,
            'activities': activities,
        }
        return render(request, 'pica/input_user_activity.html', context)

    def post(self, request, tp, user_id):
        today = date.today()
        topic = get_object_or_404(Topic, pk=tp)
        usr = get_object_or_404(User, pk=user_id)
        meet = topic.topic2meeting
        activities = Activity.objects.filter(activity2topic=topic).order_by('-activity_date')[:10]
        form = EntryActivityForm(request.POST)
        form_file = MultiUploadActivityFileForm(request.POST, request.FILES)
        form_topic = TopicActivityForm(instance=topic)
        if form.is_valid() and form_file.is_valid():
            cek_activity = Activity.objects.filter(
                Q(activity2topic=topic) & Q(activity2user=usr) & Q(activity_date=date.today())
            )
            if cek_activity:
                messages.error(request,
                               "Activity for today has been already input. Please click update button if you want to update.")
            else:
                new_activity = form.save(commit=False)
                new_activity.activity2topic = topic
                new_activity.activity2user = usr
                new_activity.save()
                files = request.FILES.getlist('doc_file')
                for file in files:
                    activityfile_instance = ActivityFile(doc_file=file, activityfile2activity=topic)
                    activityfile_instance.save()
                messages.success(request, "Data topic has been saved successfully!")

            form = EntryActivityForm()
            form_file = MultiUploadActivityFileForm()
            form_topic = TopicActivityForm(instance=topic)
            meet = topic.topic2meeting
            activities = Activity.objects.filter(activity2topic=topic).order_by('-activity_date')[:10]
            context = {
                'form': form,
                'meet': meet,
                'form_file': form_file,
                'form_topic': form_topic,
                'usr': usr,
                'topic': topic,
                'activities': activities,
                'today': today,
            }
            return render(request, 'pica/input_user_activity.html', context)
        else:
            print(form)
            print(form.errors)
            form = EntryActivityForm(request.POST)
            form_file = MultiUploadActivityFileForm(request.POST, request.FILES)
            form_topic = TopicActivityForm(instance=topic)
            context = {
                'form': form,
                'meet': meet,
                'form_file': form_file,
                'form_topic': form_topic,
                'usr': usr,
                'activities': activities,
                'today': today,
            }
            return render(request, 'pica/input_user_activity.html', context)


def update_user_activity(request, act, user_id):
    usr = get_object_or_404(User, pk=user_id)
    activity = get_object_or_404(Activity, pk=act)
    topic = activity.activity2topic
    if request.method == "POST":
        form = UpdateActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            messages.success(request, "Data has been successfully updated.")
            return redirect(f'/pica/input_user_activity/{topic.id}/{usr.id}/')
    form = UpdateActivityForm(instance=activity)
    context = {
        'form': form,
        'usr': usr,
        'topic': topic,
        'activity': activity,
    }
    return render(request, 'pica/update_user_activity.html', context)


def details_user_activity(request, act, user_id):
    usr = get_object_or_404(User, pk=user_id)
    activity = get_object_or_404(Activity, pk=act)
    topic = activity.activity2topic
    context = {
        'usr': usr,
        'topic': topic,
        'activity': activity,
    }
    return render(request, 'pica/details_user_activity.html', context)


class NewEntryTopicView(View):
    def get(self, request, pk):
        meet = get_object_or_404(Meeting, pk=pk)
        cpy = meet.meeting2company.short_code
        form = EntryTopicsForm()
        form_file = MultiUploadFileForm()
        today = date.today()
        context = {
            'form': form,
            'meet': meet,
            'new_topic': True,
            'topic': None,
            'form_file': form_file,
            'today': today,
            'cpy': cpy,
        }
        return render(request, 'pica/input_topic.html', context)

    def post(self, request, pk):
        meet = get_object_or_404(Meeting, pk=pk)
        cpy = meet.meeting2company.short_code
        form = EntryTopicsForm(request.POST)
        form_file = MultiUploadFileForm(request.POST, request.FILES)
        if form.is_valid() and form_file.is_valid():
            new_topic = form.save(commit=False)
            new_topic.issue_date = meet.meeting_date
            new_topic.topic2meeting = meet
            new_topic.save()
            files = request.FILES.getlist('doc_file')
            for file in files:
                topicfile_instance = TopicFile(doc_file=file, topicfile2topic=new_topic)
                topicfile_instance.save()
            messages.success(request, "Data topic has been saved successfully!")
            form = EntryTopicsForm()
            form_file = MultiUploadFileForm()
            context = {
                'form': form,
                'new_topic': True,
                'topic': None,
                'meet': meet,
                'form_file': form_file,
                'cpy': cpy,
            }
            return render(request, 'pica/input_topic.html', context)
        else:
            print(form)
            print(form.errors)
            form = EntryTopicsForm(request.POST)
            form_file = MultiUploadFileForm(request.POST, request.FILES)
            context = {
                'form': form,
                'new_topic': True,
                'topic': None,
                'meet': meet,
                'form_file': form_file,
                'cpy': cpy,
            }
            return render(request, 'pica/input_topic.html', context)


class UpdateTopicView(View):
    def get(self, request, tp):
        topic = get_object_or_404(Topic, pk=tp)
        meet = topic.topic2meeting
        cpy = meet.meeting2company.short_code
        form = UpdateTopicsForm(instance=topic)
        form_file = MultiUploadFileForm()
        today = date.today()
        context = {
            'form': form,
            'meet': meet,
            'new_topic': False,
            'topic': topic,
            'form_file': form_file,
            'today': today,
            'cpy': cpy,
        }
        return render(request, 'pica/update_topic.html', context)

    def post(self, request, tp):
        topic = get_object_or_404(Topic, pk=tp)
        meet = topic.topic2meeting
        cpy = meet.meeting2company.short_code
        form = UpdateTopicsForm(request.POST, instance=topic)
        form_file = MultiUploadFileForm(request.POST, request.FILES)
        today = date.today()
        if form.is_valid() and form_file.is_valid():
            form.save()
            files = request.FILES.getlist('doc_file')
            for file in files:
                topicfile_instance = TopicFile(doc_file=file, topicfile2topic=topic)
                topicfile_instance.save()
            messages.success(request, "Data topic has been updated successfully!")
            if meet.meeting_date >= today:
                return redirect('pica:meeting_detail', meet.pk)
            else:
                return redirect('pica:dashboard_mom_detail', meet.pk)
        else:
            print(form)
            print(form.errors)
            topic = get_object_or_404(Topic, pk=tp)
            topicfile = TopicFile.objects.filter(topicfile2topic=topic)
            form = UpdateTopicsForm(request.POST, instance=topic)
            form_file = MultiUploadFileForm(request.POST, request.FILES, instance=topicfile)
            today = date.today()
            context = {
                'form': form,
                'new_topic': False,
                'topic': topic,
                'meet': meet,
                'form_file': form_file,
                'cpy': cpy,
                'today': today,
            }
            return render(request, 'pica/update_topic.html', context)


def delete_topic(request, mt, tp, fr):
    meet = get_object_or_404(Meeting, pk=mt)
    topic = get_object_or_404(Topic, pk=tp)
    if topic.topic2user.all():
        messages.error(request, "Topic has already person in charge related. It cannot be deleted!")
        if fr == "DS":
            return redirect('pica:dashboard_mom_detail', meet.pk)
        else:
            return redirect('pica:meeting_detail', meet.pk)
    if request.method == "POST":
        topic.delete()
        messages.success(request, "Topic has been deleted!")
        if fr == "DS":
            return redirect('pica:dashboard_mom_detail', meet.pk)
        else:
            return redirect('pica:meeting_detail', meet.pk)
    context = {
        'topic': topic,
        'meet': meet,
        'fr': fr,
    }
    return render(request, 'pica/delete_topic_confirmation.html', context)


class NewMeetingView(View):
    def get(self, request, cpy):
        today = date.today()
        form = NewMeetingForm()
        company = get_object_or_404(Company, short_code=cpy)
        incoming_meets = Meeting.objects.filter(
                    Q(meeting_date__gte=today) & Q(meeting2company__short_code=cpy)
                )

        context = {
            'form': form,
            'company': company,
            'incoming_meets': incoming_meets,
        }
        return render(request, 'pica/new_meeting.html', context)

    def post(self, request, cpy):
        company = get_object_or_404(Company, short_code=cpy)
        form = NewMeetingForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            meet_date = cd['meeting_date']
            find_meeting = Meeting.objects.filter(
                Q(meeting_date=meet_date) & Q(meeting2company__short_code=cpy))
            if find_meeting:
                messages.error(request, "Meeting for related date already created!")
                form = NewMeetingForm()
                today = date.today()
                incoming_meets = Meeting.objects.filter(
                    Q(meeting_date__gte=today) & Q(meeting2company__short_code=cpy)
                )
                context = {
                    'form': form,
                    'company': company,
                    'incoming_meets': incoming_meets,
                }
                return render(request, 'pica/new_meeting.html', context)

            new_meet = form.save(commit=False)
            new_meet.meeting2company = company
            new_meet.save()
            messages.success(request, "Data New Meeting has been saved!")
            return redirect('pica:meeting_detail', new_meet.pk)
        else:
            context = {
                'form': form,
                'company': company,
            }
            return render(request, 'pica/new_meeting.html', context)


def meeting_detail(request, pk):
    meet = get_object_or_404(Meeting, pk=pk)
    internal_participants = meet.meeting2user.all()
    outside_participants = meet.meeting2outside.all()
    topics = Topic.objects.filter(topic2meeting=meet)
    company = meet.meeting2company.short_code
    today = date.today()
    context = {
        'meet': meet,
        'internal_participants': internal_participants,
        'outside_participants': outside_participants,
        'topics': topics,
        'company': company,
        'today': today,
    }
    return render(request, 'pica/meeting_detail.html', context)


def delete_meeting(request, pk, cpy):
    meet = get_object_or_404(Meeting, pk=pk)
    if meet.meeting2topic.all():
        messages.error(request, "Meeting has already topic related. It cannot be deleted!")
        return redirect('pica:new_meeting', cpy)
    if request.method == "POST":
        meet.delete()
        messages.success(request, "Meeting has been deleted!")
        return redirect('pica:new_meeting', cpy)
    context = {
        'cpy': cpy,
        'meet': meet,
    }
    return render(request, 'pica/delete_meeting_confirmation.html', context)


def input_internal_participant(request, pk):
    today = date.today()
    meet = get_object_or_404(Meeting, pk=pk)
    cpy = meet.meeting2company.short_code
    current_participants = meet.meeting2user.all()
    search_query = ""
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    internal_participants = User.objects.distinct().filter(
        Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query)).exclude(username='admin')

    candidates = []
    for internal_participant in internal_participants:
        if internal_participant not in current_participants:
            candidates.append(internal_participant)
    page = request.GET.get('page')
    results = 10
    paginator = Paginator(candidates, results)
    try:
        candidates = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        candidates = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        candidates = paginator.page(page)

    context = {
        'candidates': candidates,
        'search_query': search_query,
        'meet': meet,
        'paginator': paginator,
        'today': today,
        'cpy': cpy,
    }
    return render(request, 'pica/input_internal_participant.html', context)


def add_internal_participant(request, meet_pk, user_id):
    meet = get_object_or_404(Meeting, pk=meet_pk)
    usr = get_object_or_404(User, pk=user_id)
    meet.meeting2user.add(usr)
    messages.success(request, "Participant was successfully added!")
    return redirect('pica:input_internal_participant', meet.pk)


def delete_internal_participant(request, mt, usr):
    meet = get_object_or_404(Meeting, pk=mt)
    participant = get_object_or_404(User, pk=usr)
    if request.method == "POST":
        meet.meeting2user.remove(participant)
        messages.success(request, "Participant has been deleted!")
        return redirect('pica:meeting_detail', meet.pk)
    context = {
        'meet': meet,
        'participant': participant,
    }
    return render(request, 'pica/delete_internal_confirmation.html', context)


def input_outside_participant(request, pk):
    today = date.today()
    meet = get_object_or_404(Meeting, pk=pk)
    current_participants = meet.meeting2outside.all()
    cpy = meet.meeting2company.short_code
    search_query = ""
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    outside_participants = Outside.objects.distinct().filter(fullname__icontains=search_query)
    candidates = []
    for outside_participant in outside_participants:
        if outside_participant not in current_participants:
            candidates.append(outside_participant)
    page = request.GET.get('page')
    results = 10
    paginator = Paginator(candidates, results)
    try:
        candidates = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        candidates = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        candidates = paginator.page(page)

    context = {
        'candidates': candidates,
        'search_query': search_query,
        'meet': meet,
        'paginator': paginator,
        'today': today,
        'cpy': cpy,
    }
    return render(request, 'pica/input_outside_participant.html', context)


def add_outside_participant(request, meet_pk, user_id):
    meet = get_object_or_404(Meeting, pk=meet_pk)
    usr = get_object_or_404(Outside, pk=user_id)
    meet.meeting2outside.add(usr)
    messages.success(request, "Outside Participant was successfully added!")
    return redirect('pica:input_outside_participant', meet.pk)


def delete_outside_participant(request, mt, usr):
    meet = get_object_or_404(Meeting, pk=mt)
    participant = get_object_or_404(Outside, pk=usr)
    if request.method == "POST":
        meet.meeting2outside.remove(participant)
        messages.success(request, "Participant has been deleted!")
        return redirect('pica:meeting_detail', meet.pk)
    context = {
        'meet': meet,
        'participant': participant,
    }
    return render(request, 'pica/delete_outside_confirmation.html', context)


def input_pic_topic(request, tp):
    topic = get_object_or_404(Topic, pk=tp)
    meet = topic.topic2meeting
    cpy = meet.meeting2company.short_code
    current_pics = topic.topic2user.all()
    search_query = ""
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    user_exists = User.objects.distinct().filter(
        Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query))

    candidates = []
    for user_exist in user_exists:
        if user_exist not in current_pics:
            candidates.append(user_exist)
    page = request.GET.get('page')
    results = 10
    paginator = Paginator(candidates, results)
    try:
        candidates = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        candidates = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        candidates = paginator.page(page)

    context = {
        'candidates': candidates,
        'search_query': search_query,
        'meet': meet,
        'paginator': paginator,
        'topic': topic,
        'cpy': cpy,
    }
    return render(request, 'pica/input_pic_topic.html', context)


def add_pic_topic(request, meet_pk, tp, user_id):
    meet = get_object_or_404(Meeting, pk=meet_pk)
    usr = get_object_or_404(User, pk=user_id)
    topic = get_object_or_404(Topic, pk=tp)
    topic.topic2user.add(usr)
    messages.success(request, "PIC topic was successfully added!")
    return redirect('pica:input_pic_topic', topic.pk)


def delete_pic_topic(request, meet_pk, tp, user_id):
    meet = get_object_or_404(Meeting, pk=meet_pk)
    topic = get_object_or_404(Topic, pk=tp)
    pic = get_object_or_404(User, pk=user_id)
    cpy = topic.topic2company.short_code
    if request.method == "POST":
        topic.topic2user.remove(pic)
        messages.success(request, "PIC topic has been deleted!")
        return redirect('pica:update_topic', topic.pk)
    context = {
        'meet': meet,
        'pic': pic,
        'topic': topic,
        'cpy': cpy,
    }
    return render(request, 'pica/delete_pic_topic_confirmation.html', context)


def preview_pdf(request, pk):
    result, response = create_pdf(request, pk)
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    return response


def sending_pdf(request, pk):
    meet = get_object_or_404(Meeting, pk=pk)
    cpy = meet.meeting2company.short_code
    topiks = Topic.objects.filter(topic2meeting=meet)
    # Create MoM pdf for all BOD
    result, response = create_pdf(request, meet.pk, None)
    send_to = []
    signatures = meet.meeting2user.filter(user2profile__bod='Y')
    for signature in signatures:
        send_to.append(signature.email)
    send_pdf(request, result, meet, send_to, bod=True)
    for topik in topiks:
        pics = topik.topic2user.all()
        send_to = []
        for pic in pics:
            send_to.append(pic.email)
            # Create Assignment pdf for all PIC
        result, response = create_pdf(request, meet.pk, topik.pk)
        send_pdf(request, result, meet, send_to, bod=None)
    messages.success(request, "MoM & Assignment sudah terkirim via email!")
    return redirect(f'/pica/dashboard_mom/{cpy}/')
