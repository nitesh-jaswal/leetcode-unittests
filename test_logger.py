import time
from pprint import pprint
import random
from uuid import uuid4
import unittest
from logger import Logger
from typing import Tuple
class TestLogger(unittest.TestCase):
    def setUp(self):
        self.start_time = time.monotonic()
        self.logger = Logger()
        self.base_msg = 'sample_message'
    
    def random_message_generator(self, previous_ts: int) -> Tuple[int, str]:
        is_ts_more_than_10: bool = random.choice((True, False))
        is_unique_message: bool = random.choice((True, False))
        msg = str(uuid4()) if is_unique_message else self.base_msg
        ts_difference = random.randint(1, 9) * 10 if is_ts_more_than_10 else random.randint(1, 9)
        
        return (previous_ts + ts_difference, msg)
    
    def test_shouldPrintMessage_true(self):
        self.assertTrue(
            self.logger.shouldPrintMessage(0, self.base_msg)
        )
        
        previous_timestamp = 0
        num_messages = random.randint(20, 100)
        for _ in range(num_messages):
            previous_timestamp += random.randint(1, 9) * 10
            self.assertTrue(
                self.logger.shouldPrintMessage(previous_timestamp, self.base_msg)
            )


    def test_shouldPrintMessage_false(self):
        self.assertTrue(
            self.logger.shouldPrintMessage(0, self.base_msg)
        )
        
        previous_timestamp = 0
        num_messages = random.randint(4, 9)
        for _ in range(num_messages):
            previous_timestamp += 1
            self.assertFalse(
                self.logger.shouldPrintMessage(previous_timestamp, self.base_msg)
            )
        
    def test_shouldPrintMessage_mixed_random(self):
        num_messages = random.randint(50, 100)
        previous_ts = 0
        previous_sample_ts = None
        msg_list = []
        for _ in range(num_messages):
            msg = self.random_message_generator(previous_ts)
            if msg[1] == self.base_msg:
                flag = True
                if previous_sample_ts is not None:
                    diff = msg[0] - previous_sample_ts
                    if diff < 10:
                        flag = False
                    else:
                        previous_sample_ts = msg[0]
                else:
                    previous_sample_ts = msg[0]
                msg_list.append((flag, msg))
            else:
                msg_list.append((True, msg))
            previous_ts = msg[0]
        
        pprint(msg_list)
        for flag, msg in msg_list:
            try:
                self.assertEqual(flag, self.logger.shouldPrintMessage(*msg))
            except AssertionError:
                print("Assertion error at:", flag, msg)
                assert False
if __name__ == "__main__":
    unittest.main()