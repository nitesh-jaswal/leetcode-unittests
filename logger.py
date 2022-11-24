from collections import deque

class Logger(object):

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self._msg_set = set()
        self._msg_queue = deque()
    
    def shouldPrintMessage(self, timestamp, message):
        """
        Returns true if the message should be printed in the given timestamp, otherwise returns false.
        """
        # Uncomment for debugging
        # print("TS:", timestamp, "MSG:", message, "SET:", self._msg_set, "Q:", self._msg_queue)
        while self._msg_queue:
            msg, ts = self._msg_queue[0]
            if timestamp - ts >= 10:
                self._msg_queue.popleft()
                self._msg_set.remove(msg)
            else:
                break
        
        if message not in self._msg_set:
            self._msg_set.add(message)
            self._msg_queue.append((message, timestamp))
            return True
        else:
            return False

if __name__ == "__main__":

        import random
        from uuid import uuid4
        from typing import Tuple

        def random_message_generator(previous_ts: int) -> Tuple[int, str]:
            is_ts_more_than_10: bool = random.choice((True, False))
            is_unique_message: bool = random.choice((True, False))
            msg = str(uuid4()) if is_unique_message else "sample_msg"
            ts_difference = random.randint(1, 9) * 10 if is_ts_more_than_10 else random.randint(0, 9)
            
            return (previous_ts + ts_difference, msg)
        
        num_messages = random.randint(50, 100)
        previous_ts = 0
        previous_sample_ts = None
        msg_list = []
        for _ in range(num_messages):
            msg = random_message_generator(previous_ts)
            if msg[1] == "sample_msg":
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
        
        print("MSG LIST:", msg_list)
        print()
        print("MSGS NOT TO BE PRINTED:", [msg for msg in msg_list if not msg[0]])