import GoodClock
import time

Clock = GoodClock.GoodClock()

Clock.run()



time.sleep(1)

print('Time: ' + str(Clock.now().strftime("%f")))



