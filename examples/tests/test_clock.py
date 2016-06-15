import os
import socket

from testtools.testcase import TestCase

from daemonfixture.daemon import DaemonFixture

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
TWISTD_BIN = os.path.join(ROOT_DIR, "env", "bin", "twistd")
CLOCK_COMMAND = (TWISTD_BIN, "-n", "web", "--class", "examples.clock.Root")


class ClockExampleTest(TestCase):

    def setUp(self):
        super(ClockExampleTest, self).setUp()
        self.useFixture(DaemonFixture(CLOCK_COMMAND, is_ready=is_ready))
        self.driver = webdriver.PhantomJS()
        self.addCleanup(self.driver.quit)

    def test_event_source(self):
        """
        Test that notifications are correctly delivered.
        """
        self.driver.get("http://localhost:8080")
        self.assertEqual("SSE Clock", self.driver.title)
        time = self.driver.find_element_by_id("time")
        current = int(time.text)
        wait = WebDriverWait(self.driver, 3)
        wait.until(lambda _: int(time.text) > current)


def is_ready():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return sock.connect_ex(("127.0.0.1", 8080)) == 0
