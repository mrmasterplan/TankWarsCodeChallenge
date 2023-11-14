import time

class CountDownTimer:
    def __init__(self, countdownsecs):
        self.end_time = time.time() + countdownsecs

    def get_countdown_reached_and_timer_string(self):
        # Calculate the time left
        time_left = int(max(0, self.end_time - time.time()))
        minutes = time_left // 60
        seconds = time_left % 60
        return time_left == 0, f"{minutes:02}:{seconds:02}"

    
