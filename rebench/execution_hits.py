from rebench.interop.adapter   import GaugeAdapter
from rebench.model.data_point  import DataPoint
from rebench.model.measurement import Measurement
import re

def parse_dictionary_string(s):
    # Extract the content inside "Dictionary(...)"
    match = re.search(r'Dictionary\((.*?)\)', s)
    if not match:
        return {}

    inner_content = match.group(1)
    # Find all ClassName->Number pairs
    pairs = re.findall(r'(\w+)->(\d+)', inner_content)

    # Convert to dictionary
    result = [[key, int(value)] for key, value in pairs]
    return result

class MyAdapter(GaugeAdapter):

    def parse_data(self, data, run_id, invocation):
        iteration = 1
        data_points = []
        current = DataPoint(run_id)
        parsed = parse_dictionary_string(data)

        # print("\n")
        # print(run_id) # RunId(benchMeteor, 1, None, , , , 0)
        # print(parsed) # [['CleanBlockClosure', 2114], ['ConstantBlockClosure', 2570]]
        # print("\n")

        for [bench, value] in parsed:
            measure = Measurement(invocation, iteration, value, bench, run_id, 'total')
            current.add_measurement(measure)
            data_points.append(current)
            current = DataPoint(run_id)
            iteration += 1

        return data_points