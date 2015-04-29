from django.db import models
from users.models import Patient, Doctor, is_doctor, is_employee, is_patient, is_nurse
from datetime import datetime, date
from calendar import HTMLCalendar
from itertools import groupby
from django.core.urlresolvers import reverse

from django.utils.html import conditional_escape as esc

# Create your models here.

class Appointment(models.Model):
    patient = models.ForeignKey(Patient);
    doctor = models.ForeignKey(Doctor)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    title = models.CharField(max_length = 100)
    description = models.CharField(max_length = 500)
    location = models.CharField(max_length = 200)

    def has_passed(self):
        return self.end_time < datetime.now()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        #return reverse('home', kwargs={'slug': self.slug})
        return reverse('appointment-detail', kwargs={"pk":self.pk})



class AppointmentCalendar(HTMLCalendar):

    def __init__(self, appointments):
        super(AppointmentCalendar, self).__init__()
        self.appointments = self.group_by_day(appointments)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.appointments:
                cssclass += ' filled'
                body = ['<ul>']
                for appointment in self.appointments[day]:
                    body.append('<li>')
                    body.append('<a href="%s">' % appointment.get_absolute_url())
                    body.append(esc(appointment.title))
                    body.append('</a></li>')
                body.append('</ul>')
                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(AppointmentCalendar, self).formatmonth(year, month)

    def group_by_day(self, appointments):

        field = lambda appointment: appointment.start_time.day
        return dict(
             [(day, list(items)) for day, items in groupby(appointments, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)

    #def get_absolute_url(self):
        #return reverse('home', kwargs={'slug': self.slug})
        #return reverse('calendar', kwargs={'month':datetime.now().month,'year':datetime.now().year})

    def get_next_month_url(self):
        new_year = self.year
        if self.month == 12:
            new_month = 1
            new_year = self.year+1
        else:
            new_month = self.month+1
        return reverse("calendar", kwargs={"year":new_year, "month":new_month})


    def get_prev_month_url(self):
        new_year = self.year
        if self.month == 1:
            new_month = 12
            new_year = self.year-1
        else:
            new_month = self.month-1
        return reverse("calendar", kwargs={"year":new_year, "month":new_month})
