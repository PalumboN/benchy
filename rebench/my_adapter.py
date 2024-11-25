from rebench.interop.adapter   import GaugeAdapter
from rebench.model.data_point  import DataPoint
from rebench.model.measurement import Measurement


class MyAdapter(GaugeAdapter):

    def parse_data(self, data, run_id, invocation):
        iteration = 1
        data_points = []
        current = DataPoint(run_id)
        data_points.append(current)

        print("\n")
        print(run_id)
        print(data)
        print("\n")

        measure = Measurement(invocation, iteration, 1, 'hits', run_id, 'total')
        current.add_measurement(measure)

        return data_points