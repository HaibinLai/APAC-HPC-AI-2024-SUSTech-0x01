#  APAC 2024 HPC-AI
## SUSTech 0x01 Team

**Profiling logs repo**

Thie repo record our profiling result in APAC 2024 HPC-AI 

Structure of the repo:

> file_log_on_qiming

The log file on Qiming 2.0 Cluster

you can find the main logs on /file_log_on_qiming/main_logs

> Haibin99.b07u26a

The Intel Vtune Profiler log for HPC HOOMD-blue 

> python3.12_1536_bx7351.1727860582.512668.ipm.xml_ipm_0

The ipm analysis of HPC HOOMD-blue on Qiming 2.0



**HPC Groups:**
	ZuDong Li (leader)
	Haibin Lai
	Benxiang Xiao
	Zixu Wang
	Wenhan Tan
	Wenbo An

**AI Groups:**
	Yukun Yang
	Honglie Li
	Junyu Su

---

## Abstract

In this report, we detail the optimization efforts conducted on two key applications for the APAC2024 competition: HPC HOOMD-blue and AI Llama2. Initially, we performed benchmark tests on both applications, transitioning from a single-node setup to a multi-node, multi-GPU environment. 

For **HOOMD-blue**, a high-performance molecular dynamics simulation program, we carried out an in-depth analysis of the source code and implemented several optimizations. These included switching to the HPC-X communication library, applying O3 compiler optimization, fine-tuning UCX parameters, replacing Intel MPI with OpenMPI, adjusting program buffer settings, and employing NUMA-aware scheduling for domain decomposition to enhance performance in a multi-node setup.

In the case of **Llama2**, a large-scale language model used for AI tasks, we built upon benchmark results to profile different batch sizes and optimized performance on A100 GPUs using Tensor Cores. We also optimized the FSDP (Fully Sharded Data Parallel) strategy and parameters, replaced the NCCL communication library with MSCCL for improved multi-GPU communication, and introduced techniques to overlap computation with communication. Additionally, we incorporated faster computational operators to further boost training efficiency.

Through these efforts, we achieved significant performance improvements in both the HPC and AI tasks, deepening our knowledge of high-performance computing optimizations and enhancing our profiling capabilities.



<div STYLE="page-break-after: always;"></div>


## About us

We are `SUSTech 0x01` Team:

Under supervision and support of **Centre for Computational Science and Engineering** in SUSTech,  we formed a diverse and experienced award-winning team.

We aim to foster next generation of HPC  talents through actual scientific research and attending international HPC challenges.

At `0x01`, we have abundant computational resources for student to maximize their practical HPC skills, as well as systematic and cutting-edge training.


![[aff6447a2ffc26efa392151137c1b97.jpg]]

<div STYLE="page-break-after: always;"></div>

## HPC HOOMD-blue

### Introduction
![[Pasted image 20241108193032.png]]

HOOMD-blue is a Python package that runs simulations of particle systems. 
It performs hard particle Monte Carlo simulations of a variety of shape classes and molecular dynamics simulations of particles with a range of pair, bond, angle, and other potentials. Many features are targeted at the soft matter research community, though the code is general and capable of many types of particle simulations. It has been actively developed since March 2007 and available open source since August 2008. ^[1]


### CPU Task Workload And Benchmark

The Benchmark needs us to compute WCA potential for the following parameter:
- **Workload**: [md_pair_wca](https://github.com/glotzerlab/hoomd-benchmarks/tree/trunk?tab=readme-ov-file#simulation-benchmarks)
- **Number of particles**: `200,000`
- **Input data**:hard_sphere_200000_1.0_3.gsd

HOOMD-Blue Benchmark calculates **WCA potential** for N particles as workload. WCA potential (Weeks-Chandler-Andersen potential) is a potential energy function used to simulate intermolecular interactions. It is simple, computationally eﬃcient and suitable.

$$
U(r) = 4 \epsilon[(\frac{\sigma}{r})^{12} - (\frac{\sigma}{r})^{6}]
$$
- The WCA potential is commonly used in molecular dynamics simulations, especially when studying physical phenomena such as liquids, gases, and their phase transitions.
- It provides higher computational efficiency by removing the attractive part of the potential.

### System Architecture

**![[Pasted image 20241108214237.png]]**

The system Architecture of HOOMD-blue is shown in the figure. In initialization part, the position and number of particle will be set, then the whole space will be divided into subdomain using a technique called `domain decomposition`. Then each subdomain will be sent to a MPI worker to a slot, computing forces and communicate with each other with buffer. After computation, they will gather and sent the result using `MPI_AllReduce` primitive, and do the computation again until reaching the steps and output result.

### Testing Platform

To test the programme, we use QiMing cluster on SUSTech CCSE. It has 24 CPU cores for each nodes, 64GB Memory and connected with infiniband. 

![[Pasted image 20241108214657.png]]

And we also use Gadi, it has 24 CPU cores per node with 192GB Memory and connected with infiniband. 
![[Pasted image 20241108214714.png]]

The last cluster we use is NSCC. It has 128 cores per server and 512GB Memory and 100 Gbi infiniband.
![[Pasted image 20241108214730.png]]

<div STYLE="page-break-after: always;"></div>
### Baseline Testing and Analysis
We test the Baseline of HOOMD in 3 machines with 1,2,4,8 and 16 nodes, and 32 nodes on Gadi and NSCC. As baseline, we use OpenMPI for HOOMD-blue.

![[Pasted image 20241108214914.png]]

We can find that before 4 nodes, the program’s performance scales up as the number of nodes increase. However after 4 nodes, the performance begins to slow down.

So what led to the slow down? We mainly consider on the communication and load imbalance of HOOMD-blue.


We first use Intel Vtune to see what is the bottleneck of the software on multi nodes. However, the profiler can only detect the cpython library and failed to reveal furthur call stack. 

![[Pasted image 20241108221429.png]]


So we try to use IPM analysis to find out what happen to the communication.


![[Pasted image 20241108220804.png]]


The IPM analysis shows that the communication time increase from the ratio of 15% to nearly 55%. So the communication time counts for slowing down the performance.

And here the figure shows that different clusters get different communication properties.
![[Pasted image 20241108221043.png]]


And these properties difference may be due to the strategy of MPI_Allreduce that MPI choosing. The figure shows different strategy that OpenMPI choose for different chunk file on `MPI_AllReduce` Primitive.

![[Pasted image 20241108221059.png]]

As we can see, the OpenMPI will choose different algorithm based on the size and the number of chunk file. When the file is small, a butterfly algorithm for different nodes will be called. When the file is larger and less than MPI Process, a Reduce&Broadcast algorithm will be called. If the number is larger, a Ring algorithm and even a segmented ring algorithm will be called.

So after this profiling, we think it may be the strategy that OpenMPI used may not suits best for the HOOMD communication.


### HPC-X profiling

To profile this, we use HPC-X to select a better strategy for communication.   HPC-X™ is a comprehensive software package that includes MPI, SHMEM and UPC communications libraries. It integrates **MPI** (specifically **OpenMPI** and **Intel MPI**) to optimize message passing in distributed computing.By only changing that, the performance on QiMing get 413.8% improvement on 16 nodes.

![[Pasted image 20241108222011.png]]


After initiating hcoll, we find all parameters of All_Reduce from hcoll_info.

Here we try to find the best params from 32 nodes with each node 24 nodes:
```bash
--mca coll_hcoll_enable 1
--x HCOLL_ENABLE_SHARP=1 (Correlated to Hardware Switch)
--x HCOLL_ALLREDUCE_LB_SUPPORT=0
--x HCOLL_BCOL_P2P_LARGE_ALLREDUCE_ALG=1
--x HCOLL_BCOL_UCX_P2P_HYBRID_SRA_NODE_RADIX=3
--x HCOLL_BCOL_UCX_P2P_HYBRID_SRA_NET_RADIX=2
```


And now we are trying to select better parameters for HPC-X. We choose SHArP to enable smart switch, P2P_Large AllReduce Algorithm etc.

And here we get another 9% improving with OSHMEM and 8% for MPI.
![[Pasted image 20241108222227.png]]

The performance comparison between HPC-X , IntelMPI and OpenMPI shows that HPC-X delivers superior performance and greater scalability with the same number of cores. 
And we hope rebuilding OpenMPI with HPC-X can help us make a better decision on improving the Collective Communication Algorithm.

Here HPC-X gives 29.89% improvement for 32 nodes.
![[Pasted image 20241108222801.png]]
However for NSCC, HPC-X does not get significant improvement in NSCC. It only cause 1.78% improvement for 32 nodes. We gauss that it may be the cause of Hardware like the bandwith limit from infiniband.
![[Pasted image 20241108222843.png]]
### O3 Compilation
Next we use O3 compiler flags to get 5 more percent optimization. O3 flags will help do optimizations like **Loop unrolling**, **Vectorization** and **Instruction reordering**. Also, we try to use `-march=native` which would generate code optimized for CPU microarchitecture, enabling features like **AVX2**, **FMA** (Fused Multiply-Add), and other instruction sets on the nodes.

![[Pasted image 20241108222426.png]]




## Optimal UCX params

A core component of HPC-X is **UCX (Unified Communication X)**, which is a high-performance communication framework that supports multiple network interfaces, including InfiniBand, Ethernet, and other high-speed networks. UCX offers low-latency and high-bandwidth communication, making it suitable for large-scale parallel applications.

UCX_TLS refers to the "Transport Layer Selection" feature in the Unified Communication X (UCX) framework. It allows users to specify which transport protocols UCX should use for communication in a parallel or distributed computing environment.

![[Pasted image 20241108223039.png]]


We test multi combination of UCX_TLS to get better performance. Here we test UCX_TLS in bottleneck scale 16nodes.

| Params | Description                                                     |
| ------ | --------------------------------------------------------------- |
| all    | use all the available transports                                |
| sm     | all shared memory transports                                    |
| rc     | reliable connection                                             |
| ud     | unreliable datagram transport                                   |
| dc     | Mellanox scalable offloaded dynamic con_x0002_nection transport |

![[Pasted image 20241108223507.png]]
Here from the figure we find that `shm` combine with `dc_x` may best out perform the benchmark with 4740.571( the third one on performance. `dc_x` in UCX refers to the dynamic connected transport mode, used for reliable, connection-oriented communication between nodes in a distributed system. It utilizes RDMA like InfiniBand  for high-throughput, low-latency communication, with direct memory access and minimal CPU involvement.

However, `shm` combine with `dc_x` does not have much improvements in both ompi and hpcx.

![[Pasted image 20241108223615.png]]

And as for NSCC, we test multi combination of UCX_TLS to get better performance.
![[Pasted image 20241108223812.png]]

And the best parameter is `shm` combine with `ud_mlx5`. `ud_mlx5` is a transport mode in UCX that enables connectionless communication (UD) using the Mellanox mlx5 driver, leveraging RDMA capabilities for low-latency, high-throughput data transfer.

Here we get 45.3% performance improvement with ompi and 44.0% with hpcx in 32 nodes. UCX gets high improvement for NSCC cluster with different parameter.

![[Pasted image 20241108223849.png]]

![[Pasted image 20241108224322.png]]

![[Pasted image 20241108224914.png]]

The reason may due to a faster communication between nodes. With less buffer on UCX framework and high affinity with Hardware, the time of `MPI_Waitall` dropped, and the time in `MPI_AllReduce` dropped significantly too.
![[Pasted image 20241108224446.png]]


### Better buffer parameters

Buffer is a params to set the neighbor list buffer distance in hoomd.
The neighbor list recomputes itself more often when buffer is small, and the pair force computation takes more time when buffer is large.

![[Pasted image 20241108224711.png]]

Here we test different buffer across nodes to find out which value of buffer suits best.
![[Pasted image 20241108224726.png]]

![[Pasted image 20241108224934.png]]


![[Pasted image 20241108225039.png]]

![[Pasted image 20241108225053.png]]




![[Pasted image 20241108225105.png]]



### Summary

So in summary, we take different optimization on Qiming2.0, Gadi and NSCC. The chart shows our optimization and our future work.
![[Pasted image 20241108230335.png]]


And that will be the end of our HPC profiling.

<div STYLE="page-break-after: always;"></div>

## AI Llama 2

LitGPT Llama2 is a specialized integration of Llama 2, a powerful language model developed by Meta. With LitGPT, a framework designed to enable fine-tuning and customization of large language models for specific tasks or domains.

### Testing Platform

![[Pasted image 20241108232359.png]]
<div STYLE="page-break-after: always;"></div>

## Reference

[1] Anderson, J. A., Glaser, J., and Glotzer, S. C. 2019. HOOMD-blue: A Python package for high-performance molecular dynamics and hard particle Monte Carlo simulations. *arXiv preprint arXiv:1308.5587*. Retrieved from https://arxiv.org/abs/1308.5587

[2] P. Shamis _et al_., "UCX: An Open Source Framework for HPC Network APIs and Beyond," _2015 IEEE 23rd Annual Symposium on High-Performance Interconnects_, Santa Clara, CA, USA, 2015, pp. 40-43, doi: 10.1109/HOTI.2015.13.

[3] Andi Drebes, Antoniu Pop, Karine Heydemann, Nathalie Drach, and Albert Cohen. 2016. NUMA-aware scheduling and memory allocation for data-flow task-parallel applications. SIGPLAN Not. 51, 8, Article 44 (August 2016), 2 pages. https://doi.org/10.1145/3016078.2851193

[4] PAC: Preference-Aware Co-location Scheduling on Heterogeneous NUMAArchitectures To Improve Resource Utilization (ICS 23)

[5] Domain Decomposition. David E. Keyes. Department of Applied Physics & Applied Mathematics Columbia University [Technologies and Tools for High-Performance Distributed Computing](https://csweb-prod.cs.princeton.edu/picasso/seminarsF04/Keyes.pdf)

[6] An Introduction to Domain Decomposition Methods Algorithms, Theory, and Parallel Implementation. Victorita Dolean, Pierre Jolivet, Frédéric Nataf. [OT144DoleanJolivetNataf_full.pdf](https://www.ljll.fr/nataf/OT144DoleanJolivetNataf_full.pdf)

[7] Scheduling NUMA-aware workloads. Redhat Document [Chapter 9. Scheduling NUMA-aware workloads | Red Hat Product Documentation](https://docs.redhat.com/en/documentation/openshift_container_platform/4.14/html/scalability_and_performance/cnf-numa-aware-scheduling#cnf-numa-aware-scheduling)

[8] Andi Drebes, Antoniu Pop, Karine Heydemann, Nathalie Drach, and Albert Cohen. 2016. NUMA-aware scheduling and memory allocation for data-flow task-parallel applications. SIGPLAN Not. 51, 8, Article 44 (August 2016), 2 pages. https://doi.org/10.1145/3016078.2851193

[9] NVIDIA A100 Tensor Core GPU Architecture [nvidia-ampere-architecture-whitepaper.pdf](https://images.nvidia.cn/aem-dam/en-zz/Solutions/data-center/nvidia-ampere-architecture-whitepaper.pdf)

[10] Cowan, M., Maleki, S., Musuvathi, M., Saarikivi, O., and Xiong, Y. 2022. GC3: An Optimizing Compiler for GPU Collective Communication. arXiv:2201.11840 [cs.DC]. https://arxiv.org/abs/2201.11840.

[11] Zixian Cai, Zhengyang Liu, Saeed Maleki, Madanlal Musuvathi, Todd Mytkowicz, Jacob Nelson, and Olli Saarikivi. 2021. Synthesizing optimal collective algorithms. In Proceedings of the 26th ACM SIGPLAN Symposium on Principles and Practice of Parallel Programming (PPoPP '21). Association for Computing Machinery, New York, NY, USA, 62–75. https://doi.org/10.1145/3437801.3441620


