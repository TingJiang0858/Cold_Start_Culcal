# Analysis code for Azure Function Workload Traces
- Copy Azure Function Traces (invocations_per_function_md.anon.d01.csv to .d14.csv) to ./az_data
- Single execution -- python3 cal_cold_start idle_time. e.g., `python3 cal_cold_start 10`
- Batch execution -- `./run_batch.sh` -- Current script is to run batch jobs with 20+ cores. You can redistribute load based on the your machine specifications.

