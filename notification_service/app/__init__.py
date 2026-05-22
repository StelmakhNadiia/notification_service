import asyncio
from fastapi import FastAPI
from app.controllers.http_routes import router as http_router
from app.controllers.broker_consumer import RabbitMQEventConsumer
from app.services.logger import logger

def create_app() -> FastAPI:
    app = FastAPI(title="Notification Service Core", version="1.0.0")
    
    
    app.include_router(http_router)
    
    @app.on_event("startup")
    async def startup_event():
        logger.info("Initializing Notification Service Microservice infrastructure components...")
        
        
        try:
            consumer = RabbitMQEventConsumer()
            asyncio.create_task(consumer.start_consuming())
            logger.info("Event-driven Message Broker Consumer successfully mounted into lifecycle event loop.")
        except Exception as e:
            logger.error(f"Failed to establish non-blocking connection to RabbitMQ: {str(e)}. Running in HTTP-only state.")

    return app