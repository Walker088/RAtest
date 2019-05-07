#!/usr/bin/env python
import requests, time, random, csv
from tqdm import tqdm
from prettytable import PrettyTable
from multiprocessing import Pool

url_saa = 'http://190.52.167.69:9000/'
api_saa = 'SOAP/get_expediente.php?cedula=%d'

url_his = 'http://192.168.1.43:5000/'
api_his = 'api/v1/policia/%d'

max_num = 8500000
min_num = 8500

def query(id, url=url_his, api=api_his):
    url = url + api
    res = requests.get(url %(id))
    return res

def writeRes(lrLst, trLst):
    with open('latency.csv', 'w', newline='') as lrCsv:
        writer = csv.writer(lrCsv)
        writer.writerow(['number_of_requests', 'latency'])
        for nor in range(len(lrLst)):
            writer.writerow([10**(nor+1), lrLst[nor]])
        for nt in range(len(trLst)):
            writer.writerow([nt+1, trLst[nt]])

def printRes(lrLst, trLst):
    lrTb = PrettyTable()
    lrTb.field_names = ['number_of_requests', 'latency(ms/r)']
    trTb = PrettyTable()
    trTb.field_names = ['number_of_threads', 'throughput(r/s)']
    for nor in range(len(lrLst)):
        lrTb.add_row([10**(nor+1), int(lrLst[nor]*1000)])
    for nt in range(len(trLst)):
        trTb.add_row([nt+1, int(trLst[nt])])
    print(lrTb, trTb)

def TputTest(url, api):
    # number of thread list
    trLst = []
    notLst = range(1,11)
    for nt in notLst:
        queryLst = [ random.randint(min_num, max_num) for i in range(10)]
        #print('number of threads: %d, number of querys: %d' % (nt, len(queryLst)))
        pool = Pool(processes=nt)
        start = time.time()
        res = [ pool.apply_async(query, (q, url, api)) for q in queryLst ]
        for re in tqdm(res):
            re.get()
        end = time.time()
        trLst.append((10 / (end - start)))
    return trLst

def LatencyTest(url, api):
    # number of request list
    lrLst = []
    norLst = [10, 100]
    for nor in norLst:
        queryLst = [ random.randint(min_num, max_num) for i in range(nor)]
        start = time.time()
        for id in tqdm(queryLst):
            query(id, url, api)
        end = time.time()
        lrLst.append(((end - start) / nor))
    return lrLst

if __name__ == '__main__':
    #lr = LatencyTest(url_his, api_his)
    #tr = TputTest(url_his, api_his)
    lr = [0.3029536008834839, 0.2214457130432129, 0.1843657989501953, 0.18939784162044526]
    tr = [3.983674122527586, 6.866074402356782, 13.971673269752504, 9.58865809346394, 13.990261829086482, 30.513835682900563, 15.752908931499869, 18.684565604867185, 55.515026023594956, 35.01826261225654]
    printRes(lr, tr)
    writeRes(lr, tr)

    #lr = LatencyTest(url_saa, api_saa)
    #tr = TputTest(url_saa, api_saa)
    #print('LatencyTest:', lr, 'TputTest', tr)
    #writeRes(lr, tr)
