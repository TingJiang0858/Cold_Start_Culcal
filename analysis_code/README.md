# Analysis code for Azure Function Workload Traces
- Copy Azure Function Traces (invocations_per_function_md.anon.d01.csv to .d14.csv) to ./az_data
- Single execution -- python3 cal_cold_start idle_time. e.g., `python3 cal_cold_start 10`
- Batch execution -- `./run_batch.sh` -- you may need more than 20 core machines. You can redistribute loads based on the cores you have.

