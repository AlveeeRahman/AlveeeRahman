<p align="center">
  <img src="assets/banner.png" alt="Alve Rahman. PhD student in EECS. Research interests include the Benefit of Humanity, Quantum Computing and Edge AI." width="100%">
</p>

# Alve Rahman

I have been working with AI since 2020, but never got the time to create a git for myself, so here I am. The below thread here are some tooling for Claude Code and some fun apps, I built around one habit, since the inception of LLMs: verify what a chat model would otherwise just assert.

## What I build

<table>
<tr>
<td width="72" align="center" valign="middle"><a href="https://github.com/AlveeeRahman/research-hound"><img src="https://raw.githubusercontent.com/AlveeeRahman/research-hound/main/docs/assets/icon.png" width="48" height="48" alt="research-hound icon"></a></td>
<td valign="middle"><a href="https://github.com/AlveeeRahman/research-hound"><b>research-hound</b></a><br>A five-stage research workflow for Claude Code, with 21 scripts that check citations and claims instead of trusting the model.</td>
</tr>
<tr>
<td width="72" align="center" valign="middle"><a href="https://github.com/AlveeeRahman/skill-vision"><img src="https://raw.githubusercontent.com/AlveeeRahman/skill-vision/main/docs/assets/icon.png" width="48" height="48" alt="skill-vision icon"></a></td>
<td valign="middle"><a href="https://github.com/AlveeeRahman/skill-vision"><b>skill-vision</b></a><br>Validates Claude Agent Skills for spec conformance, quality and security, and counts the context tokens each one costs.</td>
</tr>
<tr>
<td width="72" align="center" valign="middle"><a href="https://github.com/AlveeeRahman/agent-oracle"><img src="https://raw.githubusercontent.com/AlveeeRahman/agent-oracle/main/docs/assets/icon.png" width="48" height="48" alt="agent-oracle icon"></a></td>
<td valign="middle"><a href="https://github.com/AlveeeRahman/agent-oracle"><b>agent-oracle</b></a><br>Decides how an agent system should be built before it runs, from the number of agents to what gets locked down.</td>
</tr>
<tr>
<td width="72" align="center" valign="middle"><a href="https://github.com/AlveeeRahman/mr-usage"><img src="https://raw.githubusercontent.com/AlveeeRahman/mr-usage/main/docs/assets/icon.png" width="48" height="48" alt="mr-usage icon"></a></td>
<td valign="middle"><a href="https://github.com/AlveeeRahman/mr-usage"><b>mr-usage</b></a><br>A Rust and Tauri desktop app that shows what is left on nine paid APIs, with keys kept in the OS keystore.</td>
</tr>
<tr>
<td width="72" align="center" valign="middle"><a href="https://github.com/AlveeeRahman/llm-dogfight"><img src="https://raw.githubusercontent.com/AlveeeRahman/llm-dogfight/main/docs/assets/icon.png" width="48" height="48" alt="llm-dogfight icon"></a></td>
<td valign="middle"><a href="https://github.com/AlveeeRahman/llm-dogfight"><b>llm-dogfight</b></a><br>Two small local language models command rival saucer fleets in your terminal while a genetic algorithm evolves their tactics.</td>
</tr>
</table>

NVIDIA SkillSpector scans the three skills on every push, and each ships with a `.skillspector-baseline.yaml` that names every suppressed finding and why.

## In the works

Three of my own, still in active development.

<table>
<tr>
<td width="72" align="center" valign="middle"><a href="https://tigerocr.buildforpeople.dev"><img src="assets/tigerocr.png" width="48" height="48" alt="TigerOCR icon"></a></td>
<td valign="middle"><a href="https://tigerocr.buildforpeople.dev"><b>TigerOCR</b></a> &nbsp;<code>beta</code><br>Hosted GPU OCR that turns PDFs and images into clean Markdown, as a remote MCP server and REST API.</td>
</tr>
<tr>
<td width="72" align="center" valign="middle"><a href="https://github.com/AlveeeRahman/OpenCarMind"><img src="assets/opencarmind.png" width="48" height="48" alt="OpenCarMind icon"></a></td>
<td valign="middle"><a href="https://github.com/AlveeeRahman/OpenCarMind"><b>OpenCarMind</b></a> &nbsp;<code>beta</code><br>A car logger for the ESP32-S3 with a 93 KB on-chip neural network and a desktop app for Windows, macOS and Linux.</td>
</tr>
<tr>
<td width="72" align="center" valign="middle"><img src="assets/murasaki.png" width="48" height="48" alt="Murasaki icon"></td>
<td valign="middle"><b>Murasaki</b> &nbsp;<code>invite only</code><br>A purple-team platform for authorized security research, with AI-driven reverse engineering and ICS threat modeling.</td>
</tr>
</table>

## How I work with Claude

My Claude Code sessions run in the cloud with a short rulebook that Claude reads before anything else.

- Anything that touches the live web goes through agent-reach: SerpApi answers which pages rank, Firecrawl reads the page, and its developer, research and government indexes handle code, papers and law. The built-in search stays off unless I ask for it, because I want results I can audit.
- Every draft that leaves a session passes through humanizer, and anything that looks too confident gets hall-hunter, which has to name the file, line and contradicting fact for every finding or report it as unverified.
- Skills get validated by skill-vision before they ship. Agent designs start with agent-oracle's four questions. Papers go through research-hound, which checks that each DOI resolves and that its metadata matches the citation.
- The quantum-computing skill covers Qiskit, PennyLane, QuTiP and D-Wave Ocean, which is where the power systems work and the Claude work meet.

The icons on the five repositories above came out of one such sessions (Clearly I am no Photo Editor). Firecrawl read each project page, Higgsfield rendered the marks on the same near-black tile as the mr-usage app icon, Claude Design laid out the family, and Claude Code pushed the commits.

## Google Scholar

<a href="https://scholar.google.com/citations?user=wRWUQQYAAAAJ"><img src="assets/scholar.png" alt="Google Scholar as of October 2026: 37 citations, h-index 4. Citations per year: 4 in 2023, 5 in 2024, 15 in 2025, 13 in 2026." width="100%"></a>

## Find me

[LinkedIn](https://www.linkedin.com/in/alvieee/) · [Google Scholar](https://scholar.google.com/citations?user=wRWUQQYAAAAJ)
