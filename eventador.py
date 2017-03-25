import os
import json
import logging
from sqlalchemy import Column, Table, Integer, MetaData, create_engine
from sqlalchemy.dialects import postgresql

from chan_monitor import ChanMonitor
from kafka import KafkaProducer
import utils

logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Eventador kafka config
KAFKA_TOPIC = 'info_source_testing'
KAFKA_BROKERS = os.getenv("KAFKA_BROKERS")

# Setup producer connection
producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                         bootstrap_servers=KAFKA_BROKERS)

logger.info("connected to {} topic {}".format(KAFKA_BROKERS, KAFKA_TOPIC))


def setup_db():
    db = create_engine('postgresql://admin:slowmo@localhost:5432/postgres')
    metadata = MetaData(db)
    data_table = Table(
            'fourchan2',
            metadata,
            Column('id', Integer, primary_key=True),
            Column('parent', Integer),
            Column('chan_id', Integer, unique=True),
            Column('created_at', postgresql.TIMESTAMP),
            Column('content', postgresql.JSONB)
    )
    return db, data_table


def sendto_eventador(payload):
    """Add a message to the produce buffer asynchronously to be sent to Eventador."""
    try:
        producer.send(KAFKA_TOPIC, payload)
    except Exception as e:
        logging.warning("Unable to produce to {} topic {}".format(
            KAFKA_BROKERS, KAFKA_TOPIC))
        logging.warning(e)


class EventadorChanMonitor(ChanMonitor):
    def __init__(self, board, sleep_per_loop=0, sleep_per_request=1, stop_timer=55):
        super(EventadorChanMonitor, self).__init__(
                board,
                sleep_per_loop=sleep_per_loop,
                sleep_per_request=sleep_per_request,
                stop_timer=stop_timer)
        self.previously_sent = {}
        self.producer = producer
        self.db, self.data_table = setup_db()
        self.msg_counter = 0

    def _transform_dict(self, post, thread_id, final=False):
        reply = post
        reply = reply.__dict__['_data']

        if final:
            reply['feed'] = 'final'
        else:
            reply['feed'] = 'stream'
        reply['thread_no'] = thread_id
        reply['source'] = 'fourchan'
        reply['project'] = 'state_test'

        return reply

    def on_update(self, thread):
        post_list = [p.post_id for p in thread.posts]
        if str(thread.id) in self.previously_sent:
            logging.info("Previously sent thread {}")
            prev_sent = 0
            new_sent = 0
            for reply in thread.posts:
                if reply.post_id not in self.previously_sent[str(thread.id)]:
                    message = self._transform_dict(reply, thread.id)
                    sendto_eventador(message)
                    self.msg_counter += 1
                    new_sent += 1
                else:
                    prev_sent += 1
            logger.info("{} sent {} replies {} previously sent".format(thread.id, new_sent, prev_sent))

        else:
            for reply in thread.posts:
                message = self._transform_dict(reply, thread.id)
                sendto_eventador(message)
                self.msg_counter += 1
            logger.info('New thread {} posted to eventador'.format(thread.id))
        self.previously_sent[str(thread.id)] = post_list

    def on_archive(self, thread):
        for reply in thread.posts:
            message = self._transform_dict(reply, thread.id, final=True)
            sendto_eventador(message)
            self.msg_counter += 1
        logger.info("{} archive sent to eventador".format(thread.id))
        utils.archive_thread(thread, self.db, self.data_table)

        if str(thread.id) in self.previously_sent:
            del self.previously_sent[str(thread.id)]
            logger.info("Removed {} from previously sent".format(thread.id))

    def on_loop_complete(self):
        producer.flush()
        state_file = 'state.json'
        with open('state.json', 'w') as f:
            json.dump(self.previously_sent, f, indent=0)
        logger.info("Loop complete state saved {} with {} threads".format(
                state_file, len(self.previously_sent)))
        logger.info("Message count: {}".format(self.msg_counter))

    def on_start(self):
        try:
            with open('state.json', 'r') as f:
                state = json.load(f)
            self.previously_sent = state


if __name__ == '__main__':
    chan = EventadorChanMonitor(board='pol', sleep_per_request=.25, stop_timer=False)
    chan.follow()
