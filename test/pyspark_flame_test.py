from pyspark_flame import FlameProfiler
from pyspark import SparkConf, SparkContext
import os
import shutil
import time
import tempfile
import unittest


def wait_a_bit(*args, **kwargs):
    time.sleep(5.0)
    return 1


def crash(*args, **kwargs):
    raise ValueError("A value error")


class PysparkFlameTest(unittest.TestCase):
    def setUp(self):
        self.dumpdir = tempfile.mkdtemp()
        conf = SparkConf().set("spark.python.profile", "true")
        self.sc = SparkContext('local[*]', 'test',
                               conf=conf,
                               profiler_cls=FlameProfiler,
                               environment={'pyspark_flame.interval': 0.25})

    def tearDown(self):
        self.sc.stop()
        shutil.rmtree(self.dumpdir)

    def test_pyspark_flame(self):

        self.sc.parallelize(range(4)).map(wait_a_bit).sum()
        self.sc.dump_profiles(self.dumpdir)
        dumps = os.listdir(self.dumpdir)
        self.assertEqual(1, len(dumps))
        with open(os.path.join(self.dumpdir, dumps[0])) as dumpfile:
            for line in dumpfile.readlines():
                location, count = line.split(' ')
                if 'pyspark_flame_test.py:wait_a_bit:11' in location:
                    count = int(count)
                    self.assertIn(count, range(70, 90))
                    return
            else:
                self.fail('No wait_a_bit profile line found')

    def test_propagate_exception(self):
        with self.assertRaises(Exception):
            self.sc.parallelize(range(4)).map(crash).sum()
