import pika, sys, os

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    while True:
        channel = connection.channel()

        channel.queue_declare(queue='hello')
        channel.queue_declare(queue='hello-return')

        def callback(ch, method, properties, body):
            print(" [x] Received %r" % body)

        channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

        channel.start_consuming()
        print(" [x] Sent 'Hello World!'")
        user_input = input("Enter something: ")
        channel.basic_publish(exchange='', routing_key='hello-return', body=user_input)
        if user_input == "quit":
            break
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)