from multiprocessing import Pool, Lock
import os, time, random

# 用多进程的想法是错误的，子进程复制了父进程的值，但是读共享，写独立，子进程的程序并没能改变父进程的值
# sum = 0
# def long_time_task(name):
#     print('Run task %s (%s)...' % (name, os.getpid()))
#     start = time.time()
#     time.sleep(random.random() * 3)
#     lock.acquire()
#     global sum
#     print(sum)
#     sum = sum + 1
#     lock.release()
#     end = time.time()
#     print('Task %s runs %0.2f seconds.' % (name, (end - start)))
#
# def poll_init(l):
#     global lock
#     lock = l
#
# if __name__=='__main__':
#     print('Parent process %s.' % os.getpid())
#     lock = Lock()  # 初始化或者叫生成锁
#     p = Pool(4, initializer=poll_init, initargs=(lock,))
#     for i in range(5):
#         p.map(long_time_task, [i])
#     print('Waiting for all subprocesses done...')
#     p.close()
#     p.join()
#     print(sum)
#     print('All subprocesses done.')

import time, threading, multiprocessing

# 假定这是你的银行存款:
balance = 0

def change_it(n):
    # 先存后取，结果应该为0:
    global balance
    balance = balance + n
    balance = balance - n

def run_thread(n, lock):
    for i in range(100000):
        lock.acquire()
        print(n)
        change_it(n)
        lock.release()

# 同步， 互斥，都得有
lock = threading.Lock()
wait_list = []
for i in range(multiprocessing.cpu_count()):
    t1 = threading.Thread(target=run_thread, args=(i,lock,))
    wait_list.append(t1)
    t1.start()

# 等待所有线程执行完毕
for i in wait_list:
    i.join()

print("balance = ", balance)