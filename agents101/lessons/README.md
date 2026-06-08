# Reference lessons for the agents101 course

These files are **reference depth** for the tutor — concrete commands,
worked examples, pitfalls, and further reading per topic.

The intended way to use this course is the tutor-driven flow:

```bash
cd /w/CoursesGinaGu/agents101
claude                 # launches Claude Code in this directory
/lesson                # begins (or resumes) today's ~1-hour session
```

See `../syllabus.md` for the syllabus and `../CLAUDE.md` for the
tutor's contract.

That said, these reference files are also readable directly. If
you'd rather skim than be tutored, the suggested order:

| # | File | Topic |
|---|---|---|
| 00 | [00-setup.md](00-setup.md) | Environment prerequisites |
| 01 | [01-what-are-agents.md](01-what-are-agents.md) | Agents vs LLMs vs chatbots |
| 02 | [02-local-models.md](02-local-models.md) | MLX / Ollama |
| 03 | [03-first-conversation.md](03-first-conversation.md) | Hermes hello-world |
| 04 | [04-tools-and-skills.md](04-tools-and-skills.md) | Extending the agent |
| 05 | [05-kanban.md](05-kanban.md) | Multi-agent coordination |
| 06 | [06-cron-and-scheduling.md](06-cron-and-scheduling.md) | Scheduled agents and watchdogs |
| 07 | [07-messaging.md](07-messaging.md) | Telegram / Slack gateways |
| 08 | [08-oversight.md](08-oversight.md) | Building a polling watchdog |
| 09 | [09-debugging.md](09-debugging.md) | Where state lives; when things break |
| 10 | [10-docker.md](10-docker.md) | Containerized agents |
| 11 | [11-where-next.md](11-where-next.md) | Other frameworks; deeper directions |

Each file is self-contained at the topic level. Cross-references
(`[02-local-models.md](02-local-models.md)`) work as relative links
within this directory.
