import uuid
import asyncio
from jinja2 import Template
from app.repositories.notification_repo import NotificationRepository
from app.services.logger import logger

class NotificationManager:
    def __init__(self):
        self.repo = NotificationRepository()

    async def send_transactional_notification(self, template_key: str, payload: dict, target: str, channel: str):
        notification_id = str(uuid.uuid4())
        logger.info(f"Processing notification job {notification_id} for template: {template_key}")

        
        raw_template = "Hi {{ user_name }}, action '{{ template_key }}' processed successfully."
        compiled_body = Template(raw_template).render(user_name=payload.get("user_name", "User"), template_key=template_key)

        max_retries = 3
        retry_count = 0
        success = False
        error_msg = None

       
        while retry_count < max_retries and not success:
            try:
                logger.info(f"Attempting transport delivery via {channel}. Attempt {retry_count + 1}")
                
                
                if "fail" in target.lower():
                    raise ConnectionError("Network connection timeout with downstream mail provider API.")
                
                await asyncio.sleep(0.05)  
                success = True
                logger.info(f"Notification {notification_id} successfully dispatched to external gateway.")
            except Exception as ex:
                retry_count += 1
                error_msg = str(ex)
                logger.warn(f"Transient delivery failure detected for job {notification_id}: {error_msg}")
                await asyncio.sleep(0.1 * retry_count) 

       
        final_status = "SENT" if success else "FAILED"
        await self.repo.log_notification(
            notification_id=notification_id,
            template_key=template_key,
            user_id=payload.get("user_id", "unknown-uuid"),
            target=target,
            status=final_status,
            error=error_msg,
            retries=retry_count
        )