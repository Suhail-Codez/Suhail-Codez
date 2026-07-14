"""
seed_reviews — load data/drug_reviews.csv into the DrugReview table.

Root cause fixed: the training script (data/generate_and_train.py) only
produces the ML .pkl/.json model artifacts; it never wrote the underlying
review rows into the Django database. As a result recommender_drugreview
was empty (0 rows) even though the models were trained on ~9,000 reviews,
so per-drug review counts/ratings and dashboard analytics were always zero.

Usage:
    python manage.py seed_reviews            # seed only if table is empty
    python manage.py seed_reviews --force     # wipe and reseed regardless
"""
import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from recommender.models import DrugReview


class Command(BaseCommand):
    help = "Seed the DrugReview table from data/drug_reviews.csv (idempotent unless --force)."

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Wipe existing DrugReview rows and reseed.")
        parser.add_argument("--csv-path", default=None, help="Override path to drug_reviews.csv")

    def handle(self, *args, **options):
        from recommender.views import _vader, _load

        existing = DrugReview.objects.count()
        if existing and not options["force"]:
            self.stdout.write(self.style.WARNING(
                f"DrugReview already has {existing} rows. Use --force to wipe and reseed."
            ))
            return

        csv_path = options["csv_path"] or os.path.join(
            settings.BASE_DIR.parent, "data", "drug_reviews.csv"
        )
        if not os.path.exists(csv_path):
            self.stderr.write(self.style.ERROR(f"CSV not found at {csv_path}"))
            return

        _load()  # ensures the VADER analyzer is available for _vader()

        if options["force"]:
            deleted, _ = DrugReview.objects.all().delete()
            self.stdout.write(f"Deleted {deleted} existing rows.")

        batch = []
        BATCH_SIZE = 500
        created = 0

        with open(csv_path, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                drug_name = (row.get("drugName") or "").strip()
                condition = (row.get("condition") or "").strip()
                review = (row.get("review") or "").strip()
                if not drug_name or not review:
                    continue
                try:
                    rating = float(row.get("rating") or 0)
                except ValueError:
                    rating = 0.0
                try:
                    useful_count = int(float(row.get("usefulCount") or 0))
                except ValueError:
                    useful_count = 0

                sent = _vader(review)

                batch.append(DrugReview(
                    drug_name=drug_name,
                    condition=condition,
                    review=review,
                    rating=rating,
                    useful_count=useful_count,
                    sentiment=sent["sentiment"],
                    sentiment_score=sent["sentiment_score"],
                    pos_score=sent["pos"],
                    neg_score=sent["neg"],
                    neu_score=sent["neu"],
                    compound_score=sent["compound"],
                ))
                if len(batch) >= BATCH_SIZE:
                    with transaction.atomic():
                        DrugReview.objects.bulk_create(batch)
                    created += len(batch)
                    batch = []

            if batch:
                with transaction.atomic():
                    DrugReview.objects.bulk_create(batch)
                created += len(batch)

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {created} DrugReview rows from {csv_path}."
        ))
