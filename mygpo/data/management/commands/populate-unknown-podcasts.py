from django.core.management.base import BaseCommand

from mygpo.podcasts.models import Podcast
from mygpo.data.models import PodcastUpdateResult
from mygpo.data.feeddownloader import update_podcasts


class Command(BaseCommand):
    help = "Find untitled podcasts (from client subscriptions) and attempt to populate podcast info"

    def handle(self, *args, **options):
        # Consider all Podcast objects with no known latest episode timestamp as unknown.
        # Should be faster than checking for empty title. Might add index in future
        podcast_urls = Podcast.objects.filter(latest_episode_timestamp=None).prefetch_related("urls").values_list("urls__url")

        # Grab first applicable URL for each Podcast
        podcast_url_list = [url_group[0] for url_group in podcast_urls if url_group != None and len(url_group) > 0]

        # Grab info for each URL
        update_podcasts(podcast_url_list)
