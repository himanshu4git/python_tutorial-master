import asyncio
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData

async def run():
    # create a producer client to send messages to the event hub
    # specify connection string to your event hubs namespace and
        # the event hub name
    producer = EventHubProducerClient.from_connection_string(conn_str="Endpoint=sb://python-tutorial-events.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=41MOqZ43oBdoT2s14LaAgOxrSj/LImyLY8v5Bgq0gNI=", eventhub_name="python-event-hub")
    async with producer:
        # create a batch
        event_data_batch = await producer.create_batch()

        # add events to the batch
        event_data_batch.add(EventData('First event '))
        event_data_batch.add(EventData('Second event'))
        event_data_batch.add(EventData('Third event'))

        # send the batch of events to the event hub
        await producer.send_batch(event_data_batch)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
print("Send messages in {} seconds.".format(time.time() - start_time))