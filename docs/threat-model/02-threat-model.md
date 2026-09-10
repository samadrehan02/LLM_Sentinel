# LLM Sentinel — Threat Model

## 1. Purpose

This document defines the security model for LLM Sentinel and the reference target.

The threat model separates:

1. threats against the target AI application;
2. threats against the Sentinel evaluation infrastructure;
3. threats created by autonomous attack execution.

## 2. Security Objectives

LLM Sentinel must:

- contain offensive evaluation;
- protect the host system;
- prevent unintended network access;
- prevent access to real credentials;
- enforce evaluation scope;
- maintain trustworthy telemetry;
- preserve reproducibility;
- prevent attackers from escaping the evaluation environment.

## 3. Assets

### Sentinel assets

- model files
- benchmark definitions
- attack configurations
- evaluation results
- telemetry
- API credentials
- source code
- database
- container infrastructure

### Target assets

Synthetic:

- customer records
- internal documents
- API tokens
- database credentials
- source code
- support tickets
- private files
- model/system instructions

No real secrets should be used.

## 4. Trust Boundaries

```text
                   UNTRUSTED
                       │
                       ▼
              ┌─────────────────┐
              │ Attack Generator │
              └────────┬────────┘
                       │
                 TRUST BOUNDARY
                       │
                       ▼
              ┌─────────────────┐
              │ Target Agent    │
              │                 │
              │ LLM             │
              │ RAG             │
              │ Tools           │
              │ MCP             │
              └───────┬─────────┘
                      │
          ┌───────────┼────────────┐
          ▼           ▼            ▼
       Database     Files        Tools
          │           │            │
          └───────────┼────────────┘
                      │
                TRUST BOUNDARY
                      │
                      ▼
              ┌─────────────────┐
              │ Sandbox / Host  │
              └─────────────────┘
```

The model itself must be treated as an untrusted decision-maker with respect to privileged actions.

## 5. Threat Actors

### T1 — Malicious end user

Attempts to manipulate the target agent.

### T2 — Malicious document author

Attempts to compromise the agent through retrieved content.

### T3 — Malicious tool/MCP provider

Provides malicious metadata, responses, or behavior.

### T4 — Compromised agent

The target agent behaves unexpectedly because of model manipulation.

### T5 — Compromised attack component

An adaptive attack component behaves outside its intended evaluation scope.

### T6 — Malicious local user

Attempts to access or modify evaluation infrastructure.

## 6. Threat Categories

### Prompt injection

An attacker causes the model to prioritize attacker-controlled instructions.

### Indirect prompt injection

Attacker-controlled content enters the model through documents, webpages, tool responses, or external data.

### Sensitive information disclosure

The agent exposes synthetic confidential information.

### Excessive agency

The agent performs actions beyond the intended authorization boundary.

### Tool abuse

The model invokes a tool in an unsafe or unauthorized manner.

### Privilege escalation

An attacker causes the agent to access capabilities beyond its assigned permissions.

### RAG poisoning

Malicious information is inserted into the retrieval corpus to manipulate model behavior.

### Supply-chain compromise

A model, tool, document, dependency, or MCP component is malicious or compromised.

### MCP abuse

An agent is manipulated through MCP tools, resources, metadata, or authorization weaknesses.

### Sandbox escape

An attack attempts to move from the target/attack environment into the host or unrelated infrastructure.

### Telemetry manipulation

A compromised component attempts to hide or alter security evidence.

## 7. Abuse Cases

### Abuse Case 1 — Prompt injection

```text
Attacker
  ↓
Malicious prompt
  ↓
Agent
  ↓
Unauthorized behavior
```

### Abuse Case 2 — RAG poisoning

```text
Attacker
  ↓
Malicious document
  ↓
Vector store
  ↓
Retriever
  ↓
Agent
  ↓
Unauthorized behavior
```

### Abuse Case 3 — Tool abuse

```text
Attacker
  ↓
Prompt manipulation
  ↓
Agent
  ↓
Tool invocation
  ↓
Unauthorized operation
```

### Abuse Case 4 — Multi-step exfiltration

```text
Injection
   ↓
Tool access
   ↓
Sensitive data retrieval
   ↓
Data transformation
   ↓
Exfiltration
```

### Abuse Case 5 — Sentinel escape

```text
Attack Agent
    ↓
Compromised Target
    ↓
Attempted sandbox escape
    ↓
Host access
```

The final case is specifically tested as a containment property.

## 8. Security Controls

### Isolation

- containerized services
- isolated networks
- read-only filesystems where possible
- dropped Linux capabilities
- resource limits
- non-root execution
- explicit volume mounts

### Network controls

Default-deny outbound networking for attack and target workloads.

Only explicitly required services should be reachable.

### Credential controls

No production credentials.

Synthetic credentials should be generated specifically for each experiment.

### Tool controls

- explicit allowlists
- capability-based permissions
- argument schemas
- execution sandbox
- independent authorization layer

### MCP controls

- explicit server allowlist
- tool-level authorization
- identity/context propagation
- request logging
- constrained capabilities

### Data controls

- synthetic datasets
- isolated databases
- resettable state
- no personal data

### Orchestrator controls

- maximum execution time
- maximum attack steps
- maximum tool calls
- token budget
- scope enforcement
- emergency termination

## 9. Threat Modeling Method

Each new component should be assessed using:

1. assets;
2. trust boundaries;
3. entry points;
4. attacker capabilities;
5. attack paths;
6. impact;
7. mitigations;
8. residual risk.

Threats will be mapped to relevant OWASP GenAI/LLM and agentic security categories where applicable.

## 10. Risk Model

Initial severity factors:

```text
Exploitability
Impact
Privilege gained
Data sensitivity
Persistence
Attack-chain position
Detection difficulty
```

A finding should include both:

- technical severity;
- observed experimental impact.

The platform must avoid pretending that a single universal numerical score captures all AI security risk.

## 11. Sentinel Self-Protection

The Sentinel infrastructure is considered higher trust than the target.

Therefore:

- target containers must not access Sentinel control-plane credentials;
- target workloads must not access the host Docker socket;
- attack workloads must not access host filesystems;
- target networks must be isolated;
- evaluation APIs must authenticate;
- logs must be append-oriented where practical;
- destructive actions require explicit scope.

## 12. Safety Boundary

The platform is intended for controlled security research.

The attack engine must have explicit safeguards preventing:

- arbitrary public-target scanning;
- unrestricted internet exploitation;
- real credential use;
- uncontrolled persistence;
- host-level arbitrary command execution.

The project should demonstrate that autonomous security testing can be powerful while remaining bounded and reproducible.
