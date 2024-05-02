import time
from queue import Queue
import matplotlib.pyplot as plt

class Process:
    def __init__(self, id, burst_time):
        self.id = id
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.state = 'Ready'  # 프로세스의 초기 상태

    def run(self):
        if self.remaining_time > 0:
            self.state = 'Running'  # 프로세스가 실행 중임
            self.remaining_time -= 1
        if self.remaining_time == 0:
            self.state = 'Completed'  # 프로세스가 실행 완료됨

class RoundRobinScheduler:
    def __init__(self, quantum):
        self.quantum = quantum
        self.process_queue = Queue()
        self.current_process = None

    def add_process(self, process):
        self.process_queue.put(process)

    def schedule(self):
        if self.current_process is None or self.current_process.remaining_time == 0:
            if not self.process_queue.empty():
                self.current_process = self.process_queue.get()
        return self.current_process

def main_loop():
    processes = [Process(i, 5) for i in range(5)] # 프로세스 5개 생성
    scheduler = RoundRobinScheduler(quantum = 1)
    time_steps = []
    states = {p.id: [] for p in processes}  # 각 프로세스의 상태 기록

    for proc in processes:
        scheduler.add_process(proc)

    step = 0
    while not scheduler.process_queue.empty():
        current_process = scheduler.schedule()
        if current_process is not None:
            current_process.run()
            if current_process.remaining_time > 0:
                scheduler.add_process(current_process)
        # 프로세스 상태 데이터 수집
        time_steps.append(step)
        for p in processes:
            states[p.id].append(p.state)
        step += 1
        time.sleep(0.1)  

    # 상태 시각화
    state_values = {'Ready': 1, 'Running': 2, 'Completed': 3}  # 상태를 숫자로 매핑
    plt.figure(figsize=(12, 6))
    for pid, state_list in states.items():
        numeric_states = [state_values[s] for s in state_list]
        plt.plot(time_steps, numeric_states, label = f'Process {pid}')
    plt.yticks([1, 2, 3], ['Ready', 'Running', 'Completed'])
    plt.xlabel('Time Step')
    plt.ylabel('State')
    plt.title('Round Robin Scheduling Process')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main_loop()
