import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from .matchmaking import match_maker
from .tournament import tournament_match_maker
import logging

logger = logging.getLogger(__name__)

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            await self.accept()
            self.game = None
            logger.info("User connected via WebSocket")
        except Exception as e:
            logger.error(f"Error during WebSocket connection: {str(e)}")

    async def receive(self, text_data):
        try:
            logger.debug(f"Received data: {text_data}")
            data = json.loads(text_data)
            message_type = data.get('type')

            if message_type == 'authenticate':
                await self.authenticate(data.get('token'))
            elif message_type == 'authenticate2':
                await self.authenticate2(data.get('token_1'), data.get('token_2'))
            elif message_type == 'authenticate3':
                await self.authenticate3(data.get('token'))
            elif message_type == 'key_press':
                if self.game:
                    await self.game.handle_key_press(self, data.get('key'))
                else:
                    await match_maker.handle_key_press(self, data.get('key'))
            else:
                logger.warning(f"Received unknown message type: {message_type}")
                await self.send(text_data=json.dumps({'type': 'error', 'message': 'Unknown message type'}))
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)} - Data received: {text_data}")
            await self.send(text_data=json.dumps({'type': 'error', 'message': 'Invalid JSON format'}))
        except Exception as e:
            logger.error(f"Error in WebSocket receive: {str(e)}")
            await self.send(text_data=json.dumps({'type': 'error', 'message': 'Internal server error'}))

    async def authenticate(self, token):
        if not token:
            logger.error("Token is None, authentication cannot proceed")
            await self.send(text_data=json.dumps({'type': 'error', 'message': 'Token is missing'}))
            return
        try:
            user = await self.get_user_from_token(token)
            if user:
                self.user = user
                await self.send(text_data=json.dumps({'type': 'authenticated'}))
                logger.info(f"User {self.user} authenticated")
                await self.join_waiting_room()
            else:
                logger.warning(f"Authentication failed for token: {token}")
                await self.send(text_data=json.dumps({'type': 'error', 'message': 'Authentication failed'}))
        except Exception as e:
            logger.error(f"Error during authentication: {str(e)}")
            await self.send(text_data=json.dumps({'type': 'error', 'message': 'Internal server error'}))

    async def authenticate2(self, token_1, token_2):
        try:
            user = await self.get_user_from_token(token_1)
            if user:
                self.user = user
                await self.send(text_data=json.dumps({'type': 'authenticated'}))
                logger.info(f"User {self.user} authenticated with token_1")

                user2 = await self.get_user_from_token2(token_2)
                if user2:
                    self.user2 = user2
                    await self.send(text_data=json.dumps({'type': 'authenticated'}))
                    logger.info(f"User {self.user2} authenticated with token_2")
                    await match_maker.create_game(self, None, True)
                else:
                    logger.warning(f"Authentication failed for token_2: {token_2}")
                    await self.send(text_data=json.dumps({'type': 'error', 'message': 'Authentication failed for user 2'}))
            else:
                logger.warning(f"Authentication failed for token_1: {token_1}")
                await self.send(text_data=json.dumps({'type': 'error', 'message': 'Authentication failed for user 1'}))
        except Exception as e:
            logger.error(f"Error during dual authentication: {str(e)}")
            await self.send(text_data=json.dumps({'type': 'error', 'message': 'Internal server error'}))

    async def authenticate3(self, token):
        try:
            user = await self.get_user_from_token(token)
            if user:
                self.user = user
                await self.send(text_data=json.dumps({'type': 'authenticated'}))
                logger.info(f"User {self.user} authenticated for tournament")
                await self.join_tournament_waiting_room()
            else:
                logger.warning(f"Authentication failed for token: {token}")
                await self.send(text_data=json.dumps({'type': 'error', 'message': 'Authentication failed'}))
        except Exception as e:
            logger.error(f"Error during tournament authentication: {str(e)}")
            await self.send(text_data=json.dumps({'type': 'error', 'message': 'Internal server error'}))

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            user = User.objects.filter(auth_token=token).first()
            logger.debug(f"User found: {user} for token: {token}")
            return user
        except User.DoesNotExist:
            logger.warning(f"User not found for token: {token}")
            return None

    @database_sync_to_async
    def get_user_from_token2(self, token):
        try:
            user2 = User.objects.filter(auth_token=token).first()
            logger.debug(f"User2 found: {user2} for token: {token}")
            return user2
        except User.DoesNotExist:
            logger.warning(f"User not found for token_2: {token}")
            return None

    async def join_waiting_room(self):
        logger.info("Joining waiting room")
        await self.send(text_data=json.dumps({'type': 'waiting_room'}))
        await match_maker.add_player(self)

    async def join_tournament_waiting_room(self):
        logger.info("Joining tournament waiting room")
        await tournament_match_maker.add_player(self)

    async def disconnect(self, close_code):
        try:
            if self.game:
                await self.game.end_game(disconnected_player=self)
            await match_maker.remove_player(self)
            await tournament_match_maker.remove_player(self)
            logger.info(f"User {self.user.username if hasattr(self, 'user') else 'Unknown'} disconnected")
        except Exception as e:
            logger.error(f"Error during WebSocket disconnection: {str(e)}")

    async def set_game(self, game):
        logger.info(f"Setting game: {game}")
        self.game = game

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.room_group_name = 'chat'
            self.user = self.scope["user"]
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
            logger.info(f"{self.user.username} connected to chat WebSocket")
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'chat_message',
                'message': f'{self.user.username} has joined the chat'
            })
        except Exception as e:
            logger.error(f"Error during chat WebSocket connection: {str(e)}")

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'chat_message',
                'message': f'{self.user.username} has left the chat'
            })
            logger.info(f"{self.user.username} disconnected from chat WebSocket")
        except Exception as e:
            logger.error(f"Error during chat WebSocket disconnection: {str(e)}")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data['message']
            username = data['username']
            logger.debug(f"Received message from {username}: {message}")
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'chat_message',
                'message': f'{username}: {message}'
            })
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in chat receive: {str(e)} - Data received: {text_data}")
            await self.send(text_data=json.dumps({'type': 'error', 'message': 'Invalid JSON format'}))
        except Exception as e:
            logger.error(f"Error during chat message receive: {str(e)}")
            await self.send(text_data=json.dumps({'type': 'error', 'message': 'Internal server error'}))

    async def chat_message(self, event):
        try:
            message = event['message']
            await self.send(text_data=json.dumps({'message': message}))
            logger.debug(f"Broadcasting chat message: {message}")
        except Exception as e:
            logger.error(f"Error during chat message broadcast: {str(e)}")
