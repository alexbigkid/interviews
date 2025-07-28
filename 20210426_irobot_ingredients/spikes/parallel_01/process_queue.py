import multiprocessing

results = []   #Creating a Global Variable

def calc_square(numbers, q):   #child-function
    global results
    for i in numbers:
        q.put(i*i)
        print('square: ', str(i*i))
        results.append(i*i)
        print('inside process : '+str(results))


def main():
    arr = [2,3,8,9]
    q = multiprocessing.Queue()
    p1 = multiprocessing.Process(target = calc_square,args=(arr, q))
    p1.start()
    p1.join()
    while q.empty() is False:
        print(q.get())


if __name__ == "__main__":   #main function
    main()
