# Week 4 integration status

`main.py` is now in the course repository. The main orchestration can be reviewed with the configuration schema, session and process state, sandbox, security scanner, JavaScript/TypeScript checker, packager, and snapshot helpers.

This is a static integration review. Static review does not mean that all runtime tests have passed, and no end-to-end runtime result is claimed here. The current source contains validation items around configuration mapping, confirmation and recovery behavior, checker failure handling, rollback call sites, and Windows Node.js/dependency preparation.

Week 5+ is where later real tests, fixes, and improvements occur.
