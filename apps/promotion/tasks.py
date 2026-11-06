from celery import shared_task
from django.utils import timezone
from apps.promotion.models import Promotion
import logging

logger = logging.getLogger(__name__)


# This will update the `disponibilite` of promotion articles according
# to their `start_date` and `end_date`.
@shared_task(name='promotion.tasks.update_promotions')
def update_promotions():
    now = timezone.now()
    print(now)

    try:
        # End promotions first
        Promotion.objects.filter(
            end_date__lte=now,
            disponibilite__in=['disponible', 'commencé']
        ).update(disponibilite='promotion done')

        # Start promotions
        Promotion.objects.filter(
            start_date__lte=now,
            disponibilite='disponible'
        ).update(disponibilite='commencé')

        logger.info("Promotion update completed successfully")
        return True

    except Exception:
        logger.exception("Failed to update promotions")
        raise

