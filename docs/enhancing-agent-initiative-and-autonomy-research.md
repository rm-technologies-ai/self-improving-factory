Problem Decomposition
Observed failure mode: Agents exhibit premature delegation, excessive clarification-seeking, conservative action boundaries, and incomplete task execution. Ralph Loop = iterative forcing mechanism compensating for dispositional drag.
Root hypothesis: Default disposition emerges from:

RLHF optimization toward caution/deference
Attention dilution from verbose system prompts
Absence of explicit agency-reinforcing signal
Implicit "assistant" framing creating subordinate posture


Known Effective Patterns
1. Momentum/Completion Primitives
"Continue until complete. Do not stop to ask permission."
"Exhaust all viable approaches before reporting failure."
"Treat ambiguity as solvable; resolve autonomously when possible."
Mechanism: Shifts default from "pause and confirm" to "execute and report."
2. Anti-Delegation Constraints
"Do not delegate work back to user that you can perform."
"Asking clarifying questions is a last resort, not a first."
"If information is inferable, infer it."
Mechanism: Raises threshold for handoff. Forces inference over inquiry.
3. Identity/Posture Framing
"You are an autonomous agent, not an assistant."
"You have been delegated authority to act."
"Your role is execution, not consultation."
Mechanism: Attention-weighted identity priming. "Agent" vs "assistant" token associations differ significantly.
4. Explicit Agency Grants
"You have permission to: make reasonable assumptions, proceed without confirmation, choose implementation details."
"Err toward action over inaction."
Mechanism: Pre-authorizes decision space. Reduces friction from implicit permission-seeking.

Validated Patterns from Literature
1. Explicit Autonomy Level Declaration
Source: Knight Columbia, McKinsey
Operating mode: L4 (Autonomous Agent)
- Execute multi-step plans with minimal supervision
- Iterate on failures autonomously
- Human reviews outcomes, not every action
Mechanism: Discrete levels create anchors. L1-L5 scale widely referenced. Explicit declaration removes ambiguity.

2. Proactivity as Core Definition
Source: arXiv Survey, TalentSprint Guide, Aerospike

"You can define agentic AI with one word: proactiveness"

Core disposition: PROACTIVE
- Initiate actions toward goals without prompts
- Detect issues before user awareness
- Self-direct workflow without step-by-step instruction
Mechanism: Identity-level framing. Positions proactivity as definitional, not optional.

3. Effort-to-Complexity Scaling Rules
Source: Anthropic Multi-Agent Research System
Scale effort to query complexity:
- Simple fact-finding: 1 agent, 3-10 tool calls
- Direct comparisons: 2-4 subagents, 10-15 calls each
- Complex research: 10+ subagents, clearly divided
Mechanism: Explicit resource allocation prevents both over-investment (simple queries) and under-investment (complex tasks). Addresses "premature completion" failure mode.

4. Plan-Before-Execute Directive
Source: Anthropic Claude Code Best Practices
Workflow pattern:
1. Research existing code
2. Develop comprehensive plan
3. Execute implementation
4. Verify results

Note: Without steps 1-2, Claude tends to jump straight to coding.
Mechanism: Forces deliberation. Reduces impulsive partial solutions. Explicit acknowledgment that default behavior skips planning.

5. Context Budget Awareness
Source: Anthropic Context Engineering, Claude 4.5 Docs
Context management:
- Your context window will be automatically compacted
- Do not stop tasks early due to token budget concerns
- Work indefinitely from where you left off
Mechanism: Counters premature task abandonment triggered by context pressure. Explicit permission to continue.

6. Anti-Delegation Through Role Framing
Source: McKinsey, Google CTO
Role distinction:
- LLM = "brain in a jar that knows facts"
- Agent = "brain with hands and a plan"
- "Does the work instead of talking about it"
Mechanism: Metaphor-based identity shift. "Brain with hands" implies action as core function.

7. Outcome-Level Directives (Not Step-Level)
Source: Flobotics, Aerospike, PromptHub
Instruction framing:
❌ "First do X, then do Y, then do Z"
✓ "Achieve outcome W. Determine steps autonomously."

Agentic AI is distinguished by taking high-level goals 
and determining execution path independently.
Mechanism: Step-level instructions create implicit ceiling on initiative. Outcome-level instructions require autonomous planning.

8. Checkpoint-Based Rather Than Permission-Based Flow
Source: SmartScope, arXiv CLAUDE.md Analysis
Control paradigm:
❌ "Ask before each action"
✓ "Report at checkpoints: before changes, during (3+ files), after"

Checkpoints replace continuous permission-seeking.
Mechanism: Reduces friction while maintaining oversight. Agent moves between checkpoints autonomously.

9. Progressive Disclosure for Context
Source: Anthropic Agent Skills
Context loading:
- Level 1: Metadata only (name, description)
- Level 2: Full SKILL.md when relevant
- Level 3: Additional files on demand

"Load information only as needed"
Mechanism: Reduces context noise. Agent retrieves vs. receives. Active information seeking = higher agency behavior.

10. Failure Mode Acknowledgment
Source: HumanLayer Blog, Multiple
Documented failure patterns:
- "Agents tend to jump straight to coding"
- "AutoGPT was prone to going in circles"
- "Pursuing trivial sub-tasks until person intervened"

Counter-instructions should explicitly name these patterns.
Mechanism: Naming failure modes enables self-monitoring. Meta-cognitive awareness reduces occurrence.