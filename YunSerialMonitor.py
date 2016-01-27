from threading import Thread

__author__ = 'Leenix'

import logging
import sys

import serial
from serial import SerialException


class SerialMonitor:
    def __init__(self, port, baud_rate, logger_name=__name__, logger_level=logging.DEBUG):
        self.port = port
        self.baud_rate = baud_rate
        self.ser = serial.Serial()

        self.logger = logging.getLogger(logger_name)
        if self.logger.name == __name__:
            self.logger.addHandler(logging.StreamHandler())
            self.logger.setLevel(logger_level)

        self.is_reading = False
        self.read_thread = Thread(name="read_thread", target=self._read_loop)

        self.is_writing = False
        # self.write_thread = Thread(name="write_thread", target=self._write_loop)

    def run(self):
        """
        Start the read loop for Serial input.

        :return: None
        """

        try:
            self.logger.debug("Opening serial port [{}] with {} baud".format(self.port, self.baud_rate))
            self.ser.setBaudrate(self.baud_rate)
            self.ser.setPort(self.port)
            self.ser.setTimeout(1)
            self.ser.open()

            self.ser.flushOutput()
            self.ser.flushInput()

        except SerialException:
            self.logger.error("Serial port [{}] cannot be opened :(".format(self.port))
            input("Hit 'Enter' to close...")
            sys.exit()

        self.read_thread.start()
        self.is_reading = True

        # self.write_thread.start()
        self.is_writing = True

    def stop(self):
        """
            Shut down the serial monitor
            :return:
            """
        self.logger.info("Stopping serial comms")
        self.is_writing = False
        self.is_reading = False
        self.ser.close()
        sys.exit()

    def _read_loop(self):
        """
            Print received characters to the console
            :return:
            """
        while self.is_reading:
            try:
                c = self.ser.readline()
                if c:
                    print c
            except Exception, e:
                continue

    def _write_loop(self):
        """
            Write console characters across to the serial link
            :return:
            """
        while self.is_writing:
            c = sys.stdin.read()
            self.ser.write(c)


if __name__ == '__main__':
    logger = logging.getLogger("YunSerial")
    logger.setLevel(logging.DEBUG)

    monitor = SerialMonitor("/dev/ttyATH0", 115200, logger_level=logging.DEBUG)
    monitor.run()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        monitor.stop()
