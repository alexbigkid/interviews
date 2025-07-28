"""Main program for experimenting with multi threading"""

import time
import threading


def calc_square(numbers):
    print("Calculate square numbers: ")
    for i in numbers:
        time.sleep(2)  # artificial time-delay
        print(str(i), ' power of 2: ', str(i * i))


def calc_cube(numbers):
    print("Calculate cube numbers: ")
    for i in numbers:
        time.sleep(3)
        print(str(i), ' power of 3: ', str(i * i * i))


def main():
    arr = [2, 3, 8, 9]
    t1 = threading.Thread(target=calc_square, args=(arr,))
    t2 = threading.Thread(target=calc_cube, args=(arr,))
    start_time = time.time()
    epoch_time = int(time.time())
    print('epoch time start: %s' % epoch_time)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
    end_time = time.time()
    print("Successes in -- %s  seconds --" % (end_time - start_time))
    epoch_time = int(time.time())
    print('epoch time end: %s' % epoch_time)


if __name__ == "__main__":
    main()
