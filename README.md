# The World in One Day — Friday 20 November 2026

[![make.fun](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Nr1414-dev/news-image-20-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Nr1414-dev/news-image-20-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261120)

A newspaper front page that sums up the world's news of **Friday 20 November 2026** in one image: the first three-way Trump–Xi–Putin summit in Shenzhen, the ICJ ruling that Myanmar committed genocide against the Rohingya, Cyclone Akvan nearing Odisha, strikes damaging embassies in Kyiv, a tanker burning after a mine strike east of the Strait of Hormuz, and Anthropic's stock market debut.

## How it is made

`draw.py` draws the front page from scratch with PIL (1024×1024, deterministic) and saves it as `entry.png`. `main.ts` copies that image to `/output/entry.png`, which is all the graded program does — no network, no randomness, so both runs write identical bytes.

## Run it

```sh
python3 draw.py            # redraw entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Competition

Entry for [news-image-20261120](https://make.fun/bounty/news-image-20261120) on [make.fun](https://make.fun).
