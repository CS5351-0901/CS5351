# A1 Week 4 integration review

`metadata.yaml` identifies `main:CodeAgentPlugin` as the plugin entry point, and `pyproject.toml` declares the Python package requirement and dependencies. `_conf_schema.json` supplies plugin settings that `main.py` reads through `_get_config` for blacklist checks, sandbox time and resource values, debug-round bounds, and quality thresholds.

The current static review also finds schema settings for network access, the network whitelist, knowledge use, and model selection without corresponding direct reads in the reviewed `main.py` call sites. Node.js setup and checker dependency preparation run from plugin initialization; the installer dispatch has Linux and macOS paths and needs Windows validation.

The Week 1–4 personal branch changes only `course_evidence/A1/**`. It contains role evidence and review documentation, with no changes to project business source. This is a source review and does not claim runtime tests passed.
