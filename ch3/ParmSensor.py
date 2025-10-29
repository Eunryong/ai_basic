import random
import threading
import time
from datetime import datetime
class ParmSensor:

    def __init__(self):
        self.temperature = random.randrange(20, 30)
        self.illuminance = random.randrange(5000, 10000)
        self.humidity = random.randrange(40, 70)

    def setData(self):
        self.temperature = random.randrange(20, 30)
        self.illuminance = random.randrange(5000, 10000)
        self.humidity = random.randrange(40, 70)
    
    def getData(self):
        return self.temperature, self.illuminance, self.humidity

def work(id, parm, stop_event):
    while not stop_event.is_set():
        parm.setData()
        temperature, illuminance, humidity = parm.getData()
        now = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        print(f"{now} Parm-{id} — temp {temperature}, light {illuminance}, humi {humidity}")

        for _ in range(100):
            if stop_event.is_set():
                break
            time.sleep(0.1)

def main():

    sensors = []
    for i in range(1, 6):
        sensors.append(ParmSensor())
    stop_event = threading.Event()

    threads = []
    for i in range(5):
        thread = threading.Thread(target=work, args=(i+1, sensors[i], stop_event))
        thread.daemon = True
        threads.append(thread)

    for thread in threads:
        thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n프로그램 종료 중...")
        stop_event.set()
        
        # 모든 쓰레드가 종료될 때까지 대기
        for thread in threads:
            thread.join(timeout=1)
        
        print("프로그램이 종료되었습니다.")

if __name__ == '__main__':
    main()