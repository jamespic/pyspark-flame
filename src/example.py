import time
import random
from pyspark_flame import FlameProfiler
from pyspark import SparkConf, SparkContext


def multiply_inefficiently(x):
    for i in range(1000):
        time.sleep(0.0001 * random.random())
        time.sleep(0.0001 * random.random())
    return x * 2


conf = SparkConf().set("spark.python.profile", "true")#.set("spark.python.profile.dump", ".")
sc = SparkContext('local', 'test', conf=conf, profiler_cls=FlameProfiler, environment={'pyspark_flame.interval': 0.25})
sc.parallelize(range(1000)).map(multiply_inefficiently).take(10)
sc.show_profiles()
sc.dump_profiles('.')
sc.stop()
