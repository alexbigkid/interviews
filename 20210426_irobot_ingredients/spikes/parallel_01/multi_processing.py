import time
import multiprocessing


def calc_square(numbers):
    for i in numbers:
        time.sleep(3)  # artificial time-delay
        print('square: ', str(i * i))


def calc_cube(numbers):
    for i in numbers:
        time.sleep(3)
        print('cube: ', str(i * i * i))


def main():
    arr = [2, 3, 8, 9]
    p1 = multiprocessing.Process(target=calc_square, args=(arr,))
    p2 = multiprocessing.Process(target=calc_cube, args=(arr,))
    start_time = time.time()
    epoch_time = int(time.time())
    print('epoch time start: %s' % epoch_time)

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    end_time = time.time()
    print("Successes in -- %s  seconds --" % (end_time - start_time))
    epoch_time = int(time.time())
    print('epoch time end: %s' % epoch_time)


if __name__ == "__main__":
    main()
