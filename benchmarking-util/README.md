# Benchmarking utility script
Used for analysing agent logs benchmarking data. Need to use
the `benchmark.py` module when recording timers.

## Assumptions
- You have NodeJS installed
- Can use linux CLI features like pipes

## Getting started

```
npm install
npm start
```

## Usage

1. Insert benchmark utility in python script
2. Run the game
3. Retrieve the logs by typing `docker logs [container_id] > agent.logs`
4. Copy or move agent.logs into this directory (overwrite existing if needed)

## Limitations
Ensure that you're removing irrelevant log data to make script run faster.