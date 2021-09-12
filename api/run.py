from sake_global import sake_global_fetch_data
from axis_plan import axis_plan_fetch_data

def fetch_data():
    result_sake_global = sake_global_fetch_data()
    all_results=result_sake_global
    # for i in range(1,6):
    #     print(result_sake_global[i])
    result_sake_axis_plan = axis_plan_fetch_data()
    all_results.append(result_sake_axis_plan)
    # for i in range(1,6):
    #     print(result_sake_axis_plan[i])
    print(len(all_results))
    print(all_results[0:2])
    return all_results


fetch_data()