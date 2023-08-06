# PyAMQP

Python interface for simple usage of AMQP middleware applications.

This interface is made to ease the process of using AMQP software.

The applications supported so far:

* RabbitMQ: This is a popular open-source message-broker that implemented 
            the Advanced Message Queuing Protocol (AMQP) written in the Erlang programming language
            
# How to get it
``pip install pyamqp``

# Dependencies
Pika: 0.13 or higher

pytest: 4.0.2 or higher

# Usage example
 ## RabbitMQ - Receiver
```python    
from pyamqp.rabbit.receiver import Receiver

# Initializing and creating the connection with the Rabbit server
receiver_instance = Receiver(host='18.222.222.222',
                             port=5672,
                             user='guest',
                             password='1245554221')
                             
# Declares the queue with the specified parameters, 
# binds it to an exchange using the routing_keys list.
receiver_instance.connect_queue(queue_name='test',
                                exchange='test_exchange',
                                routing_keys=['A', 'B'],
                                is_durable=True,
                                auto_delete=False)
# callback function
# Not necesary if inheritance is used
def get_message(message, details):
    some_value = message.get('some_key', None)
    print(some_value)
    
receiver_instance.consume(callback_function=get_message,
                          no_ack=True,
                          consumer_tag='AAAAKKK_2232')
```
## Rabbit-Dispatcher
```python
from pyamqp.rabbit.dispatcher import Dispatcher

dispatcher_instance = Dispatcher(host='18.222.222.222',
                                 port=5672,
                                 user='guest',
                                 password='1245554221')
                                 
# Declaring exchanges that are going to be used for sending messages
# exchanges parameter can be an string or a list of strings                               
dispatcher_instance.connect_exchanges(exchanges=['test_exch', 'test_exch_2],
                                      exchange_type='topic',
                                      auto_delete=True)
                                      
                                      
# There can be only two types of passed messages, string or dicts.
message_1 = 'Hello'
message_2 = {'Ciao': 'Hola'} 

dispatcher.send_message(message_1, 'THIS.IS.A.KEY', 'test_exch')
dispatcher.send_message(message_2, 'KEY.SOMETHING', 'test_exch_2')
```

# Current limitations

*  There's only support for BlockingConnection adapter since this is the main adapter used in production.
*  Threaded Receiver class is not thread-safe, will be added using an internal instance of Queue() to address that issue.
*  This packages does not support the inheritance of Receiver and Dispatcher in the same child class.

# License

GNU GPLv3

Permissions of this strong copyleft license are conditioned on making available complete source code of licensed works and modifications, which include larger works using a licensed work, under the same license. Copyright and license notices must be preserved. Contributors provide an express grant of patent rights.

