[toc]

# LitGPT Llama2 Task Description

## 1. Task workload and input dataset

Participants are required to optimize the following workload for improved performance.

## Workload Profile

- **Workload**: [Llama-2-7b finetune-full](https://github.com/Lightning-AI/litgpt/blob/main/config_hub/finetune/llama-2-7b/full.yaml)
- **Max Seq Length**: 512
- **Number of Epochs**: 1
- **Dataset**

| Supercomputer | NCI Gadi iterations     | Gadi Baseline     | NSCC SG Aspire-2A iterations | Aspire-2A Baseline |
| ------------- | ----------------------- | ----------------- | ---------------------------- | ------------------ |
| **Dataset**   | `Alpaca1024/train.json` | 421.66s / 422.16s | `Alpaca1024/train.json`      | 41.42s / 41.51s    |

## 2. Submission and Presentation

- Prepare presentation slides for your team’s interview based on your application tuning work.
- Include a comparison with the provided baseline performance in your presentation slides.
- Submit the `build scripts`, `setup scripts`, `run scripts`, `LitGPT configuration file`, and `output text` files that support your presentation(e.g., *.stdout, *.o{jobid}, etc.).
- Do **not** submit the large model files.

## 3. Rules

- Participants need to run the task on `2 servers, each equipped with 4 GPUs`.
- Participants are not allowed to make any changes to the model itself.
- Grading will be based on the `optimization method` and the `performance improvement` achieved.

## 4. General Rules

- **Cluster Usage**: All HPC and AI tasks must be optimized on either the NCI or NSCC SG supercomputers. Teams can choose which tasks to optimize on which supercomputer. Additionally, teams may present optimization work done on other supercomputers as extra information.
- **Evaluation Criteria**: The judging panel will assess each team’s methods for optimizing cluster application throughput. Teams must clearly explain and demonstrate the performance improvements achieved through their optimization techniques, showing a solid understanding of their methods.
- **System Reliability**: Teams do not need to worry about system maintenance. If either the NCI or NSCC SG supercomputer is down for maintenance, teams can switch to the other operational system to continue their optimization work, ensuring the competition runs smoothly.
- **Performance Assessment**: The absolute performance metrics of NCI and NSCC SG will not be directly compared. These metrics will indicate the effectiveness of the system tuning and will be a significant factor in the judges’ scoring. However, they will not be the only criteria for ranking teams.
- **Scoring Flexibility**: When performance metrics are close, the judges will consider how well teams understand and explain their optimization process. This ensures that both technical results and the team’s comprehension are fairly evaluated.

