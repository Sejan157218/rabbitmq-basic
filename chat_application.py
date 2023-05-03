import pika

# Establish a connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare an exchange and a queue
channel.exchange_declare(exchange='chat_exchange', exchange_type='topic')
channel.queue_declare(queue='chat_queue', durable=True)

# Bind the queue to the exchange
channel.queue_bind(exchange='chat_exchange', queue='chat_queue', routing_key='chat.message')

# Publish a message to the exchange
channel.basic_publish(exchange='chat_exchange', routing_key='chat.message', body='Hello, World!')

# Consume messages from the queue
def callback(ch, method, properties, body):
    print("Received message:", body.decode())

channel.basic_consume(queue='chat_queue', on_message_callback=callback, auto_ack=True)

# Start consuming messages
channel.start_consuming()