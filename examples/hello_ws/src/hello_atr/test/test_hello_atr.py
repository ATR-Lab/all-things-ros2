"""Tests for hello_atr. Run them with `colcon test --packages-select hello_atr`."""

import time

import pytest
import rclpy
from rclpy.executors import SingleThreadedExecutor
from rclpy.parameter import Parameter
from std_msgs.msg import String

from hello_atr.listener import Listener
from hello_atr.talker import format_message, Talker


def test_format_message():
    # A plain unit test: no ROS graph needed.
    assert format_message('Hello', 3) == 'Hello #3'


@pytest.fixture
def context():
    # A private context keeps this test independent of any other ROS 2 code in the process.
    ctx = rclpy.Context()
    ctx.init()
    yield ctx
    ctx.try_shutdown()


def test_talker_rejects_bad_rate(context):
    with pytest.raises(ValueError):
        Talker(
            context=context,
            parameter_overrides=[Parameter('publish_rate_hz', value=0.0)])


def test_listener_hears_talker(context):
    # An integration test: two nodes, one process, one executor.
    talker = Talker(
        context=context,
        parameter_overrides=[
            Parameter('greeting', value='Test greeting'),
            Parameter('publish_rate_hz', value=20.0),
        ])
    listener = Listener(context=context)
    heard = []
    # A second subscription on the listener node records what arrives, so the test can check it.
    listener.create_subscription(String, 'chatter', lambda msg: heard.append(msg.data), 10)

    executor = SingleThreadedExecutor(context=context)
    executor.add_node(talker)
    executor.add_node(listener)
    try:
        deadline = time.monotonic() + 10.0
        while not heard and time.monotonic() < deadline:
            executor.spin_once(timeout_sec=0.1)
    finally:
        executor.shutdown()
        talker.destroy_node()
        listener.destroy_node()

    assert heard, 'the listener received nothing within 10 seconds'
    assert heard[0].startswith('Test greeting #')
    assert listener.received >= 1
