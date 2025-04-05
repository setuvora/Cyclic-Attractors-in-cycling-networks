
# Cyclic-Attractors-in-cycling-networks

The goal of this program is to systematically detect randomly generated boolean networks with natural cycling activity. Simple boolean networks have been sucessfully used to model complex dynamics in various biological systems with remarkable accuracy (e.g. [the cell cycle network in baker's yeast](https://www.pnas.org/doi/10.1073/pnas.0305937101) ).


The [previous program](https://github.com/setuvora/Oscillating-Boolean-Network-Generator) generated directed (+/-) and fully-connected random boolean networks. After simulating network dynamics by turning all nodes ON, cycling activity was determined heuristically by comparing the last two timesteps of each simulation - if they were unequal, the network was determined to cycle indefinitely. This method was accurate only with networks with few nodes. Larger networks evolve over many timesteps before reaching a steady-state (or attractor state), making it difficult to predict if they are cycling using this method.


## The current program determines network cycling algorithmically:

<table>
  <tr>
    <td align="center"> <br>
      (1) Generates a network (Fully connected: N=4 nodes, k=3 edges; Directed: +/-; No self-edges); visualized using <a href="https://pypi.org/project/networkx/">networkX</a><br>
      <br>
      <img src="https://github.com/user-attachments/assets/764d2de3-0f38-441f-a8f8-fb8813129d35" width="300" />
    </td>
    <td align="center">
      (2) Calculates every possible state of the network at T₀, and computes every resulting state at T₁<br>
      <br>
      <img src="https://github.com/user-attachments/assets/5d3f270c-d1a7-4a1e-b41a-d81cb2fa146c" width="900" />
    </td>
  </tr>
  <tr>
    <td align="center">
      (3) Uses this state-transition space to construct an attractor graph (Kauffman, 1969; Hopfield, 1982)<br>
      <br>
      <img src="https://github.com/user-attachments/assets/f6a059cc-9f5b-4e06-8f72-989016cead30" width="350" />
    </td>
    <td align="center">
      (4) Uses graph theory to determine the Strongest Connected Component, SCC (Tarjan, 1972; <a href="https://pypi.org/project/networkx/">networkX</a>)<br>
      If SCC > 1, the network is capable of indefinite cycling.<br>
      <br>
      <img src="https://github.com/user-attachments/assets/84f9b4f0-9d8c-446e-8306-e87157f82937" width="200" />
    </td>
  </tr>
</table>

---


<td align="center"> <strong> The cycling periodicity of a boolean network is equal to the SCC of its corresponding attractor network (S.A. Kauffman, 1969) .. </strong> </td>
<br><br>
<table>
  <tr>
    <td align="center">(1) Take for example this randomly generated cycling network .. </td>
    <td align="center">(2) Here is a simulation of its network dynamics, showing a periodicity of 6 <br>(All nodes ON at T<sub>-1</sub>; Periodicity = 6) <br> Y-axis: Time | X-axis: Node States </td>
    <td align="center">(3) Here is its corresponging attractor graph with an SCC = 6 <br>SCC nodes in red</td>
  </tr>
  <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/0b01323a-c76e-44db-a726-273bd10e6590" width="300">
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/fcf45cb2-cb63-4011-b437-1d4e5cb11238" width="200">
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/d89675d4-72aa-411b-b24d-8a80b6d46ff5" width="300">
    </td>
  </tr>
</table>



F. Li, T. Long, Y. Lu, Q. Ouyang, & C. Tang, (2004) **The yeast cell-cycle network is robustly designed.** Proc. Natl. Acad. Sci. U.S.A. 101 (14) 4781-4786. 

Hagberg, Aric & Swart, Pieter & Chult, Daniel. (2008). **Exploring Network Structure, Dynamics, and Function Using NetworkX.** Proceedings of the 7th Python in Science Conference. 10.25080/TCWV9851. 

Hopfield, J. J. (1982). **Neural networks and physical systems with emergent collective computational abilities.** Proceedings of the National Academy of Sciences, 79(8), 2554–2558.

Kauffman, S. A. (1969). **Metabolic stability and epigenesis in randomly constructed genetic nets.** Journal of Theoretical Biology, 22(3), 437–467.

Tarjan, R. (1972). **Depth-First Search and Linear Graph Algorithms. SIAM Journal on Computing.** 1(2), 146–160.

