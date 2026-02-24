# Node-Local Files in MPI
***MPI-safe patterns for per-rank scratch files (node-local */tmp*)***

When you use */tmp* in an MPI job, remember:

* */tmp* is **node-local**, so **each node has its own** */tmp*
* **multiple ranks on the same node share the same */tmp* namespace**
* if you don’t separate per-rank (and sometimes per-node) paths, ranks will overwrite each other


## Why */tmp* requires special handling in MPI jobs

The */tmp* directory is:

* **Fast** (node-local disk or RAM-backed)
* **Not shared across nodes**
* **Shared by all ranks on the same node**
* **Deleted when the job ends**

As a result:

* */tmp/input.dat* is visible to *all ranks on that node*
* Rank collisions will occur unless filenames or directories are separated
* Files in */tmp* must be explicitly copied back to shared storage

This is fundamentally different from Tapis-staged directories on shared filesystems, where all nodes see the same paths.


## Managing /tmp files by Rank

Below are safe, practical patterns you can drop into *tapisjob_app.sh* (or any Slurm-launched MPI wrapper).

---

:::{dropdown} **Pattern 1 — One unique scratch directory per rank**

This is the simplest and safest approach: every rank creates and uses its own folder.

```bash
# In your MPI-launched command context
# Assumes Slurm; adjust env vars if needed.
RANK="${SLURM_PROCID:-0}"
JOBID="${SLURM_JOB_ID:-manual}"
SCR_ROOT="/tmp/${USER}/tapis_${JOBID}"
SCR_RANK="${SCR_ROOT}/rank_${RANK}"

mkdir -p "${SCR_RANK}"

# Copy in only what this rank needs (or common files if small)
cp -p input_${RANK}.dat "${SCR_RANK}/" 2>/dev/null || true
cp -p common.dat "${SCR_RANK}/" 2>/dev/null || true

# Run using node-local paths
cd "${SCR_RANK}"
./solver common.dat "input_${RANK}.dat" > "rank_${RANK}.log" 2>&1

# Copy out required outputs to shared filesystem
cp -p output_${RANK}.dat "${TAPIS_JOB_WORKDIR}/" 2>/dev/null || true
cp -p "rank_${RANK}.log" "${TAPIS_JOB_WORKDIR}/logs/" 2>/dev/null || true
```

**Why it’s safe:** no file collisions, easy debugging (each rank has its own working directory).

:::

:::{dropdown} **Pattern 2 — One scratch directory per node, then per-rank inside it**

This is useful when you want a shared node-local cache (e.g., a big lookup table) but still avoid rank collisions.

```bash
RANK="${SLURM_PROCID:-0}"
LOCALID="${SLURM_LOCALID:-0}"           # rank index within node
NODEID="${SLURM_NODEID:-0}"             # node index within allocation
JOBID="${SLURM_JOB_ID:-manual}"

SCR_NODE="/tmp/${USER}/tapis_${JOBID}/node_${NODEID}"
SCR_RANK="${SCR_NODE}/rank_${LOCALID}"

mkdir -p "${SCR_RANK}"

# (Optional) node-shared cache directory
SCR_CACHE="${SCR_NODE}/cache"
mkdir -p "${SCR_CACHE}"
```

**Typical use:** one rank per node populates *${SCR_CACHE}*, others read from it.

:::

:::{dropdown} **Pattern 3 — “One rank per node” does the heavy copy (node-local caching)**

Use this when you have a **large common file** (e.g., ground motions, big meshes) that would be wasteful to copy once per rank.

**Goal:** copy once per node, then all ranks on that node read it from */tmp*.

```bash
NODEID="${SLURM_NODEID:-0}"
LOCALID="${SLURM_LOCALID:-0}"
JOBID="${SLURM_JOB_ID:-manual}"

SCR_NODE="/tmp/${USER}/tapis_${JOBID}/node_${NODEID}"
SCR_CACHE="${SCR_NODE}/cache"
mkdir -p "${SCR_CACHE}"

COMMON_SRC="${TAPIS_JOB_WORKDIR}/common_big.dat"
COMMON_DST="${SCR_CACHE}/common_big.dat"

# Only LOCALID==0 copies the large file on each node
if [[ "${LOCALID}" == "0" ]]; then
  cp -p "${COMMON_SRC}" "${COMMON_DST}"
fi

# MPI-safe barrier so other ranks don't read before copy finishes
# (If you are launching with srun, the simplest is an srun barrier step)
```

**Barrier options (choose one):**

**A) srun “barrier step” (recommended in Slurm jobs):**

```bash
# Make sure every task reaches this point before proceeding
srun --ntasks="${SLURM_NTASKS}" --ntasks-per-node="${SLURM_NTASKS_PER_NODE}" bash -c 'true'
```

This works because Slurm won’t complete the step until all tasks start and finish the no-op.

**B) File-based barrier (portable, but more management):**

```bash
BARRIER="${SCR_NODE}/.ready"
if [[ "${LOCALID}" == "0" ]]; then
  cp -p "${COMMON_SRC}" "${COMMON_DST}"
  touch "${BARRIER}"
fi

# Everyone waits until the node-local copy is ready
while [[ ! -f "${BARRIER}" ]]; do
  sleep 0.1
done
```

Then each rank can safely run:

```bash
./solver "${COMMON_DST}" other_inputs...
```

:::

:::{dropdown} **Pattern 4 — Output aggregation: avoid “N ranks writing one shared file”**

A very common failure mode is all ranks appending to one output file on shared storage or even */tmp*.

**Safer alternatives:**

**4A) Per-rank outputs, then merge on rank 0**

```bash
RANK="${SLURM_PROCID:-0}"
OUTDIR="${TAPIS_JOB_WORKDIR}/outputs"
mkdir -p "${OUTDIR}"

# each rank writes its own output
./solver ... > "${OUTDIR}/rank_${RANK}.out" 2>&1

# rank 0 merges in order (optional)
if [[ "${RANK}" == "0" ]]; then
  cat "${OUTDIR}"/rank_*.out > "${OUTDIR}/merged.out"
fi
```

**4B) Use MPI-IO or a parallel output format (best for large data)**

If your code supports HDF5/MPI-IO or parallel NetCDF, that’s typically more scalable than ad-hoc text aggregation.

:::

:::{dropdown} **Pattern 5 — Cleanup that won’t break your run**

You generally want cleanup, but you don’t want rank races deleting shared paths too early.

**Rule of thumb:**

* each rank can delete **its own** rank directory
* only one rank per node (LOCALID==0) deletes node directories
* rank 0 deletes job-level scratch root (optional)

```bash
RANK="${SLURM_PROCID:-0}"
LOCALID="${SLURM_LOCALID:-0}"
NODEID="${SLURM_NODEID:-0}"
JOBID="${SLURM_JOB_ID:-manual}"

SCR_ROOT="/tmp/${USER}/tapis_${JOBID}"
SCR_NODE="${SCR_ROOT}/node_${NODEID}"
SCR_RANK="${SCR_NODE}/rank_${LOCALID}"

# delete per-rank
rm -rf "${SCR_RANK}"

# node leader deletes node dir after a brief wait
if [[ "${LOCALID}" == "0" ]]; then
  # small delay helps avoid races in some workflows
  sleep 0.2
  rm -rf "${SCR_NODE}"
fi

# (Optional) global cleanup by rank 0
if [[ "${RANK}" == "0" ]]; then
  sleep 0.5
  rm -rf "${SCR_ROOT}"
fi
```

If you ever want post-mortem debugging, **skip cleanup** or gate it behind a flag like *KEEP_TMP=1*.
:::

---

## Quick decision guide

* **Most robust:** Pattern 1 (per-rank dir)
* **Best for big shared inputs:** Pattern 3 (per-node cache + barrier)
* **Best for outputs:** Pattern 4A (per-rank files + merge) or MPI-IO formats
* **Least fragile cleanup:** Pattern 5 (hierarchical cleanup)

:::{dropdown} **Combination Bash utility block**
The following block combines all of the above. You can reuse it across all your Tapis app wrappers:

```
#!/usr/bin/env bash
#===============================================================================
# MPI / Slurm / Tapis: node-local /tmp utilities (drop-in)
#
# Goal:
#   Safe, reusable helpers for per-rank scratch dirs, per-node caching,
#   lightweight barriers, and staging outputs back to the shared job directory.
#
# Designed for:
#   Slurm-launched MPI jobs (srun/mpirun within a Tapis job wrapper).
#
# Notes:
#   - /tmp is node-local and ephemeral. Use only for temporary files.
#   - Avoid collisions by always using rank- or node-scoped paths.
#   - Prefer "copy once per node" for large shared inputs.
#===============================================================================

set -euo pipefail

#-----------------------------
# Environment discovery
#-----------------------------
mpi_rank()   { echo "${SLURM_PROCID:-0}"; }
mpi_localid(){ echo "${SLURM_LOCALID:-0}"; }
mpi_nodeid() { echo "${SLURM_NODEID:-0}"; }

job_id()     { echo "${SLURM_JOB_ID:-manual}"; }
user_name()  { echo "${USER:-user}"; }

# Shared work directory (Tapis sets this; fall back to current working dir)
shared_workdir() {
  if [[ -n "${TAPIS_JOB_WORKDIR:-}" ]]; then
    echo "${TAPIS_JOB_WORKDIR}"
  else
    echo "$(pwd)"
  fi
}

# Root for all node-local scratch for this job
tmp_root() {
  local jid; jid="$(job_id)"
  echo "/tmp/$(user_name)/tapis_${jid}"
}

# Node-scoped scratch root on this node
node_tmp_root() {
  local node; node="$(mpi_nodeid)"
  echo "$(tmp_root)/node_${node}"
}

#-----------------------------
# Logging helpers
#-----------------------------
log()  { echo "[tmp-util] $*" >&2; }
die()  { echo "[tmp-util][ERROR] $*" >&2; exit 1; }

#-----------------------------
# Core utilities
#-----------------------------

# make_rank_tmp [optional_subdir]
# Creates and prints a unique per-rank scratch directory on this node.
make_rank_tmp() {
  local sub="${1:-}"
  local lid; lid="$(mpi_localid)"
  local base; base="$(node_tmp_root)/rank_${lid}"
  local path="${base}"
  if [[ -n "${sub}" ]]; then
    path="${base}/${sub}"
  fi
  mkdir -p "${path}"
  echo "${path}"
}

# make_node_tmp [optional_subdir]
# Creates and prints a node-scoped scratch directory (shared by ranks on node).
make_node_tmp() {
  local sub="${1:-}"
  local base; base="$(node_tmp_root)"
  local path="${base}"
  if [[ -n "${sub}" ]]; then
    path="${base}/${sub}"
  fi
  mkdir -p "${path}"
  echo "${path}"
}

# node_leader: true if this rank is "leader" on node (LOCALID==0)
node_leader() {
  [[ "$(mpi_localid)" == "0" ]]
}

# global_leader: true if this rank is rank 0 in the MPI world
global_leader() {
  [[ "$(mpi_rank)" == "0" ]]
}

# node_cache_file <source_path> <dest_basename> [cache_subdir]
# Copy a file ONCE PER NODE into node-local cache, then wait until ready.
# Returns full path to cached file.
node_cache_file() {
  local src="${1:?source_path required}"
  local name="${2:?dest_basename required}"
  local sub="${3:-cache}"

  local cache_dir; cache_dir="$(make_node_tmp "${sub}")"
  local dst="${cache_dir}/${name}"
  local ready="${cache_dir}/.${name}.ready"

  # Only one rank per node copies
  if node_leader; then
    if [[ ! -f "${src}" ]]; then
      die "node_cache_file: source not found: ${src}"
    fi
    # Copy atomically: write to temp then mv
    local tmp="${dst}.tmp.$$"
    log "Node leader copying to cache: ${src} -> ${dst}"
    cp -p "${src}" "${tmp}"
    mv -f "${tmp}" "${dst}"
    : > "${ready}"
  fi

  # All ranks wait until cache is ready
  while [[ ! -f "${ready}" ]]; do
    sleep 0.1
  done

  echo "${dst}"
}

# mpi_barrier [barrier_name]
# Lightweight synchronization barrier.
# Implementation:
#   - If running under srun with Slurm vars, uses a file-based barrier per node.
#   - Optionally, you can replace with an "srun no-op step" barrier if desired.
#
# For most workflows, you only need node-local barriers (per-node cache).
mpi_barrier() {
  local name="${1:-barrier}"
  local dir; dir="$(make_node_tmp "sync")"
  local flag="${dir}/.${name}.ready"

  # Node-local barrier: node leader touches flag; others wait.
  if node_leader; then
    : > "${flag}"
  fi
  while [[ ! -f "${flag}" ]]; do
    sleep 0.05
  done

  # NOTE: This is a node-local barrier (ranks on same node).
  # For a *global* barrier across all nodes, use global_file_barrier below.
}

# global_file_barrier [barrier_name] [shared_dir]
# Global barrier across all ranks/nodes using the shared filesystem.
# Use sparingly: it adds shared FS metadata traffic.
global_file_barrier() {
  local name="${1:-global_barrier}"
  local shared="${2:-$(shared_workdir)}"
  local n="${SLURM_NTASKS:-}"

  [[ -n "${n}" ]] || die "global_file_barrier requires SLURM_NTASKS to be set."

  local bdir="${shared}/.barriers/${name}"
  mkdir -p "${bdir}"

  local r; r="$(mpi_rank)"
  local token="${bdir}/rank_${r}"
  : > "${token}"

  # rank 0 waits for all tokens then releases
  local release="${bdir}/RELEASE"
  if global_leader; then
    log "Global barrier: waiting for ${n} ranks..."
    local i
    for (( i=0; i< n; i++ )); do
      while [[ ! -f "${bdir}/rank_${i}" ]]; do
        sleep 0.05
      done
    done
    : > "${release}"
  fi

  while [[ ! -f "${release}" ]]; do
    sleep 0.05
  done
}

# stage_in <src> <dst_dir>
# Copy a file/dir from shared filesystem into a given /tmp directory.
# - Preserves timestamps/permissions.
# - Works for files and directories.
stage_in() {
  local src="${1:?src required}"
  local dst_dir="${2:?dst_dir required}"
  mkdir -p "${dst_dir}"

  if [[ -d "${src}" ]]; then
    log "Staging in directory: ${src} -> ${dst_dir}/"
    cp -a "${src}" "${dst_dir}/"
  else
    log "Staging in file: ${src} -> ${dst_dir}/"
    cp -p "${src}" "${dst_dir}/"
  fi
}

# stage_out <src> <dst_dir>
# Copy a file/dir from /tmp back to shared filesystem.
# - Creates destination dir.
# - For directories, copies recursively.
stage_out() {
  local src="${1:?src required}"
  local dst_dir="${2:?dst_dir required}"
  mkdir -p "${dst_dir}"

  if [[ -d "${src}" ]]; then
    log "Staging out directory: ${src} -> ${dst_dir}/"
    cp -a "${src}" "${dst_dir}/"
  else
    log "Staging out file: ${src} -> ${dst_dir}/"
    cp -p "${src}" "${dst_dir}/"
  fi
}

# safe_rm <path>
# Defensive delete for scratch paths (only under /tmp/<user>/tapis_<jobid>).
safe_rm() {
  local p="${1:?path required}"
  local root; root="$(tmp_root)"

  if [[ "${p}" != "${root}"* ]]; then
    die "Refusing to delete outside job tmp root. path=${p} root=${root}"
  fi
  rm -rf "${p}"
}

# cleanup_tmp [KEEP_TMP env honored]
# Hierarchical cleanup:
#   - each rank deletes its own rank dir
#   - node leader deletes node dir
#   - global leader deletes root (optional)
cleanup_tmp() {
  if [[ "${KEEP_TMP:-0}" == "1" ]]; then
    log "KEEP_TMP=1 set; skipping cleanup."
    return 0
  fi

  local lid; lid="$(mpi_localid)"
  local node; node="$(mpi_nodeid)"
  local rdir; rdir="$(node_tmp_root)/rank_${lid}"
  local ndir; ndir="$(tmp_root)/node_${node}"
  local root; root="$(tmp_root)"

  # per-rank cleanup
  [[ -d "${rdir}" ]] && safe_rm "${rdir}" || true

  # node leader cleans node directory after brief delay
  if node_leader; then
    sleep 0.2
    [[ -d "${ndir}" ]] && safe_rm "${ndir}" || true
  fi

  # global leader can remove root
  if global_leader; then
    sleep 0.5
    [[ -d "${root}" ]] && safe_rm "${root}" || true
  fi
}

#===============================================================================
# Example usage (copy/paste into your wrapper as needed)
#===============================================================================
#
# # 1) Create per-rank scratch dir
# RANK_DIR="$(make_rank_tmp)"
# cd "${RANK_DIR}"
#
# # 2) Cache a large shared input once per node
# COMMON_SHARED="$(shared_workdir)/inputs/ground_motions.bin"
# COMMON_LOCAL="$(node_cache_file "${COMMON_SHARED}" "ground_motions.bin")"
#
# # 3) Stage rank-specific input and run
# stage_in "$(shared_workdir)/inputs/input_$(mpi_rank).dat" "${RANK_DIR}"
# ./solver "${COMMON_LOCAL}" "input_$(mpi_rank).dat" > "rank_$(mpi_rank).log" 2>&1
#
# # 4) Stage outputs back to shared FS
# stage_out "${RANK_DIR}/rank_$(mpi_rank).log" "$(shared_workdir)/logs"
# stage_out "${RANK_DIR}/output_$(mpi_rank).dat" "$(shared_workdir)/outputs"
#
# # 5) Cleanup (or set KEEP_TMP=1 to preserve for debugging)
# cleanup_tmp
#
#===============================================================================
```
:::