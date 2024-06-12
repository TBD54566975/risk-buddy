# Evaluating rules

Currently evaluating rules against an approximate schema if it can match it. 

Big picture plan for how this fits in to risk buddy: 

1) we have some schema for expected data to risk scorer
2) we have some rules in structured format (similar to drl) that work over objects that match that schema
3) if the data coming in matches schema well, evaluate the rules (happy path)
4) Some rules can express things in a fuzzy way: ie perhaps it asks that a description is reasonable for an amount, something that is pretty clearly LLM territory (ie 500K for a sandiwch)
5) Data may come in which doesn't nearly match the schema, we can use LLMs (similar to what Mario showed) to match it into an object, and then eval rules (as above)
6) Some rules may be unexpressable in that rigorous logic way, in which case can be evaluated directly by an LLM to try to score