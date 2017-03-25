import basc_py4chan
import time
import logging
import datetime as datetime

logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ChanMonitor():
    """Monitors 4chan board by continuously polling API

    Overwrite on_status and on_archive to handle thread updates

    Arguments:
        board: string 4chan board to monitor. Ex `pol`
        sleep_per_loop: int number of seconds to sleep after poll of every active
            thread is complete.
        sleep_per_request: int number of seconds to pause between poll. Per 4chan API docs
            recommended wait is at least 1 second.
        stop_timer: int timer in minutes process should run. Process will stop after
            all threads in current loop are updated. Run definitely if set to False
    """

    def __init__(self, board, sleep_per_loop=0, sleep_per_request=1, stop_timer=5):
        self.board = basc_py4chan.board(board)
        self.thread_cache = []
        self.new_threads = []
        self.sleep_per_loop = sleep_per_loop
        self.sleep_per_request = sleep_per_request
        self.stop_timer = datetime.timedelta(minutes=stop_timer)
        self.start = datetime.datetime.utcnow()
        self.loop_start = datetime.datetime.utcnow()

    def on_update(self, thread):
        """Called when thread is updated with new replies"""
        pass

    def on_archive(self, thread):
        """Called when thread is archived"""
        pass

    def _time_expired(self):
        """Check process running longer than specified timer"""
        now = datetime.datetime.utcnow()
        if now - self.start >= self.stop_timer:
            return True
        return False

    def _poll_thread(self, thread):
        """Polls 4chan thread for updates or archival"""
        time.sleep(self.sleep_per_request)
        update = thread.update()

        if update:
            logger.info("{} has {} new updates".format(thread.id, update))
            self.on_update(thread)
        else:
            logger.info("{} no updates".format(thread.id))

        if thread.archived:
            self.thread_cache.remove(thread)
            self.on_archive(thread)

            logger.info("{} has been archived".format(thread.id))

    def _fetch_one(self, thread_id):
        """
        Get a new thread
        :param thread_id: int single id of thread to initiate
        :return: thread object
        """
        time.sleep(self.sleep_per_request)
        thread = self.board.get_thread(thread_id)
        logger.info("Fetching thread ID {}".format(thread_id))
        return thread

    def _fetch_new(self, active_threads):
        """
        Adds new threads to thread cache
        :param active_threads: list of currently active threads
        :return: int number threads added
        """
        active_thread_ids = [t.id for t in self.thread_cache]
        processed = 0
        for thread in active_threads:
            if thread not in active_thread_ids:
                self.thread_cache.append(self._fetch_one(thread))
                logger.info("{} added to thread cache".format(thread))
                processed += 1
        logger.info("Processed {} new threads".format(processed))
        return processed

    def update(self):
        """Cycle through thread_cache polling for updates"""
        for thread in self.thread_cache:
            self._poll_thread(thread)
        logger.info("Active threads {}".format(len(self.thread_cache)))

    def follow(self):
        """
        Build a thread cache of active threads. Loop over threads until they are archived
        Ends on first loop after stop_timer limit is hit. If stop_timer=false follow
        runs indefinitely
        """
        self.start = datetime.datetime.utcnow()
        self.thread_cache = self.board.get_all_threads()
        logger.info("Thread cache initialized {} active threads".format(
            len(self.thread_cache)))
        logger.info("Running for {} minutes".format(self.stop_timer))
        active_threads = self.board.get_all_thread_ids()

        while not self._time_expired() and self.stop_timer:
            self.loop_start = datetime.datetime.utcnow()
            self._fetch_new(active_threads)
            self.update()
            logger.info("Thread cache loop complete time elapsed: {}".format(
                datetime.datetime.utcnow() - self.loop_start))

            time.sleep(self.sleep_per_loop)
            logging.info("Sleeping {} seconds before restart".format(
                self.sleep_per_loop))

        end = datetime.datetime.utcnow()
        elapsed = end - self.start
        logger.info("Stopping /{} collection".format(self.board.name.upper()))
        logger.info("Time Elapsed {}".format(elapsed))

        return
