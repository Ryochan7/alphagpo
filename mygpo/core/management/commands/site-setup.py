import logging

from django.core.management.base import BaseCommand
from django.db import transaction
from django.template.defaultfilters import slugify

from mygpo.categories.models import Category, CategoryTag


DEFAULT_CATEGORIES = [
    {
        "category": {
            "title": "Arts",
            "num_entries": 0,
        },
        "tags": [
            "arts", "books", "design", "fashion-beauty", "food", "performing-arts",
            "visual-arts",
        ],
    },
    {
        "category": {
            "title": "Business",
            "num_entries": 0,
        },
        "tags": [
            "business", "careers", "entrepreneurship", "investing", "management",
            "marketing", "non-profit",
        ],
    },
    {
        "category": {
            "title": "Comedy",
            "num_entries": 0,
        },
        "tags": [
            "comedy", "comedy-interviews", "improv", "stand-up"
        ],
    },
    {
        "category": {
            "title": "Education",
            "num_entries": 0,
        },
        "tags": [
            "education", "courses", "how-to", "language-learning",
            "self-improvement",
        ],
    },
    {
        "category": {
            "title": "Fiction",
            "num_entries": 0,
        },
        "tags": [
            "fiction", "comedy-fiction", "drama", "science-fiction",
        ],
    },
    {
        "category": {
            "title": "Government",
            "num_entries": 0,
        },
        "tags": [
            "government",
        ],
    },
    {
        "category": {
            "title": "Health & Fitness",
            "num_entries": 0,
        },
        "tags": [
            "health-fitness", "alternative-health", "fitness", "medicine",
            "mental-health", "nutrition", "sexuality",
        ],
    },
    {
        "category": {
            "title": "History",
            "num_entries": 0,
        },
        "tags": [
            "history",
        ],
    },
    {
        "category": {
            "title": "Kids & Family",
            "num_entries": 0,
        },
        "tags": [
            "kids-family", "education-for-kids", "parenting", "pets-animals",
            "stories-for-kids",
        ],
    },
    {
        "category": {
            "title": "Leisure",
            "num_entries": 0,
        },
        "tags": [
            "leisure", "animation-manga", "automotive", "aviation", "crafts",
            "games", "hobbies", "home-garden", "video-games",
        ],
    },
    {
        "category": {
            "title": "Music",
            "num_entries": 0,
        },
        "tags": [
            "music", "music-commentary", "music-history", "music-interviews",
        ],
    },
    {
        "category": {
            "title": "News",
            "num_entries": 0,
        },
        "tags": [
            "news", "business-news", "daily-news", "entertainment-news",
            "news-commentary", "politics", "sports-news", "tech-news",
        ],
    },
    {
        "category": {
            "title": "Religion & Spirituality",
            "num_entries": 0,
        },
        "tags": [
            "religion-spirituality", "christianity", "buddhism", "hinduism",
            "islam", "judiasm", "religion", "spirituality",
        ],
    },
    {
        "category": {
            "title": "Science",
            "num_entries": 0,
        },
        "tags": [
            "science", "astronomy", "chemistry", "earth-sciences",
            "life-sciences", "mathematics", "natural-sciences", "nature",
            "physics", "social-sciences",
        ],
    },
    {
        "category": {
            "title": "Society & Culture",
            "num_entries": 0,
        },
        "tags": [
            "society-culture", "documentary", "personal-journals", "philosophy",
            "places-travel", "relationships",
        ],
    },
    {
        "category": {
            "title": "Sports",
            "num_entries": 0,
        },
        "tags": [
            "sports", "baseball", "basketball", "cricket", "fantasy-sports",
            "football", "golf", "hockey", "rugby", "soccer",
        ],
    },
    {
        "category": {
            "title": "Technology",
            "num_entries": 0,
        },
        "tags": [
            "technology",
        ],
    },
    {
        "category": {
            "title": "True Crime",
            "num_entries": 0,
        },
        "tags": [
            "true-crime",
        ],
    },
    {
        "category": {
            "title": "TV & Film",
            "num_entries": 0,
        },
        "tags": [
            "tv-film", "after-shows", "film-history", "film-interviews",
            "film-reviews", "tv-reviews",
        ],
    },
]


class Command(BaseCommand):
    help = """Run some common functions to set up an initial mygpo site after
the base Django setup commands."""

    def _setup_default_categories(self):
        # Check if categories exist and create entries if they do not
        for entry in DEFAULT_CATEGORIES:
            cat = entry["category"]
            slug_candidate = slugify(cat["title"])
            category = Category.objects.filter(title_slug=slug_candidate).first()
            if not category:
                category = Category.objects.create(**cat)

            # Check each tag to see if it needs to be created
            for tag in entry["tags"]:
                tag_exists = any(tag == cat_tag.tag for cat_tag in category.tags.all())
                if not tag_exists:
                    category.tags.create(tag=tag)


    def handle(self, *args, **options):
        with transaction.atomic():
            self._setup_default_categories()
