import json
import asyncio
import aiormq
from app.config import settings
from app.services.logger import logger, trace_id_ctx
from app.services.notification_manager import NotificationManager

class RabbitMQEventConsumer:
    def __init__(self):
        self.manager = NotificationManager()
        self.connection = None
        self.channel = None

    async def start_consuming(self):
        self.connection = await aiormq.connect(settings.RABBITMQ_URL)
        self.channel = await self.connection.channel()
        

        queues = [
            "user.events.registered",
            "payment.events.succeeded",
            "progress.events.course_completed"
        ]
        
        for queue_name in queues:
            await self.channel.queue_declare(queue=queue_name, durable=True)
            await self.channel.basic_consume(queue_name, self._on_message_callback)
            logger.info(f"Successfully subscribed to message broker channel: {queue_name}")

    async def _on_message_callback(self, message):
        try:
            raw_body = message.body.decode()
            event_data = json.loads(raw_body)
            
           
            extracted_trace = event_data.get("trace_id", "internal-gen-uuid")
            trace_id_ctx.set(extracted_trace)
            
            routing_key = message.routing_key if hasattr(message, 'routing_key') else "unknown.event"
            logger.info(f"Event received via broker backbone. Context routing: {routing_key}")
            
           
            template_key = "lesson_reminder"
            target_recipient = event_data.get("email", "mock@user.com")
            transport_channel = "EMAIL"
            
            if "registered" in routing_key:
                template_key = "payment_success"  
            elif "succeeded" in routing_key:
                template_key = "payment_success"  
            elif "completed" in routing_key:
                template_key = "course_completed"  
                transport_channel = "PUSH"
                target_recipient = "token_firebase_device_123"

           
            await self.manager.send_transactional_notification(
                template_key=template_key,
                payload=event_data,
                target=target_recipient,
                channel=transport_channel
            )
            
           
            await self.channel.basic_ack(delivery_tag=message.delivery_tag)
            
        except Exception as ex:
            logger.error(f"Critical error during broker inbound message pipeline execution: {str(ex)}")
            await self.channel.basic_nack(delivery_tag=message.delivery_tag, requeue=True)