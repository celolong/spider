# coding=utf-8
"""
author:cello
"""
from queue import Queue
from threading import Thread
import time


class xianchen(object):
    def __init__(self):
        self.queue = Queue()
        self.queue1 = Queue()

    def get_data(self):
        while True:
            num  = self.queue.get()
            print('get',num)
            # time.sleep(1)
            self.queue.task_done()

    def put_data1(self):
        global num
        while num<10:
            self.queue.put(num)
            num +=1
            print('put',num)


    def get_data1(self):
        while True:
            tt  = self.queue1.get()
            time.sleep(5)
            print('get', tt)
            self.queue1.task_done()

    def put_data(self):
        global tt
        while tt<20:
            time.sleep(2)
            self.queue1.put(tt)
            tt +=1
            print('put',tt)


    def run(self):
        # 创建进程池
        thread_list = []
        # put线程
        for t in range(3):
            t = Thread(target=self.put_data)
            thread_list.append(t)
        # get线程
        for t in range(3):
            t = Thread(target=self.get_data)
            thread_list.append(t)

        # # put线程
        # for t in range(3):
        #     t = Thread(target=self.put_data1)
        #     thread_list.append(t)
        # # get线程
        # for t in range(3):
        #     t = Thread(target=self.get_data1)
        #     thread_list.append(t)
        # 创建守护线程
        for t in thread_list:
            t.setDaemon(True)
            t.start()
        for q in [self.queue,self.queue1]:
            q.join()
        print('over')

if __name__ == "__main__":
    num = 0
    tt = 10
    p = xianchen()
    p.run()

