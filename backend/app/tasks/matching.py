from celery import shared_task
from datetime import datetime
import logging
import os
import sys

from db.session import SessionLocal
from services.matching import MatchingService

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

@shared_task(bind=True, name="run_property_matching")
def run_property_matching(self, user_id: int):
    """Celery task to run property matching for a specific user"""
    try:
        logger.info(f"Starting property matching task for user {user_id}")
        
        # Initialize database session
        db = SessionLocal()
        
        try:
            # Get user's KvCore token
            matching_service = MatchingService(db)
            user = await matching_service.get_user_with_token(user_id)
            
            if not user or not user.kvcore_token:
                logger.error(f"No KvCore token found for user {user_id}")
                return {
                    "status": "error",
                    "message": "No KvCore token configured",
                    "user_id": user_id,
                    "timestamp": datetime.now().isoformat()
                }
            
            # Add your scripts directory to path
            scripts_path = os.path.join(os.path.dirname(__file__), '../../../scripts')
            sys.path.append(scripts_path)
            
            # Import and run your matching script
            from KvCore_DT_scan_matches import search_datatree_thread
            search_datatree_thread()
            
            logger.info(f"Successfully completed matching for user {user_id}")
            return {
                "status": "success",
                "user_id": user_id,
                "task_id": self.request.id,
                "timestamp": datetime.now().isoformat()
            }
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error in matching task for user {user_id}: {str(e)}")
        raise self.retry(exc=e, countdown=60)
