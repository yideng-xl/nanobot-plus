"""Feishu/Lark channel implementation using lark-oapi."""

import asyncio
import json
from loguru import logger
import lark_oapi as lark
from lark_oapi.api.im.v1 import *

from nanobot.bus.events import OutboundMessage
from nanobot.bus.queue import MessageBus
from nanobot.channels.base import BaseChannel
from nanobot.config.schema import FeishuConfig


class FeishuChannel(BaseChannel):
    """
    Feishu/Lark channel using Long Connection (WebSocket).
    
    Reliable and works behind NAT/firewalls without a public IP.
    """
    
    name = "feishu"
    
    def __init__(self, config: FeishuConfig, bus: MessageBus):
        super().__init__(config, bus)
        self.config: FeishuConfig = config
        self._client: lark.Client | None = None
        self._ws_client: lark.ws.Client | None = None
        self._loop: asyncio.AbstractEventLoop | None = None

    async def start(self) -> None:
        """Start the Feishu channel with long connection."""
        self._loop = asyncio.get_running_loop()
        if not self.config.app_id or not self.config.app_secret:
            logger.error("Feishu app_id or app_secret not configured")
            return
        
        self._running = True
        
        # Build API client
        self._client = lark.Client.builder() \
            .app_id(self.config.app_id) \
            .app_secret(self.config.app_secret) \
            .log_level(lark.LogLevel.INFO) \
            .build()
            
        # Build event handler
        event_handler = lark.EventDispatcherHandler.builder("", "") \
            .register_p2_im_message_receive_v1(self._on_message) \
            .build()
            
        # Build WebSocket client
        self._ws_client = lark.ws.Client(
            self.config.app_id,
            self.config.app_secret,
            event_handler=event_handler,
            log_level=lark.LogLevel.INFO
        )
        
        logger.info("Starting Feishu channel (long connection)...")
        
        # Start in a separate thread since lark-oapi's WS client is blocking
        # But wait, lark-oapi has an async version? Actually, most use the threaded one.
        # Let's run it in an executor.
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self._ws_client.start)
        
    async def stop(self) -> None:
        """Stop the Feishu channel."""
        self._running = False
        if self._ws_client:
            # Note: lark-oapi ws client stop might be tricky if blocking
            # but usually it handles signals.
            pass
            
    async def send(self, msg: OutboundMessage) -> None:
        """Send a message through Feishu."""
        if not self._client:
            logger.warning("Feishu client not running")
            return
            
        try:
            # Determine receiver type (open_id or chat_id)
            receive_id_type = "open_id"
            if msg.chat_id.startswith("oc_"):
                receive_id_type = "chat_id"
                
            # Create request
            content = json.dumps({"text": msg.content})
            request: CreateMessageRequest = CreateMessageRequest.builder() \
                .receive_id_type(receive_id_type) \
                .request_body(CreateMessageRequestBody.builder() \
                    .receive_id(msg.chat_id) \
                    .msg_type("text") \
                    .content(content) \
                    .build()) \
                .build()
                
            # Send request
            response: CreateMessageResponse = await asyncio.get_running_loop().run_in_executor(
                None, 
                lambda: self._client.im.v1.message.create(request)
            )
            
            if not response.success():
                logger.error(f"Feishu send failed: {response.code} {response.msg}")
                
        except Exception as e:
            logger.error(f"Error sending Feishu message: {e}")
            
    def _on_message(self, data: P2ImMessageReceiveV1) -> None:
        """Handle incoming message event."""
        logger.debug(f"Received Feishu event: {data}")
        message = data.event.message
        sender = data.event.sender
        
        # Determine sender_id and chat_id
        # For DMs, chat_id can be the open_id or the actual chat_id
        sender_id = sender.sender_id.open_id
        chat_id = message.chat_id
        
        # Get content
        content_json = json.loads(message.content)
        content = content_json.get("text", "")
        
        logger.debug(f"Feishu message from {sender_id}: {content[:50]}...")
        
        # Forward to the bus (need to run in loop)
        if self._loop:
            asyncio.run_coroutine_threadsafe(
                self._handle_message(
                    sender_id=sender_id,
                    chat_id=chat_id,
                    content=content,
                    metadata={
                        "message_id": message.message_id,
                        "sender_type": sender.sender_type,
                        "chat_type": message.chat_type
                    }
                ),
                self._loop
            )
