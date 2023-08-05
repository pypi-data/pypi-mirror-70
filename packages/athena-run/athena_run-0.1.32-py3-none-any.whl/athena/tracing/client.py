from statsd.client import timer
from datetime import timedelta
from statsd.client import udp
from athena.tracing import DefaultContext
import time
from athena.tracing.config import SPAN_RECORD


# Use timer that's not susceptible to time of day adjustments.
try:
    # perf_counter is only present on Py3.3+
    from time import perf_counter as time_now
except ImportError:
    # fall back to using time
    from time import time as time_now

_StatsClient = udp.StatsClient
_Timer = timer.Timer


class PatchedStatsClient(_StatsClient):
    """
    PatchStatsClient that returns custom JSON format containing trace information
    """

    def timer(self, stat, rate=1, meta={}):
        return PatchedTimer(self, stat, rate, meta)

    def parametrized(self, stat, rate=1):
        return ParametrizedPatchedTimer(self, stat, rate)

    def timing(self, stat, start_time, delta, parent, self_id, rate=1, meta={}):
        """
        Send new timing information.
        `delta` can be either a number of milliseconds or a timedelta.
        """

        if isinstance(delta, timedelta):
            # Convert timedelta to number of microseconds
            delta_microseconds = int(delta.total_milliseconds() * 1000.0)
        else:
            delta_microseconds = int(delta * 1000.0)

        span_record = SPAN_RECORD(
            parent_id=parent,
            span_id=self_id,
            start_time=start_time,
            trace_id=DefaultContext.trace_id,
            service=DefaultContext.service,
            operation=stat,
            end_time=start_time + delta_microseconds,
            children=DefaultContext.child_map[self_id],
            meta=meta,
        )

        DefaultContext.add_span_to_trace_buffer(span_record=span_record)


class PatchedTimer(_Timer):
    """
    Patched Timer that keeps track of parent state and collects information that
    allows the Stats Client to return the JSON format
    """

    def __init__(self, client, stat, rate, meta):
        self._meta = meta

        super().__init__(client, stat, rate)

    def __call__(self, f):
        """Thread-safe timing function decorator."""

        @timer.safe_wraps(f)
        def _wrapped(*args, **kwargs):
            """
            Patching the Timer when called by decorator
            :param args:
            :param kwargs:
            :return:
            """
            parent = DefaultContext.get_current_span_from_parent_tree()
            DefaultContext.add_new_span_to_parent_tree()
            self_id = DefaultContext.get_current_span_from_parent_tree()
            duration_begin = time_now()
            start_time = int(time.time() * (10 ** 6))
            try:
                return f(*args, **kwargs)
            finally:
                elapsed_time_ms = 1000.0 * (time_now() - duration_begin)
                self_id = DefaultContext.get_current_span_from_parent_tree()
                DefaultContext.remove_current_span_from_parent_tree()
                self.client.timing(
                    self.stat, start_time, elapsed_time_ms, parent, self_id, self.rate,
                    meta=self._meta
                )

        return _wrapped

    """
    The start & send functions below work when the Timer is called with a "with"
    statement.
    """

    def start(self):
        # statsd.Timer class members
        self.ms = None
        self._sent = False
        self._start_time = time_now()

        # extensions
        self.__clock_start_time = int(time.time() * (10 ** 6))
        self.__parent = DefaultContext.get_current_span_from_parent_tree()
        DefaultContext.add_new_span_to_parent_tree()
        return self

    def send(self):
        if self.ms is None:
            raise RuntimeError("No data recorded.")
        if self._sent:
            raise RuntimeError("Already sent data.")
        self._sent = True
        self_id = DefaultContext.get_current_span_from_parent_tree()
        DefaultContext.remove_current_span_from_parent_tree()
        self.client.timing(
            self.stat,
            self.__clock_start_time,
            self.ms,
            self.__parent,
            self_id,
            self.rate,
            meta=self._meta
        )


class ParametrizedPatchedTimer(_Timer):
    """
    Patched Timer that keeps track of parent state and collects information that
    allows the Stats Client to return the JSON format
    """

    def __call__(self, f):
        """Thread-safe timing function decorator."""

        @timer.safe_wraps(f)
        def _wrapped(*args, **kwargs):
            """
            Patching the Timer when called by decorator
            :param args:
            :param kwargs:
            :return:
            """
            parent = DefaultContext.get_current_span_from_parent_tree()
            DefaultContext.add_new_span_to_parent_tree()
            self_id = DefaultContext.get_current_span_from_parent_tree()
            duration_begin = time_now()
            start_time = int(time.time() * (10 ** 6))

            arg_params = args
            kwarg_params = kwargs

            try:
                return f(*args, **kwargs)
            finally:
                elapsed_time_ms = 1000.0 * (time_now() - duration_begin)
                self_id = DefaultContext.get_current_span_from_parent_tree()
                DefaultContext.remove_current_span_from_parent_tree()
                self.client.timing(
                    self.stat,
                    start_time,
                    elapsed_time_ms,
                    parent,
                    self_id,
                    self.rate,
                    meta={"args": arg_params, "kwargs": kwarg_params},
                )

        return _wrapped

    """
    The start & send functions below work when the Timer is called with a "with"
    statement.
    """

    def start(self):
        # statsd.Timer class members
        self.ms = None
        self._sent = False
        self._start_time = time_now()

        # extensions
        self.__clock_start_time = int(time.time() * (10 ** 6))
        self.__parent = DefaultContext.get_current_span_from_parent_tree()
        DefaultContext.add_new_span_to_parent_tree()
        return self

    def send(self):
        if self.ms is None:
            raise RuntimeError("No data recorded.")
        if self._sent:
            raise RuntimeError("Already sent data.")
        self._sent = True
        self_id = DefaultContext.get_current_span_from_parent_tree()
        DefaultContext.remove_current_span_from_parent_tree()
        self.client.timing(
            self.stat,
            self.__clock_start_time,
            self.ms,
            self.__parent,
            self_id,
            self.rate,
        )
