# Agent failure log

Working notes from running AI agents, mostly Claude, on a months-long public-records investigation into xAI's data centers in Memphis, Tennessee and Southaven, Mississippi ([The xAI Files](https://rachelandthecity.com/the-xai-files/)).

Every entry is a real failure from that work, with the date, the numbers, and the rule that came out of it. The rules still run the investigation today.

## Who did what

- **Rachel Hurley** directed the investigation and the agents, and decided which rules to keep. She is not a programmer.
- **The failure log** was written up during the work by the Claude sessions running it, under her direction.
- **The scripts** were written by Claude at her direction.
- **This README** was drafted by Claude and approved by Rachel.

## What is here

| File | What it is |
| --- | --- |
| [FAILURE-LOG.md](FAILURE-LOG.md) | The log. A cleaned copy of the working document: names of people, companies and specific agency files are generalized, and every number about the process is unchanged. |
| [scripts/check.py](scripts/check.py) | The "search before you write" gate. It reads every note and source filename directly, because the vault's own search tool returned zero results on its first call. |
| [scripts/vault-check.py](scripts/vault-check.py) | A read-only health check for the agents' shared notes vault: broken links, missing fields, orphan notes, sync duplicates, and files that may hold a password. |

`check.py` is published as it runs. It still has the defect described at the end of the log: a file it cannot read is skipped silently and counted as "no match."

## The short version

| What went wrong | The rule it produced |
| --- | --- |
| A session wrote "everything in the vault has been read." A count showed 236 of 1,806 documents, 13.1 percent. | Coverage is computed, never written. |
| A checker counted its own output as proof and reported 1,860 of 1,872 files covered. The true figure was 1,212. | A checker may never read a file it also writes. |
| Old task-board rows written by earlier sessions were treated as fact, and two finished jobs came back marked "blocking." | Anything on the board is a claim until it is checked. |
| Sessions redid finished work seven times. Once, a resumed session rebuilt an exhibit from an image Rachel had rejected and reported it to her twice as new work. | Search the archive before writing, and check the history before resuming. |
| A nightly reading queue reported clean runs for six weeks while 1,809 files could never be drawn. | Rebuild the queue when new files arrive, and compare it with the whole collection before saying what is left. |
| A session searched one of two channels and reported that a record had "never been posted anywhere." | Search every channel the rule names before reporting a negative. |
