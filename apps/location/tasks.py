from celery import shared_task
from django.utils import timezone
from apps.location.models import DossierLocation
import logging

logger = logging.getLogger(__name__)


# This will update the `disponibilite` of promotion articles according
# to their `start_date` and `end_date`.
@shared_task(name='location.tasks.update_locations')
def update_locations():
    now = timezone.now()

    try:
        # End location first
        DossierLocation.objects.filter(
            date_retour__lte=now,
            deal__in=['en location', 'commencé']
        ).update(deal='disponible')

        # Start location
        DossierLocation.objects.filter(
            date_depart__lte=now,
            deal='en location'
        ).update(deal='commencé')

        logger.info("location update completed successfully")
        return True

    except Exception:
        logger.exception("Failed to update location")
        raise

