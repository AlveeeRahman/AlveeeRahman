<p align="center">
  <img src="assets/banner.png" alt="Alve Rahman Akash. PhD student in EECS at the University of Missouri. Research interests include the Benefit of Humanity, Quantum Computing and Edge AI." width="100%">
</p>

# Alve Rahman Akash

I am a PhD student in electrical engineering and computer science at the University of Missouri, in [Taesic Kim's group](https://sites.google.com/view/taesickim/people). My research puts quantum machine learning to work on power hardware: battery health monitoring on a quantum annealer, malware detection for smart grid devices with a quantum convolutional network, feature selection for electric vehicle batteries with quantum restricted Boltzmann machines. Four years of this has taught me that the quantum part is the easy half. Getting a result that survives an adversarial input, a small edge device, or a reviewer is the work.

The second thread here is tooling for Claude Code, built around one habit: verify what a chat model would otherwise just assert.

## What I build

| | Project | What it does |
|---|---|---|
| <img src="https://raw.githubusercontent.com/AlveeeRahman/research-hound/main/docs/assets/icon.png" width="44" alt=""> | [research-hound](https://github.com/AlveeeRahman/research-hound) | A five-stage research workflow for Claude Code, from question to rubric score, with 21 scripts that verify citations, audit claims and lint manuscripts instead of trusting the model. |
| <img src="https://raw.githubusercontent.com/AlveeeRahman/skill-vision/main/docs/assets/icon.png" width="44" alt=""> | [skill-vision](https://github.com/AlveeeRahman/skill-vision) | A validator for Claude Agent Skills: spec conformance, script execution, quality and security scores, a Mermaid map of the skill, and the context tokens each skill costs. Zero dependencies. |
| <img src="https://raw.githubusercontent.com/AlveeeRahman/agent-oracle/main/docs/assets/icon.png" width="44" alt=""> | [agent-oracle](https://github.com/AlveeeRahman/agent-oracle) | Decides how an agent system should be built before it runs: how many agents, which topology, what bounds the loop, what gets locked down before unattended work starts. Cites the papers it leans on. |
| <img src="https://raw.githubusercontent.com/AlveeeRahman/mr-usage/main/docs/assets/icon.png" width="44" alt=""> | [mr-usage](https://github.com/AlveeeRahman/mr-usage) | A Rust and Tauri desktop app that shows what is left on nine paid APIs in one window. Keys live in the OS keystore and never reach the UI. 109 tests on three operating systems. |
| <img src="https://raw.githubusercontent.com/AlveeeRahman/llm-dogfight/main/docs/assets/icon.png" width="44" alt=""> | [llm-dogfight](https://github.com/AlveeeRahman/llm-dogfight) | Two small local language models command rival saucer teams in your terminal. A 0.8 MB Rust binary, a Python sidecar on CUDA or Apple MLX, and a genetic algorithm that evolves each team's doctrine. |

NVIDIA SkillSpector scans the three skills on every push, and each ships with a `.skillspector-baseline.yaml` that names every suppressed finding and why.

## How I work with Claude

My Claude Code sessions run in the cloud with a short rulebook that Claude reads before anything else.

- Anything that touches the live web goes through agent-reach: SerpApi answers which pages rank, Firecrawl reads the page, and its developer, research and government indexes handle code, papers and law. The built-in search stays off unless I ask for it, because I want results I can audit.
- Every draft that leaves a session passes through humanizer, and anything that looks too confident gets hall-hunter, which has to name the file, line and contradicting fact for every finding or report it as unverified.
- Skills get validated by skill-vision before they ship. Agent designs start with agent-oracle's four questions. Papers go through research-hound, which checks that each DOI resolves and that its metadata matches the citation.
- The quantum-computing skill covers Qiskit, PennyLane, QuTiP and D-Wave Ocean, which is where the power systems work and the Claude work meet.

Connectors wired into those sessions: GitHub, Firecrawl, SerpApi, Higgsfield, Replit and Claude Docs, plus the keys mr-usage was written to watch: Elicit, Context7, Tavily, OpenRouter, Apify, Hunter and Runway.

The icons on the five repositories above came out of one such session. Firecrawl read each project page, Higgsfield rendered the marks on the same near-black tile as the mr-usage app icon, Claude Design laid out the family, and Claude Code pushed the commits.

## Papers

Eight papers, 37 citations and an h-index of 4 as of October 2026 ([Google Scholar](https://scholar.google.com/citations?user=wRWUQQYAAAAJ)).

- [Quantum-Inspired Machine Learning for Energy Efficient and Secure Battery Health Monitoring](https://doi.org/10.1109/pesgm52009.2025.11225365). IEEE PES General Meeting, 2025.
- [Quantum Restricted Boltzmann Machines-Based Feature Selection for Electric Vehicle Battery Health Monitoring](https://doi.org/10.1109/itec63604.2025.11098077). IEEE ITEC and EATS, 2025.
- [Quantum-Inspired Machine Learning Framework using a Physics-based Ising Solver Chip](https://doi.org/10.1109/icps59941.2024.10639986). IEEE ICPS, 2024.
- [Quantum Annealing-Based Machine Learning for Battery Health Monitoring Robust to Adversarial Attacks](https://doi.org/10.1109/ecce53617.2023.10362215). IEEE ECCE, 2023.
- [Quantum Convolutional Neural Network-based Online Malware File Detection for Smart Grid Devices](https://doi.org/10.1109/dmc58182.2023.10412597). IEEE DMC, 2023.
- [Online Battery Data Analytics Pipeline using Bigdata Tools for Electric Vehicles](https://doi.org/10.23919/icpe2023-ecceasia54778.2023.10213616). ICPE 2023 and ECCE Asia, 2023.
- [Device-centric ransomware detection using machine learning-based memory forensics for smart inverters](https://scholar.google.com/citations?view_op=view_citation&hl=en&user=wRWUQQYAAAAJ&citation_for_view=wRWUQQYAAAAJ:UeHWp8X0CEIC). Industrial Control System Security Workshop, 2022.
- [A Novel Mechanism Design Technique To Develop A Vertical Climbing Robot With High Mobility For Flat And Spherical Surfaces](https://doi.org/10.1109/icrest51555.2021.9331113). ICREST, 2021.

## Find me

[ORCID](https://orcid.org/0009-0008-8454-6516) · [Google Scholar](https://scholar.google.com/citations?user=wRWUQQYAAAAJ) · [LinkedIn](https://www.linkedin.com/in/alvieee/) · [alveeerahman.github.io/research-hound](https://alveeerahman.github.io/research-hound/)
