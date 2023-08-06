Quickstart
==========

Installing opencensus-ext-newrelic
----------------------------------

To start, the ``opencensus-ext-newrelic`` package must be installed. To install
through pip:

.. code-block:: bash

    $ pip install opencensus-ext-newrelic

If that fails, download the library from its GitHub page and install it using:

.. code-block:: bash

    $ python setup.py install


Using the trace exporter
------------------------

The example code assumes you've set the following environment variables:

* ``NEW_RELIC_INSERT_KEY``

.. code-block:: python

    import os
    import time
    from opencensus.trace.tracer import Tracer
    from opencensus.trace import samplers
    from opencensus_ext_newrelic import NewRelicTraceExporter

    newrelic = NewRelicTraceExporter(
        insert_key=os.environ["NEW_RELIC_INSERT_KEY"], service_name="Example Service"
    )

    tracer = Tracer(exporter=newrelic, sampler=samplers.AlwaysOnSampler())

    with tracer.span(name="main") as span:
        time.sleep(0.5)

    # Send all data and stop the exporter
    newrelic.stop()


Using the stats exporter
------------------------

Metrics are an excellent way to expose aggregated information about your
application. The stats exporter allows metrics to be exported from opencensus
to New Relic.

The example code assumes you've set the following environment variables:

* ``NEW_RELIC_INSERT_KEY``

.. code-block:: python

    import os
    import time
    from opencensus.stats import aggregation as aggregation_module
    from opencensus.stats import measure as measure_module
    from opencensus.stats import stats as stats_module
    from opencensus.stats import view as view_module
    from opencensus_ext_newrelic import NewRelicStatsExporter

    # The stats recorder
    stats = stats_module.stats
    view_manager = stats.view_manager
    stats_recorder = stats.stats_recorder
    newrelic = NewRelicStatsExporter(
        os.environ["NEW_RELIC_INSERT_KEY"], service_name="Example Service"
    )
    view_manager.register_exporter(newrelic)

    # Create the measures and views
    # The latency in milliseconds
    m_latency_ms = measure_module.MeasureFloat(
        "task_latency", "The task latency in milliseconds", "ms"
    )

    latency_view = view_module.View(
        "task_latency_latest",
        "The latest task latency",
        [],
        m_latency_ms,
        aggregation_module.LastValueAggregation(),
    )

    view_manager.register_view(latency_view)
    mmap = stats_recorder.new_measurement_map()

    # Record a metric
    mmap.measure_float_put(m_latency_ms, 50)
    mmap.record()

    # Send all data and stop the exporter
    newrelic.stop()


Find and use data
-----------------

Tips on how to find and query your data in New Relic:

* `Find metric data <https://docs.newrelic.com/docs/data-ingest-apis/get-data-new-relic/metric-api/introduction-metric-api#find-data>`_
* `Find trace/span data <https://docs.newrelic.com/docs/understand-dependencies/distributed-tracing/trace-api/introduction-trace-api#view-data>`_

For general querying information, see:

* `Query New Relic data <https://docs.newrelic.com/docs/using-new-relic/data/understand-data/query-new-relic-data>`_
* `Intro to NRQL <https://docs.newrelic.com/docs/query-data/nrql-new-relic-query-language/getting-started/introduction-nrql>`_
