from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pika
from django.conf import settings
from .models import Message
from .serializers import MessageSerializer 

class SendMessageView(APIView):
    def get(self, request, format=None):
            try:
                messages = Message.objects.all()
                serializer = MessageSerializer(messages, many=True)
                return Response({'data': serializer.data}, status=status.HTTP_200_OK)
            except Exception as e:
                error_message = str(e)
                return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request, format=None):
        try:
            message_text = request.data.get('text')
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=settings.RABBITMQ_HOST,
                port=settings.RABBITMQ_PORT,
                credentials=pika.PlainCredentials(
                    settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD
                ),
            ))
            channel = connection.channel()
            channel.queue_declare(queue='my_line', durable=True)
            channel.basic_publish(
                exchange='',
                routing_key='my_line',
                body=message_text,
                properties=pika.BasicProperties(
                    delivery_mode=2
                )
            )
            connection.close()
            message = Message(text=message_text)
            message.save()
            serializer = MessageSerializer(message)
            return Response({'message': 'Message sent successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            error_message = str(e)
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
