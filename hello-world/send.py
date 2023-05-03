import pika


while True:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.queue_declare(queue='hello-return')
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
    channel.start_consuming()
    channel.basic_consume(queue='hello-return', on_message_callback=callback, auto_ack=True)


        
    print(" [x] Sent 'Hello World!'")
    user_input = input("Enter something: ")
    channel.basic_publish(exchange='', routing_key='hello', body=user_input)
    if user_input == "quit":
        break

