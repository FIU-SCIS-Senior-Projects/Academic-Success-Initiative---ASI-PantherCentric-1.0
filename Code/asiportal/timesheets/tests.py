from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory

from .models import TimeSheet

from .views import (
        approve_timesheet,
        edit_timesheet,
        TimeSheetDetailView,
        TimeSheetListView,
        TimeSheetCreateFormView,
        AmbassadorListView,
        TimeSheetAmbassadorListView,
        FinalApproveAmbassadorTimeSheet,
        )


class ProtectionTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username='jlope590')
        self.ts = TimeSheet.objects.create(ambassador=self.user,
                pay_period_begin = timezone.now(),
                pay_period_end = timezone.now() + timedelta(weeks=2),
                )

    def test_only_authenticated_users_can_access_views(self):
        req = self.factory.get('/')
        pk_req = self.factory.get('/', kwargs={'timesheet_pk' : self.ts.pk})
        req.user = AnonymousUser()
        response = approve_timesheet(req)
        self.assertEqual(response.status_code, 302)
        response = edit_timesheet(req, self.ts.pk)
        self.assertEqual(response.status_code, 302)
        response = TimeSheetDetailView.as_view()(req, timesheet_pk=self.ts.pk)
        self.assertEqual(response.status_code, 302)
        response = TimeSheetListView.as_view()(req)
        self.assertEqual(response.status_code, 302)
        response = TimeSheetCreateFormView.as_view()(req)
        self.assertEqual(response.status_code, 302)
        response = AmbassadorListView.as_view()(req)
        self.assertEqual(response.status_code, 302)
        response = TimeSheetAmbassadorListView.as_view()(req)
        self.assertEqual(response.status_code, 302)
        response = FinalApproveAmbassadorTimeSheet.as_view()(req)
        self.assertEqual(response.status_code, 302)
