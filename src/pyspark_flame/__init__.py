from __future__ import print_function
from collections import defaultdict
from pyspark import AccumulatorParam
from pyspark.profiler import Profiler
from os.path import join
from threading import Thread, Event
from sys import _current_frames


def extract_stack(frame):
    result = []
    while frame is not None:
        result.append((
            frame.f_code.co_filename,
            frame.f_code.co_name,
            frame.f_lineno
        ))
        frame = frame.f_back
    return tuple(reversed(result))


class Collector(object):
    def __init__(self, interval=0.01):
        self.interval = interval
        self.finished = Event()

    def start(self):
        self.thread = Thread(target=self.run)
        self.thread.start()

    def stop(self):
        self.finished.set()
        self.thread.join()

    def run(self):
        results = defaultdict(int)
        self.results = results
        this_thread = self.thread.ident
        while True:
            self.finished.wait(self.interval)
            if self.finished.is_set():
                return
            results = self.results
            frames = _current_frames()
            for frame_id, frame in frames.items():
                if frame_id != this_thread:
                    stack = extract_stack(frame)
                    results[stack] += 1


class ResultsAccumulator(AccumulatorParam):
    def zero(self, value):
        return defaultdict(int)

    def addInPlace(self, a, b):
        for stack, count in b.items():
            a[stack] += count
        return a


class FlameProfiler(Profiler):
    def __init__(self, ctx):
        self.interval = float(ctx.environment.get('pyspark_flame.interval', 0.05))
        self._accumulator = ctx.accumulator(defaultdict(int), ResultsAccumulator())

    def profile(self, func):
        collector = Collector(self.interval)
        collector.start()
        try:
            func()
        finally:
            collector.stop()
            self._accumulator.add(collector.results)

    def stats(self):
        return self._accumulator.value

    def show(self, id):
        print("Flame Data for RDD {}".format(id))
        print(self.format())

    def dump(self, id, path):
        with open(join(path, 'rdd-{}.flame'.format(id)), 'w') as f:
            f.write(self.format())

    def format(self):
        return ''.join(
            '{stack} {count}\n'.format(stack=';'.join(
                '{file}:{method}:{line}'.format(file=file_, method=method, line=line)
                for file_, method, line in stack
            ), count=count)
            for stack, count in self.stats().items()
        )
