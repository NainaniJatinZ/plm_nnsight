# NNsight for Protein Language Models: ESM Tutorial

## 1 intro 

### Why nnsight? 
When I first started working on pLMs, most of the infra was built for LLMs. So the work we did for plm circuits was using pytorch hooks for caching and interventions. But interp infra has come a long way. One of the strongest examples is nnsight. So before I started a project on investigating pLMs further, I wanted to experiment and transfer all my tools to nnsight. This details my experience. 

### Why plm interp? 

This question demands a different post, and after working in this direction I have a lot of thoughts. But my reasoning boils down to: “On one hand, finding that the models are relying on incorrect patterns or spurious correlations is important for reliability and trust, as they are starting to be deployed in healthcare, drug design, and research among other things. On the other hand, finding that the models are finding patterns unknown to us can be the source of new scientific hypotheses.” 
But folks from goodfire have a more principled case for it: https://www.goodfire.ai/research/interpreting-evo-2# (look for “Why this matters”) 

### Contributions
- Show the convenience of starting a project, in the hopes we find more comp bio folks who want to understand their models 
- Solve any and all bugs / issues that come with bringing a protein model to this repo 
- Provide helpers if anything is missing from nnsight to complete the toolkit 
- Provide a notebook that showcases various capabilities and limitations 

## 2 Loading the model + setup 

## 3 Accessing activations + attention head visualization 

## 4 Sparse Autoencoders 

## 5 Replicating pLM circuits paper in nnsight 





