# invest-stack

This repo is Ped's investing workflow. For any task here, load the `invest-mode` skill first and follow the playbook it routes to. Skills live in `plugins/invest-stack/skills/`.

- Holdings live in the ledger artifact named in `invest.config.json`, not in this repo.
- `work/` is scratch space with Ped's positions and is git-ignored. Never commit it.
- `briefs/` keeps each published weekly edition as HTML plus its content.json.
- `LESSONS.md` records mistakes that changed a script or playbook. Read it before writing a brief.
- Before editing, `git pull` and check the file's modified time. Another session may be working here.
