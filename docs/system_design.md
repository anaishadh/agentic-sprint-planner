## System Design Overview

### Why Multi-Agent?
Different stages of sprint planning require different kinds of reasoning, such as business understanding, task decomposition, and execution planning.

### Why State-Based Planning?
Sprint planning is iterative. Each step depends on the output of the previous step, which makes maintaining shared state important.

### Why LangGraph (Later)?
As the system grows, LangGraph can help orchestrate agent execution, control flow, and state transitions in a clean and debuggable way.
