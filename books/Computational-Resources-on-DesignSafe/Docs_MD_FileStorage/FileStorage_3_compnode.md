# On Compute Nodes
***Storage on Compute Nodes: /tmp***

In addition to *Home*, *Work*, and *Scratch*, **each compute node** on any Compute System such as Stampede3 **has its own local temporary storage**, typically mounted at:

```
/tmp
```

This is **the fastest storage available**, because it's physically located on the node — closest to the processors.

## When to Use */tmp*
    
* If your job performs lots of fast, repeated read/write operations (e.g., temp caching, I/O-intensive loops)
* If you need **scratch-like speed** for intermediate steps
* If you're staging files for **a second phase** within the same job

## Considerations

* */tmp* is **local to each node** — it’s not shared across nodes or persistent after the job ends.
* You must **explicitly copy files to and from */tmp*** in your job script (using *cp* or *rsync*).
* If output is written to */tmp*, you must **move it to *$SCRATCH* or *$WORK*** before your job ends, or the data will be lost.

## Best Practices

* Use */tmp* **only when the performance benefit outweighs the cost** of transferring data in and out.
* Benchmark your job with and without */tmp* to see if it's worth the added complexity.
* For multi-node jobs, remember each node has a **separate */tmp*** — they don’t share it.

