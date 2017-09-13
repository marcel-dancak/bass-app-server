from django.core.management.base import BaseCommand, CommandError
from basscloud.catalog.models import Project


class Command(BaseCommand):
    help = 'Generates sitemap in simple text format'

    def handle(self, *args, **options):
        site = 'https://basscloud.net'
        # self.stdout.write(site+'/projects')
        for project in Project.objects.all():
            self.stdout.write(site+'/project/'+project.id)
