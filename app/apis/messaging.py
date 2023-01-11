from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from app.dantic.messaging import MessageDANT
from app.services.MessagingService import MessagingService

router = APIRouter()


@router.post(
    "/messages/",
)
async def send_message(message: MessageDANT, service: MessagingService = Depends(MessagingService)):
    try:
        message = await service.send_message(message.embed, message.channel_id)
    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error while sending message: {exc}"},
        )

    if message:
        return message.to_message_reference_dict()

    return JSONResponse(status_code=500, content={"message": "Error while sending message"})
