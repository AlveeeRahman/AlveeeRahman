<p align="center">
  <img src="assets/banner.png" alt="Alve Rahman Akash. PhD student in EECS at the University of Missouri. Research interests include the Benefit of Humanity, Quantum Computing and Edge AI." width="100%">
</p>

# Alve Rahman Akash

Research interests include the Benefit of Humanity, Quantum Computing and Edge AI.

I have worked with AI for four years, and the knowledge behind it was tested the slow way, through graduate coursework across a master's and a PhD in quantum annealing, quantum optimization and artificial intelligence. The part of machine learning I care about is the optimization inside it. I cast pieces of a learning pipeline, feature selection and the training of restricted Boltzmann machines among them, as Ising problems and run them on a quantum annealer, then check how the result holds up when the input is adversarial or the device is small.

My research group pairs that with on-device optimizers, physics-based Ising solver chips that run the same formulations at the edge, next to the battery or the inverter, with no cloud in the loop. The aim is twofold, faster quantum machine learning, and control and optimization loops for power systems and power electronics that can run on the hardware they govern.

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

## Find me

[LinkedIn](https://www.linkedin.com/in/alvieee/) · [Skill Vision](https://alveeerahman.github.io/skill-vision/) · [Agent Oracle](https://alveeerahman.github.io/agent-oracle/) · [Research Hound](https://alveeerahman.github.io/research-hound/)
