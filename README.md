# Backtesting

Repo to perform backtesting on stocks and validate strategies.

In order to setup this project, run:

## Setting up

```
bin/setup
```

## Running it

You'll then be able to:

```
NOSTATS=true STRATEGY=landry python3 main.py
```

## Deps

This project relies on:

* https://github.com/mementum/backtrader
* https://github.com/quantopian/pyfolio

## TODO

- [ ] Show stats in the end of the run using `pyfolio`.
- [ ] Improve Landry's strategy.
