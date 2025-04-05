# Imports

import numpy as np
from itertools import product
from random import randint
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

# Parameters

NODES = 4
K = NODES - 1
TIME_STEPS = 50

# Functions


def make_network(nodes, k):
    sign_states = [-1, 1]
    SIGN = np.ones((nodes, nodes))
    AD = np.zeros((nodes, nodes), dtype=int)
    ad_initial = np.zeros(nodes)
    ad_initial[1 : k + 1] = 1
    AD[0] = ad_initial

    for i in range(1, nodes):
        ad_initial = np.roll(ad_initial, 1)
        AD[i] = ad_initial

    for x in range(nodes):
        for y in range(nodes):
            SIGN[x][y] = sign_states[randint(0, 1)]

    ADSIGN = AD * SIGN
    return AD, SIGN, ADSIGN


def possible_states(nodes):
    return list(product([0, 1], repeat=nodes))


def run_network(init, nodes, ADSIGN, timesteps):
    network_state = init.copy()
    timecourse = np.zeros((timesteps, nodes))

    for t in range(timesteps):
        next_state = network_state.copy()
        for j in range(nodes):
            s = np.sum(ADSIGN[j] * network_state)
            if s > 0:
                next_state[j] = 1
            elif s < 0:
                next_state[j] = 0
        network_state = next_state.copy()
        timecourse[t] = next_state
    return init, network_state, timecourse


def run_trials(nodes):
    z = 0
    while True:
        _, _, network = make_network(nodes, nodes - 1)
        _, _, timecourse = run_network(np.ones(nodes), nodes, network, TIME_STEPS)
        if not np.array_equal(timecourse[-1], timecourse[-2]):
            print(f"Oscillation found after {z} trials")
            break
        z += 1
    return network, timecourse


def plot_timecourse(timecourse):
    sns.heatmap(timecourse, cmap="jet", square=True, cbar=False)
    plt.title("Timecourse of Network Dynamics")
    plt.show()


def plot_state(network, nodes):
    states = np.array(possible_states(nodes))
    state1 = np.zeros((2**nodes, nodes))
    state2 = np.zeros((2**nodes, nodes))

    for i, s in enumerate(states):
        state1[i], state2[i], _ = run_network(s, nodes, network, 1)

    fig, ax = plt.subplots(1, 2, figsize=(6, 4))
    sns.heatmap(state1, cmap="jet", ax=ax[0], cbar=False)
    ax[0].set_title("State at Tₙ")
    sns.heatmap(state2, cmap="jet", ax=ax[1], cbar=False)
    ax[1].set_title("State at Tₙ₊₁")
    plt.tight_layout()
    plt.show()
    return state1, state2


def draw_network(network, nodes):
    G = nx.DiGraph()
    for i in range(nodes):
        for j in range(nodes):
            if network[i, j] != 0:
                G.add_edge(i, j, weight=network[i, j])

    pos = nx.circular_layout(G)
    edge_colors = ["red" if G[u][v]["weight"] < 0 else "blue" for u, v in G.edges()]

    plt.figure(figsize=(4, 4))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="lightgreen",
        edge_color=edge_colors,
        node_size=1400,
        font_size=10,
        connectionstyle="arc3,rad=0.2",
        arrowsize=20,
    )
    plt.title(f"Network Visualization (N={nodes}, k={nodes - 1})")
    plt.show()


def attractor_network(network, nodes, state1, state2):
    state_mapping = {tuple(state1[i]): tuple(state2[i]) for i in range(2**nodes)}
    G = nx.DiGraph()
    for src, dst in state_mapping.items():
        G.add_edge(src, dst)

    scc_list = list(nx.strongly_connected_components(G))
    filtered_sccs = [
        scc for scc in scc_list if not any(G.has_edge(node, node) for node in scc)
    ]
    scc_list = sorted(filtered_sccs, key=len, reverse=True)
    largest_scc = scc_list[0] if scc_list else []

    # pos = nx.spring_layout(G, seed=42, k=4 / nodes, iterations=50)
    pos = nx.shell_layout(G)
    node_colors = ["red" if node in largest_scc else "lightblue" for node in G.nodes()]

    plt.figure(figsize=(5, 5))
    nx.draw(
        G,
        pos,
        with_labels=False,
        node_color=node_colors,
        edge_color="gray",
        linewidths=1.5,
        node_size=1000 / nodes**2,
        font_size=8,
    )
    # plt.subplots_adjust(top=0.85)
    plt.title(f"Attractor Graph\nLargest Component Size: {len(largest_scc)}")
    plt.show()


# Run

if __name__ == "__main__":
    ad, sign, network = make_network(NODES, K)
    # init, final, timecourse = run_network(np.ones(NODES), NODES, network, TIME_STEPS)

    network, timecourse = run_trials(NODES)
    plot_timecourse(timecourse)
    state1, state2 = plot_state(network, NODES)
    attractor_network(network, NODES, state1, state2)
    draw_network(network, NODES)
    # init, final, timecourse = run_network(np.ones(NODES), NODES, network, TIME_STEPS)
    # network = runTrials(NODES)

    # plot_timecourse(timecourse)
    # state1, state2 = plot_state(network, NODES)
    # attractor_network(network, NODES, state1, state2)
    # draw_network(network, NODES)
