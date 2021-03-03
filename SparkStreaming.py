import pyspark
from pyspark import SparkContext, RDD
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
import pandas as pd
import pymongo
import socket


def split0(x):
    data = x.split(",")
    data[5] = int(data[5])
    data[6] = int(data[6])
    return data


# def educationCout(x):
#     num = x[1][0]
#     avgSalary = x[1][1] / x[1][0]
#     myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#     mydb = myclient["job"]
#     mycol = mydb["educationResult"]
#     mycol.delete_one({"education": x[0]})
#     mycol.insert_one({"education": x[0], "num": num, "avgSalary": avgSalary})


def aboutEducation(rdd: RDD):
    num = rdd.count()
    if num > 0:
        data = rdd.map(lambda x: (x[2], x[5]))
        num1 = data.reduceByKey(lambda x, y: x + y)
        data = rdd.map(lambda x: (x[2], x[6] * x[5]))
        salary = data.reduceByKey(lambda x, y: x + y)
        result = num1.join(salary)
        print(result.take(result.count()))
        result=result.map(lambda x:[x[0],x[1][1]/x[1][0]])
        tmp=result.take(result.count())
        string="?"
        for i in range(0,len(tmp)):
            edu=tmp[i][0]
            salary=str(tmp[i][1])
            string=string+edu+","+salary+";"
        tcp_socket.send(string.encode("utf-8"))
        #vision.get_edu_salary_barchart(tmp)


def aboutCity(rdd: RDD):
    num = rdd.count()
    if num > 0:
        data = rdd.map(lambda x: (x[0], x[5]))
        num1 = data.reduceByKey(lambda x, y: x + y)
        data = rdd.map(lambda x: (x[0], x[6] * x[5]))
        salary = data.reduceByKey(lambda x, y: x + y)
        result = num1.join(salary)
        result=result.map(lambda x:[x[0],x[1][0],x[1][1]/x[1][0]])  #得到城市的数据[城市，岗位数量，薪资]
        tmp=result.take(result.count())
        for i in range(0,len(tmp)):
            if tmp[i][0]=="黑龙江省" or tmp[i][0]=="内蒙古自治区":
                tmp[i][0]=tmp[i][0][0:3]
            else:
                tmp[i][0]=tmp[i][0][0:2]
        string="#"
        for i in range(0,len(tmp)):
            city=tmp[i][0]
            num=str(tmp[i][1])
            salary=str(tmp[i][2])
            string=string+city+","+salary+","+num+";"
        tcp_socket.send(string.encode("utf-8"))   #以字节流的形式传给另一个端口
        # list=[]
        # for i in range(0,result.count()+1):
        #     tmp1=result.take(i)
        #     tmp2=[]
        #     tmp2.append(tmp1[0][0])
        #     tmp2.append(tmp1[0][1][1]/tmp1[0][1][0])
        #     list.append(tmp2)
        #vision.add_data(tmp)
        # print(result.take(1))
        # list=result.foreach(cityCout)
        # animation.add_data(list)

#
# def cityCout(x):
#     num = x[1][0]
#     avgSalary = x[1][1] / x[1][0]
#     myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#     mydb = myclient["mytest"]
#     mycol = mydb["cityResult"]
#     mycol.delete_one({"city": x[0]})
#     mycol.insert_one({"city": x[0], "num": num, "avgSalary": avgSalary})
#     print([x[0],avgSalary])
#     return [x[0],avgSalary]

if __name__ == '__main__':
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #建立socket连接
    dest_addr = ('localhost', 8888)
    tcp_socket.connect(dest_addr)
    sparkConf = SparkConf().setMaster("local").setAppName("SparkStreaming")
    sc = SparkContext(conf=sparkConf)
    ssc = StreamingContext(sc, 5)      #每隔五秒监控一下
    dirStream = ssc.textFileStream(".\data")
    stream = dirStream.map(split0)
    stream.foreachRDD(aboutEducation)
    stream.foreachRDD(aboutCity)
    stream.pprint()
    ssc.start()
    ssc.awaitTermination()
