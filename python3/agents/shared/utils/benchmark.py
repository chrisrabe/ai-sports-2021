from datetime import datetime
from collections import defaultdict


class Benchmark:
    def __init__(self):
        self.cur_tracked = defaultdict(datetime)

    def get_time(self, tracking_id):
        start_time = self.cur_tracked[tracking_id]
        end_time = datetime.now()
        time_diff = (end_time - start_time)
        exec_time = time_diff.total_seconds() * 1000
        return exec_time

    def start(self, tracking_id):
        """
        Start the timer
        """
        self.cur_tracked[tracking_id] = datetime.now()

    def end(self, tracking_id):
        """
        End the timer and print the result
        """
        if tracking_id in self.cur_tracked:
            exec_time = self.get_time(tracking_id)
            print(f'Timer {tracking_id}: Ran for {exec_time}ms')
            del self.cur_tracked[tracking_id]
        else:
            print(f'Error: timer {tracking_id} does not exist')
