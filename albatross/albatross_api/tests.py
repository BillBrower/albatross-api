from datetime import timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from teams.models import Team

from .cron import RefreshHarvestTokensCronJob, TrailExpirationCronJob


class RefreshHarvestTokensCronJobTestCase(TestCase):

    def test_case_where_no_user_has_harvest_credentials(self):
        user = User.objects.create_user(
            email='user.1@example.com',
            first_name='Test',
            last_name='Account',
            password='password125',
            username='user.1@example.com'
        )
        Team.objects.create(
            creator=user,
            name="Team"
        )

        cronjob = RefreshHarvestTokensCronJob()
        cronjob.do()


class TrailExpirationCronJobTestCase(TestCase):
    ACCOUNT_CREDENTIALS = {
        'email': 'bill@builtbykrit.com',
        'password': 'password125'
    }

    def create_user(self, account_credentials):
        User.objects.create_user(
            email=account_credentials['email'],
            first_name='Test',
            last_name='Account',
            password=account_credentials['password'],
            username=account_credentials['email']
        )

    def test_cronjob(self):
        # Setup users
        user = User.objects.create_user(
            email='user.1@example.com',
            first_name='Test',
            last_name='Account',
            password='password125',
            username='user.1@example.com'
        )
        team = Team.objects.create(
            creator=user,
            name="Team"
        )

        user_with_nearly_expired_trial = User.objects.create_user(
            email='user.2@example.com',
            first_name='Test',
            last_name='Account',
            password='password125',
            username='user.2@example.com'
        )
        team_with_nearly_expired_trial = Team.objects.create(
            creator=user_with_nearly_expired_trial,
            name="Team with nearly expired trial",
            trial_expires_at= timezone.now() + timedelta(hours=71)
        )

        user_with_expired_trial = User.objects.create_user(
            email='user.3@example.com',
            first_name='Test',
            last_name='Account',
            password='password125',
            username='user.3@example.com'
        )
        team_with_expired_trial = Team.objects.create(
            creator=user_with_nearly_expired_trial,
            name="Team with expired trial",
            trial_expires_at= timezone.now() - timedelta(hours=1)
        )

        # Run cronjob
        cronjob = TrailExpirationCronJob()
        cronjob.do()

        # Verify results
        team = Team.objects.get(id=team.id)
        assert team.on_trial == True
        assert team.trial_expires_at > timezone.now() + timedelta(days=13)

        team_with_nearly_expired_trial = Team.objects.get(
            id=team_with_nearly_expired_trial.id)
        assert team_with_nearly_expired_trial.on_trial == True

        team_with_expired_trial = Team.objects.get(
            id=team_with_expired_trial.id)
        assert team_with_expired_trial.on_trial == False