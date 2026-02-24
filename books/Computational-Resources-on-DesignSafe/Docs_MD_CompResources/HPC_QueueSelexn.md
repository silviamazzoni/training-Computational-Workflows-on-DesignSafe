# Queue Selection
**How to choose the queue for your project**

On Stampede3, you specify a queue by specifying the node type to be used and, where possible, a special case of the node, such a large-memory, or development. 
Each node type has its own performance characteristics based on speed, memory, and accessibility. 
The choice of which nodes to use is project dependent because you need to evaluate performance metrics against the cost metrics.

The following are some of the metrics that should be considered when selecting a queue:

## Performance Metrics
- Processor Type: CPU/GPU
- Number of Nodes available per job
- Number of Cores (Processors) per Node
- Processor Speed
- Communication Speed
- I/O speed (read/write)
- Memory
- Multi-Threading Capabilities

## Cost Metrics
- Cost per hour
- Availability and Wait Time
- Max Nodes/Job
- Max Jobs in Queue
- Max Job Duration
