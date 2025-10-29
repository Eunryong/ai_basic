import random
import threading
import time
from datetime import datetime
import pymysql
from dbutils.pooled_db import PooledDB

pool = PooledDB(
    creator=pymysql,
    maxconnections=10,
    mincached=2,
    blocking=True,
    host='127.0.0.1',
    port=3307,
    user='root',
    password='123',
    db='db',
    charset='utf8'
)

class SensorQueue:
    def __init__(self):
        self.queue = []
        self.lock = threading.Lock()
    
    def put(self, item):
        with self.lock:
            self.queue.append(item)
    
    def get(self):
        with self.lock:
            if len(self.queue) > 0:
                return self.queue.pop(0)  # 맨 앞 요소 제거하고 반환
            return None
    
    def is_empty(self):
        with self.lock:
            return len(self.queue) == 0
    
    def size(self):
        with self.lock:
            return len(self.queue)

# 전역 큐 생성
sensorQ = SensorQueue()


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

def insert_sensor_data(now, temperature, illuminance, humidity):
    conn = None
    cur = None
    try:
        # 풀에서 연결 가져오기
        conn = pool.connection()
        cur = conn.cursor()
        
        # 파라미터 바인딩 사용 (SQL Injection 방지)
        sql = """
            INSERT INTO parm_data (입력시간, 온도, 조도, 습도) 
            VALUES (%s, %s, %s, %s)
        """
        cur.execute(sql, (now, temperature, illuminance, humidity))
        conn.commit()
        
    except Exception as e:
        print(f"DB Error: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close() 

def queue_consumer(stop_event):
    """큐에서 데이터를 꺼내서 DB에 저장하는 쓰레드"""
    print("[큐 컨슈머] 시작")
    
    while not stop_event.is_set():
        if not sensorQ.is_empty():
            data = sensorQ.get()
            
            if data is not None:
                now, temperature, illuminance, humidity = data
                
                print(f"[큐에서 꺼냄 - FIFO] {now} - 온도: {temperature}, 조도: {illuminance}, 습도: {humidity}, 남은 큐: {sensorQ.size()}")
                
                insert_sensor_data(now, temperature, illuminance, humidity)
        
        time.sleep(1)
    
    while not sensorQ.is_empty():
        data = sensorQ.get()
        if data is not None:
            now, temperature, illuminance, humidity = data
            insert_sensor_data(now, temperature, illuminance, humidity)


def work(id, parm, stop_event):
    while not stop_event.is_set():
        parm.setData()
        temperature, illuminance, humidity = parm.getData()
        now = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")

        print(f"{now} Parm-{id} — temp {temperature}, light {illuminance}, humi {humidity}")
        
        # insert_sensor_data(now, temperature, illuminance, humidity)

        sensorQ.put((now, temperature, illuminance, humidity))

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

    consumer_thread = threading.Thread(target=queue_consumer, args=(stop_event,))
    consumer_thread.daemon = True
    threads.append(consumer_thread)

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