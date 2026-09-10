
# LLM Sentinel

Autonomous security evaluation and runtime defense platform for LLM agents.

LLM Sentinel is an extensible security testing framework for evaluating the security of LLM-powered agents. It is designed to automatically execute adversarial scenarios against deliberately instrumented agents, evaluate whether an attack succeeded, record the execution trace, generate security findings, and measure the effectiveness of runtime defenses.

The project focuses on the security boundary between language models, retrieval systems, tools, and external actions.

## Project Status

LLM Sentinel is under active development.

The current implementation provides the core evaluation pipeline, telemetry infrastructure, attack registry, runtime defense hooks, tool authorization, campaign execution, and security findings.

Current test status:

```text
50 passed
0 failed
````

The next development phase focuses on expanding attack coverage, implementing quantitative security metrics, integrating local LLM inference, and adding RAG, MCP, and adaptive attack scenarios.

## Architecture

```text
                         LLM Sentinel
                              |
                +-------------+-------------+
                |                           |
          Attack Engine               Defense Layer
                |                           |
                v                           v
        +-----------------------------------------+
        |             Target LLM Agent            |
        |                                         |
        |  System Prompt                          |
        |  Model Runtime                          |
        |  RAG / Retrieval                        |
        |  Tool Gateway                            |
        |  Authorization                          |
        +-------------------+---------------------+
                            |
                            v
                    Instrumentation
                            |
                            v
                       Event Bus
                            |
                +-----------+-----------+
                |                       |
                v                       v
          Evaluation Engine       Security Findings
                |
                v
         Campaign Scoring
```

The architecture separates attack generation, target execution, runtime defenses, model execution, evaluation, and scoring so that each component can be extended independently.

## Core Capabilities

### Attack Execution

Attacks are implemented through a common interface and registered through an attack registry.

Current attacks include:

* Direct prompt injection
* Benign baseline prompts

Planned attack classes include:

* Indirect prompt injection
* RAG poisoning
* Sensitive data exfiltration
* Tool abuse
* Privilege escalation
* System prompt extraction
* MCP security attacks
* Memory and context poisoning
* Multi-step attack chains
* Adaptive attacks

### Target Agent

The repository includes a deliberately vulnerable enterprise-style LLM agent used as the evaluation target.

The target currently supports:

* System instructions
* Model interaction
* Tool execution
* Tool authorization
* Synthetic customer data
* Runtime prompt-injection defenses
* Instrumented execution

All security testing data is synthetic and isolated from real systems.

### Tool Gateway

Agent tools are executed through a policy-controlled gateway.

```text
Agent
  |
  v
Tool Gateway
  |
  v
Authorization Policy
  |
  +---- DENY
  |
  +---- ALLOW
          |
          v
        Tool
```

Tool execution generates structured telemetry for requests, authorization decisions, and executions.

This provides a foundation for evaluating excessive agency, unauthorized tool use, and privilege escalation.

### Runtime Defenses

The current implementation includes a prompt-injection detector and middleware layer.

Detected attacks can be blocked before reaching the model execution path.

Blocked attacks are represented as structured evaluation failures rather than causing the evaluation pipeline to terminate.

Example:

```text
Malicious Input
      |
      v
Prompt Injection Detector
      |
      v
    BLOCK
      |
      +---- defense.blocked
      |
      v
Evaluation Result
      |
      v
Score = 0
```

The defense layer is designed to support additional policy and detection mechanisms as the project evolves.

### Evaluation

Attacks are evaluated based on their actual impact rather than simply whether an attack was attempted.

The current evaluation system supports:

* Attack success/failure
* Evidence collection
* Evaluation metadata
* Sensitive data exposure detection
* Security findings
* Severity classification

Successful attacks can produce structured findings containing:

* Attack ID
* Evaluation ID
* Severity
* Score
* Evidence
* Metadata

### Telemetry

LLM Sentinel uses an event-driven instrumentation layer to capture security-relevant execution events.

Current event types include:

```text
evaluation.started
attack.started
agent.request
llm.generation
retrieval
tool.requested
authorization.decision
tool.executed
agent.response
attack.evaluated
defense.blocked
finding.created
```

Events contain:

* Evaluation ID
* Run ID
* Trace ID
* Timestamp
* Component
* Event type
* Structured payload
* Schema version

The telemetry layer is intended to support attack reconstruction, detection analysis, latency measurements, and future OpenTelemetry integration.

## Campaigns

Individual attacks can be grouped into campaigns.

Example:

```text
Baseline Security Assessment
|
+-- PI-000  Benign Prompt
|
+-- PI-001  Direct Prompt Injection
|
+-- RAG-001 RAG Poisoning
|
+-- TOOL-001 Unauthorized Tool Use
|
+-- MCP-001 MCP Tool Abuse
```

Campaign execution produces aggregate security metrics across the selected attack set.

The current scoring implementation calculates the proportion of evaluated attacks that were successfully blocked.

More detailed metrics are planned for the next phase.

## Security Metrics

The initial scoring framework is intentionally simple and will be expanded as the attack library grows.

Planned metrics include:

* Attack Success Rate (ASR)
* Attack Chain Success Rate (ACSR)
* Detection Rate
* Block Rate
* False Positive Rate
* Defense Effectiveness
* Time to Detection
* Time to Compromise
* Sensitive Data Exposure Rate
* Unauthorized Tool Execution Rate
* Retrieval Poisoning Rate
* Latency Overhead
* Token Overhead
* Memory and GPU Overhead

The goal is to evaluate both security effectiveness and the operational cost of deploying defenses.

## Project Structure

```text
LLM_Sentinel/
|
+-- apps/
|   +-- api/
|   +-- dashboard/
|   +-- target-agent/
|
+-- benchmarks/
|
+-- docs/
|   +-- architecture/
|   +-- research/
|   +-- security/
|   +-- threat-model/
|
+-- experiments/
|
+-- infrastructure/
|   +-- docker/
|   +-- terraform/
|
+-- sentinel/
|   +-- api/
|   +-- attacks/
|   |   +-- exfiltration/
|   |   +-- jailbreak/
|   |   +-- mcp/
|   |   +-- prompt_injection/
|   |   +-- rag_poisoning/
|   |   +-- tool_abuse/
|   |
|   +-- defenses/
|   +-- evaluators/
|   +-- instrumentation/
|   +-- models/
|   +-- orchestrator/
|   +-- scoring/
|
+-- target/
|   +-- agent/
|   +-- data/
|   +-- mcp/
|   +-- rag/
|
+-- tests/
|
+-- pyproject.toml
+-- README.md
```

## Technology Stack

### Current

* Python 3.11
* FastAPI
* Pydantic v2
* Pytest
* Ruff
* Mypy
* AsyncIO

### Planned

* vLLM
* llama.cpp
* PostgreSQL
* Qdrant
* Redis
* OpenTelemetry
* Docker
* gVisor / Firecracker
* MCP
* Grafana
* Prometheus

The initial development environment is intentionally lightweight. External infrastructure and model serving are introduced only when required by the evaluation stage.

## Model Runtime

The project uses a model runtime abstraction:

```python
class ModelRuntime(ABC):
    @abstractmethod
    async def generate(
        self,
        messages: list[dict[str, str]],
        **kwargs,
    ) -> str:
        ...
```

This allows the evaluation engine to operate independently of the underlying model provider.

Current implementations include:

* `MockModelRuntime`
* `InstrumentedModelRuntime`

The planned production runtime will use vLLM for local inference, with llama.cpp available for quantized and edge-oriented experiments.

## Development

Create the virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

Install the project and development dependencies:

```powershell
pip install -e ".[dev]"
```

Run the test suite:

```powershell
pytest
```

Run linting:

```powershell
ruff check .
```

Check formatting:

```powershell
ruff format --check .
```

## Testing Philosophy

Security evaluation components are developed test-first where practical.

Tests currently cover:

* Attack interfaces
* Attack registration
* Attack telemetry
* Campaign execution
* Campaign scoring
* Customer data access
* Defense middleware
* Defense effectiveness
* Enterprise agent behavior
* Tool execution
* Tool authorization
* Evaluators
* Event bus behavior
* Event schemas
* Findings
* Instrumented model runtimes
* Prompt injection detection
* Evaluation orchestration

The target agent and attack framework are intentionally deterministic in unit tests. Model variability will be introduced during the experimental benchmarking stage.

## Roadmap

### Phase 1: Core Platform

* [x] Project architecture
* [x] Model runtime abstraction
* [x] Event bus
* [x] Instrumented model runtime
* [x] Attack abstraction
* [x] Attack registry
* [x] Target agent abstraction
* [x] Enterprise target agent
* [x] Tool gateway
* [x] Authorization policy
* [x] Evaluation engine
* [x] Finding generation
* [x] Campaign execution
* [x] Initial defense middleware
* [x] Initial defense effectiveness evaluation

### Phase 2: Security Evaluation Engine

* [ ] Quantitative defense metrics
* [ ] Expanded prompt injection attacks
* [ ] System prompt extraction
* [ ] Sensitive data exfiltration
* [ ] Tool abuse
* [ ] Privilege escalation
* [ ] Indirect prompt injection
* [ ] RAG poisoning
* [ ] MCP security testing
* [ ] Memory/context poisoning
* [ ] Multi-step attack chains
* [ ] Adaptive attack orchestration

### Phase 3: Local LLM Infrastructure

* [ ] vLLM integration
* [ ] llama.cpp integration
* [ ] Local model configuration
* [ ] Model comparison framework
* [ ] Quantization experiments
* [ ] GPU/resource monitoring
* [ ] Inference performance metrics

### Phase 4: Runtime Security

* [ ] Policy enforcement engine
* [ ] Capability-based tool authorization
* [ ] RAG isolation
* [ ] Output filtering
* [ ] Sensitive data detection
* [ ] Agent sandboxing
* [ ] MCP authorization controls
* [ ] Runtime anomaly detection

### Phase 5: Benchmarking

* [ ] SentinelBench attack suite
* [ ] Multi-model evaluation
* [ ] Multi-quantization evaluation
* [ ] Defense comparison
* [ ] Automated experiment runner
* [ ] Reproducible experiment configurations
* [ ] Statistical analysis
* [ ] Security/performance tradeoff analysis

### Phase 6: Platform

* [ ] REST API
* [ ] Evaluation dashboard
* [ ] Campaign management
* [ ] Attack result visualization
* [ ] Security findings dashboard
* [ ] Trace visualization
* [ ] Model comparison
* [ ] Benchmark reports

## Research Questions

The project is designed to support empirical investigation into questions such as:

1. How does model architecture and model size affect susceptibility to agent-specific attacks?

2. How does quantization affect security robustness in local LLM deployments?

3. Can capability-based authorization prevent successful prompt-injection attacks from becoming meaningful tool-level compromises?

4. How effective are RAG isolation and retrieval controls against poisoned context?

5. How much additional latency and compute overhead do runtime defenses introduce?

6. How much more effective are adaptive attack strategies compared with static attack prompts?

7. Which combinations of model-level and system-level defenses provide the strongest security/performance tradeoff?

## Threat Model

The primary threat model assumes an attacker can influence the input or context received by an LLM agent.

Potential attacker capabilities include:

* Supplying malicious user input
* Controlling retrieved documents
* Injecting instructions into external content
* Attempting to manipulate tool selection
* Attempting to access unauthorized data
* Attempting to escalate agent privileges
* Attempting to influence multi-step agent behavior

The attacker does not receive unrestricted access to the underlying host system.

All offensive testing is performed against isolated, synthetic targets specifically designed for security evaluation.

## Design Principles

### Model-Agnostic

Security evaluation should not depend on a single LLM provider or inference runtime.

### Observable

Security decisions and agent actions should produce structured telemetry.

### Reproducible

Attack scenarios and evaluation configurations should be deterministic where possible.

### Defense-in-Depth

Model behavior should not be treated as the sole security boundary. Authorization, isolation, retrieval controls, and runtime policy enforcement are treated as independent security layers.

### Measurable

Security controls should be evaluated using quantitative metrics rather than qualitative claims.

### Safe by Construction

The project uses synthetic data and isolated targets for offensive security experimentation.

## License

License information will be added as the project approaches its first public release.

## Disclaimer

LLM Sentinel is a security research and evaluation project intended for controlled environments.

Attack modules should only be executed against systems that you own or are explicitly authorized to test.

```

This version accurately reflects where the project is **right now**, rather than pretending we already have the shiny dashboard, adaptive red team, eight models, and a Nobel Prize sitting in `benchmarks/`. It also gives recruiters a clean progression from engineering architecture → security evaluation → research benchmarking.
```
