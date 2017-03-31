import datetime
import pytest
from smtk.fourchan import ChanMonitor


@pytest.fixture
def monitor():
    monitor = ChanMonitor('fixture', sleep_per_request=0)
    return monitor


def test_chan_monitor_defaults():
    chan = ChanMonitor('test')

    assert chan.board.name == 'test'
    assert chan.sleep_per_loop == 0
    assert chan.sleep_per_request == 1
    assert chan.stop_timer == datetime.timedelta(0, 300)


def test_chan_monitor_pass_args():
    chan = ChanMonitor(
        'param_test',
        sleep_per_loop=60,
        sleep_per_request=11,
        stop_timer=10
    )

    assert chan.board.name == 'param_test'
    assert chan.sleep_per_loop == 60
    assert chan.sleep_per_request == 11
    assert chan.stop_timer == datetime.timedelta(0, 600)


def test_monitor_time_expired(monitor):
    monitor.start = datetime.datetime(2017, 1, 1)
    assert monitor._time_expired() is True


def test_monitor_time_not_expired(monitor):
    monitor.start = datetime.datetime(2050, 1, 1)
    assert monitor._time_expired() is False
