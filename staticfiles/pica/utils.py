from .models import Meeting, Topic, Signature
from django.http import HttpResponse
from django.http import HttpResponse
from weasyprint import HTML, CSS
import tempfile
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from datetime import date
from django.template import loader
from django.contrib.auth.models import User


def create_pdf(request, pk, top=None):
    meet = get_object_or_404(Meeting, pk=pk)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=invoice.pdf'
    response['Context-Transfer-Encoding'] = 'binary'
    internal_participants = meet.meeting2user.all()
    outside_participants = meet.meeting2outside.all()
    if top is None:
        topiks = Topic.objects.filter(topic2meeting=meet)
    else:
        topiks = get_object_or_404(Topic, pk=top)

    # Format signature
    signatures = meet.meeting2user.filter(user2profile__bod='Y').order_by('first_name')
    cpy = meet.meeting2company.short_code
    context = {
        'internal_participants': internal_participants,
        'outside_participants': outside_participants,
        'topiks': topiks,
        'meet': meet,
        'signatures': signatures,
        'cpy': cpy,
    }
    if top is None:
        html_string = render_to_string('pica/mom.html', context)
    else:
        html_string = render_to_string('pica/mom-pic.html', context)

    result = HTML(string=html_string, base_url=request.build_absolute_uri()).render(stylesheets=[
        settings.STATIC_ROOT / 'bootstrap/css/bootstrap.min.css',
        settings.STATIC_ROOT / 'css/styles.css',
        settings.STATIC_ROOT / 'css/Open Sans.css',
    ]).write_pdf()
    return result, response


def send_pdf(request, result, meet, to_email, bod=None):
    today = date.today()
    if bod is None:
        for em in to_email:
            template = loader.get_template('pica/templ_pic.txt')
            name = get_object_or_404(User, email=em)
            context = {
                'name': name,
                'email': em,
                'meet': meet,
            }
            message = template.render(context)
            mail_subject = f"New Assignment {today}"
            email = EmailMultiAlternatives(
                mail_subject, message,
                "ePica System",
                ['epicasistem@gmail.com', em]
            )
            filename = f"New_Assignment{today}.pdf"
            email.attach(filename, result, 'application/pdf')
            email.content_subtype = 'html'
            email.send(fail_silently=False)
    else:
        for em in to_email:
            template = loader.get_template('pica/templ_bod.txt')
            name = get_object_or_404(User, email=em)
            context = {
                'name': name,
                'email': em,
                'meet': meet,
            }
            message = template.render(context)
            mail_subject = f"Meeting BOD {today}"
            email = EmailMultiAlternatives(
                mail_subject, message,
                "ePica System",
                ['epicasistem@gmail.com', em]
            )
            filename = f"Meeting_BOD_{today}.pdf"
            email.attach(filename, result, 'application/pdf')
            email.content_subtype = 'html'
            email.send(fail_silently=False)
    return
