from CyberGlove import CyberGlove
import time

s = CyberGlove();
s.stream()
time.sleep(3)
s.stop_stream()
s.read_all()
s.StopCG()
