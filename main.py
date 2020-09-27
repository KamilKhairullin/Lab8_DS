from multiprocessing import Process, Pipe
from datetime import datetime
from time import sleep

def print_local_time():
    return "LOCAL TIME IS " + str(datetime.now())

def internal_event(pid, logical_clock):
    logical_clock[pid - 1] += 1
    print("Internal Event in process ", pid, print_local_time())
    return logical_clock

def send_message(pipe, pid, logical_clock):
    logical_clock[pid - 1] += 1
    pipe.send(logical_clock)
    print("Process " + str(pid) + " sent a message. Its logical clock is ", str(logical_clock), print_local_time())
    return logical_clock

def receive_message(pipe, pid, logical_clock):
    recv_clock = pipe.recv()

    for i in range(3):
        logical_clock[i] = max(recv_clock[i], logical_clock[i])

    logical_clock[pid - 1] += 1
    print("Process " + str(pid) + " received a message. Its logical clock is ", str(logical_clock), print_local_time())
    return logical_clock

def process_a(a_to_b):
    pid = 1
    clock = [0, 0, 0]
    clock = send_message(a_to_b, pid, clock)
    clock = send_message(a_to_b, pid, clock)
    clock = internal_event(pid, clock)
    clock = receive_message(a_to_b, pid, clock)
    clock = internal_event(pid, clock)
    clock = internal_event(pid, clock)
    clock = receive_message(a_to_b, pid, clock)
    sleep(1) #sleep to sort output
    print("A" + str(clock))

def process_b(b_to_a, b_to_c):
    pid = 2
    clock = [0, 0, 0]
    clock = receive_message(b_to_a, pid, clock)
    clock = receive_message(b_to_a, pid, clock)
    clock = send_message(b_to_a, pid, clock)
    clock = receive_message(b_to_c, pid, clock)
    clock = internal_event(pid, clock)
    clock = send_message(b_to_a, pid, clock)
    clock = send_message(b_to_c, pid, clock)
    clock = send_message(b_to_c, pid, clock)
    sleep(2) #sleep to sort output
    print("B" + str(clock))

def process_c(c_to_b):
    pid = 3
    clock = [0, 0, 0]
    clock = send_message(c_to_b, pid, clock)
    clock = receive_message(c_to_b, pid, clock)
    clock = internal_event(pid, clock)
    clock = receive_message(c_to_b, pid, clock)
    sleep(3) #sleep to sort output
    print("С" + str(clock))

if __name__ == '__main__':
    a_to_b, b_to_a = Pipe()
    b_to_c, c_to_b = Pipe()

    a = Process(target=process_a, args=(a_to_b,))
    b = Process(target=process_b, args=(b_to_a,b_to_c,))
    c = Process(target=process_c, args=(c_to_b,))
    a.start()
    b.start()
    c.start()

    a.join()
    b.join()
    c.join()
