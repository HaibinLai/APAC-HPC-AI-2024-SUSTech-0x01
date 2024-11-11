import argparse

def generate_rankfile(nodes, ranks_per_node, cores_per_node):
    rankfile_lines = []
    rank = 0

    for node in nodes:
        for core in range(ranks_per_node):
            # for each MPI rank, assign it to a slot on the node
            rankfile_lines.append(f"rank {rank}={node} slot={rank % 2}")
            rank += 1

    return rankfile_lines

def save_rankfile(filename, rankfile_lines):
    with open(filename, 'w') as f:
        for line in rankfile_lines:
            f.write(line + '\n')
    print(f"Rankfile saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Generate an MPI Rankfile")
    parser.add_argument('--nodes', nargs='+', required=True, help='List of node hostnames')
    parser.add_argument('--ranks-per-node', type=int, required=True, help='Number of ranks per node')
    parser.add_argument('--output', type=str, default='rankfile', help='Output rankfile name')

    args = parser.parse_args()

    # rankfile
    rankfile_lines = generate_rankfile(args.nodes, args.ranks_per_node, 24)

    # save rankfile
    save_rankfile(args.output, rankfile_lines)

if __name__ == "__main__":
    main()
