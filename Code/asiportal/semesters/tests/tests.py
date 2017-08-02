from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from semesters.models import Semester

class SemesterTest(TestCase):
    def test_semster_slugs_are_correct(self):
        sem = Semester.objects.create()
        year = timezone.now().year
        expected_slug = '%s-%s'%(sem.get_term_display(), year)
        self.assertEqual(sem.slug, expected_slug.lower())
    def test_semester_year_default_is_this_year(self):
        sem = Semester.objects.create()
        expected_year = timezone.now().year
        self.assertEqual(sem.year, expected_year)

    def test_semester_object_is_represented_correctly(self):
        sem = Semester.objects.create()
        expected_text = 'Fall %s' % timezone.now().year
        self.assertEqual(sem.__str__(), expected_text)

    def test_semester_current_semester_returns_right_semesters(self):
        sem = Semester.objects.create()
        qs = Semester.objects.current()
        self.assertIn(sem,qs)

    def test_semester_current_doesnt_show_old_semesters(self):
        sem = Semester.objects.create(year=1982)
        qs = Semester.objects.current()
        self.assertFalse(qs)

    def test_semester_current_doesnt_show_future_semesters(self):
        now = timezone.now().date()
        later = now + timedelta(weeks=12)
        Semester.objects.create(start_date = later,
                end_date = later + timedelta(weeks=16))
        self.assertFalse(Semester.objects.current())

    def test_semester_current_will_return_only_summera_b_andc(self):
        now = timezone.now().date()
        summera_start = now
        summera_end = summera_start + timedelta(weeks=6)
        summerb_start = summera_end + timedelta(weeks=1)
        summerb_end = summerb_start + timedelta(weeks=6)
        summerc_start = summera_start
        summerc_end = summerb_end
        old = Semester.objects.create(start_date = now,
                                      end_date = now
                                      )
        sc = Semester.objects.create(start_date = summerc_start,
                                end_date = summerc_end,
                                year = now.year,
                                term = 'SC')
        sa = Semester.objects.create(start_date = summera_start,
                                end_date = summera_end,
                                year = now.year,
                                term = 'SA')
        sb = Semester.objects.create(start_date = summerb_start,
                                end_date = summerb_end,
                                year = now.year,
                                term = 'SB')
        summers = Semester.objects.all()
        currents = Semester.objects.current()
        self.assertIn(sc, currents)
        self.assertIn(sb, currents)
        self.assertIn(sa, currents)
        self.assertNotIn(old, currents)
