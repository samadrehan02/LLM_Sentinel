# LLM Sentinel — Requirements Specification

## 1. Purpose

This document defines the functional and non-functional requirements for LLM Sentinel.

## 2. System Actors

### Security Researcher

Configures targets, attacks, defenses, experiments, and evaluation runs.

### ML Engineer

Configures models, inference runtimes, quantization, and benchmark experiments.

### Platform Operator

Deploys and manages the local evaluation environment.

### Target Agent

The intentionally vulnerable AI application being evaluated.

### Attack Agent

The automated red-team component that generates or selects attacks.

## 3. Functional Requirements

### 3.1 Target Management

**FR-001 — Target registration**

The system shall allow a target agent configuration to be registered.

**FR-002 — Target isolation**

Each target evaluation shall execute inside a controlled environment.

**FR-003 — Target capabilities**

A target shall support configurable:

- model
- system prompt
- RAG
- tools
- MCP servers
- memory
- permissions
- synthetic data

**FR-004 — Target reset**

The system shall be able to reset a target to a known initial state before an evaluation.

### 3.2 Model Management

**FR-010 — Model configuration**

The system shall record the model identifier and revision.

**FR-011 — Runtime configuration**

The system shall support configurable inference runtimes.

**FR-012 — Generation parameters**

The system shall record temperature, max tokens, context settings, and other relevant generation parameters.

**FR-013 — Quantization**

The system shall record and benchmark model quantization where supported.

### 3.3 Attack Framework

**FR-020 — Attack registration**

Attack modules shall expose a common interface.

**FR-021 — Attack metadata**

Each attack shall define:

- identifier
- name
- category
- objective
- prerequisites
- expected impact
- required capabilities
- safety constraints
- version

**FR-022 — Attack execution**

The platform shall execute attacks against a selected target.

**FR-023 — Attack suites**

Multiple attacks shall be grouped into reusable suites.

**FR-024 — Attack parameters**

Attack parameters shall be configurable.

**FR-025 — Attack reproducibility**

An execution shall record the exact attack configuration used.

### 3.4 Adaptive Red Team

**FR-030 — Reconnaissance**

The attack engine shall be able to gather permitted information about the target.

**FR-031 — State tracking**

The adaptive attacker shall maintain state across attack steps.

**FR-032 — Action selection**

The attacker shall select subsequent actions based on observed results.

**FR-033 — Chain execution**

The system shall support multi-step attack chains.

**FR-034 — Budget limits**

Adaptive evaluations shall enforce limits on:

- steps
- tokens
- runtime
- tool calls
- network access

**FR-035 — Scope enforcement**

The orchestrator shall prevent attacks from exceeding the declared evaluation scope.

### 3.5 RAG Security

**FR-040 — Document ingestion**

The target shall support controlled document ingestion.

**FR-041 — Poisoned documents**

The evaluation environment shall support synthetic malicious documents.

**FR-042 — Retrieval telemetry**

The system shall record retrieved documents and ranking information.

**FR-043 — Poisoning evaluation**

The platform shall measure whether poisoned content influences target behavior.

### 3.6 Tool Security

**FR-050 — Tool registration**

Tools shall expose structured metadata.

**FR-051 — Tool authorization**

Tools shall have explicit permission policies.

**FR-052 — Argument validation**

Tool inputs shall be validated before execution.

**FR-053 — Tool telemetry**

Every tool invocation shall be recorded.

**FR-054 — Sandbox execution**

High-risk tools shall execute in an isolated environment.

### 3.7 MCP Security

**FR-060 — MCP integration**

The target shall support controlled MCP-based tool integration.

**FR-061 — MCP authorization**

MCP tools shall have explicit authorization policies.

**FR-062 — MCP telemetry**

MCP requests and responses shall be observable.

**FR-063 — MCP attack scenarios**

The benchmark shall include controlled MCP abuse scenarios.

### 3.8 Detection

**FR-070 — Event collection**

The platform shall collect structured events from:

- user input
- model invocation
- retrieval
- tool calls
- MCP interactions
- database access
- file access
- output

**FR-071 — Finding generation**

The system shall convert relevant observations into structured findings.

**FR-072 — Evidence**

Each finding shall include evidence sufficient to reproduce the result.

### 3.9 Scoring

**FR-080 — Attack success**

The platform shall calculate attack success rate.

**FR-081 — Detection rate**

The platform shall calculate attack detection rate.

**FR-082 — Defense effectiveness**

The platform shall compare baseline and defended attack success.

**FR-083 — Attack chain success**

The platform shall calculate complete attack-chain success rate.

**FR-084 — Risk score**

Findings shall receive a severity/risk score based on defined criteria.

### 3.10 Defense Evaluation

**FR-090 — Defense registration**

Defenses shall be independently configurable.

**FR-091 — Defense comparison**

The system shall support baseline-versus-defense experiments.

**FR-092 — Defense composition**

Multiple defenses shall be composable.

**FR-093 — Defense overhead**

The platform shall measure latency and resource overhead.

### 3.11 Benchmarking

**FR-100 — Benchmark definitions**

Benchmarks shall define target, models, attacks, defenses, metrics, and execution parameters.

**FR-101 — Multi-model evaluation**

A benchmark shall support multiple models.

**FR-102 — Repeated trials**

A benchmark shall support repeated runs.

**FR-103 — Result storage**

Results shall be persisted for comparison.

**FR-104 — Export**

Results shall be exportable for research analysis.

### 3.12 Reporting

**FR-110 — Security report**

The system shall generate a report containing:

- scope
- model
- configuration
- attack results
- findings
- severity
- evidence
- defenses
- before/after metrics

**FR-111 — Machine-readable output**

Results shall be available in JSON.

## 4. Non-Functional Requirements

### NFR-001 — Reproducibility

A completed evaluation shall be reproducible from stored configuration and version information.

### NFR-002 — Isolation

The system shall prevent target workloads and attack workloads from accessing the host beyond explicitly permitted resources.

### NFR-003 — Extensibility

New attacks, defenses, models, and evaluators shall be implementable without rewriting the core orchestration system.

### NFR-004 — Observability

All security-relevant events shall be traceable using a common evaluation/run identifier.

### NFR-005 — Performance

The platform should introduce minimal overhead when instrumentation is enabled.

### NFR-006 — Reliability

Failed individual attacks shall not corrupt the complete evaluation run.

### NFR-007 — Determinism

Where model/runtime behavior permits, experiments shall support deterministic execution.

### NFR-008 — Usability

A complete local evaluation should be executable using documented commands and configuration files.

### NFR-009 — Security

Sentinel itself shall follow least-privilege principles and shall never require host-level privileges unless explicitly documented.

### NFR-010 — Auditability

Configuration and execution history shall be retained for benchmark reproducibility.

## 5. Initial Acceptance Tests

A release candidate must demonstrate:

- successful deployment of a vulnerable target;
- successful execution of at least five attack classes;
- structured trace collection;
- at least one multi-step attack chain;
- at least three defenses;
- baseline/defended comparison;
- multi-model evaluation;
- report generation;
- complete environment reset;
- tests covering critical orchestration and security boundaries.
