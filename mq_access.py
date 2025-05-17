import pika


def get_current_datetime():
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def send_message_to_queue(message, queue_name='hello'):
    # Establish a connection to RabbitMQ server
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Declare a queue
        channel.queue_declare(queue=queue_name, durable=True)

        # Publish the message to the queue
        channel.basic_publish(exchange='',
                            routing_key=queue_name,
                            body=f"{get_current_datetime()} {message}",
                            properties=pika.BasicProperties(
                                delivery_mode=2,  # Make message persistent
                            ))

        # Close the connection
        connection.close()
    except pika.exceptions.AMQPConnectionError as e:
        return f"Failed to connect to RabbitMQ server: {e}"


def get_all_messages_from_queue(queue_name='hello'):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)

        messages = []
        while True:
            method_frame, header_frame, body = channel.basic_get(queue=queue_name, auto_ack=True)
            if method_frame:
                messages.append(body.decode())
            else:
                break

        connection.close()
        return messages

    except pika.exceptions.AMQPConnectionError as e:
        return f"Failed to connect to RabbitMQ server: {e}"
        