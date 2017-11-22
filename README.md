# Excelero NVMesh telegraf statistics collector plugin

## Introduction
The Excelero NVMesh telegraf statistics collector plugin is integrated through and configured in the Telegraf statistics collector inputs.exec interface.

The current and initial version collects the following volume/device statistics from the NVMesh client Volumes:
### num_ops
The number of IO requests from the kernel to the NVMesh volumes

### size in_bytes
Total size of all the ios in bytes. Size/num_ops will give you the average size of the io.  

### io_latency
Reflects the typical time it takes under good conditions in micro seconds to sucessfully excecute the IO and return ack to the kernel 

### io_execution
Reflects the actual time it takes in micro seconds to execute the IO which may be higher tha the latency number due to SSD and/or network issues

### io_e2e
End to end time it takes in micro seconds on from the kernel sending the IO request back to the ack back to the kernel considering all factors they may imact the execution time like 	throttleing, IO retries, path failure, etc. 

### io_latency^2
latency ^2, used to calculate variance

### worst_latency
Highest/max latency

### worst_execution
Highest/max execution time

### worst_e2e
Highest/max end to end time
