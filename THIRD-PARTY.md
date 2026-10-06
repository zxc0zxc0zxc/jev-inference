# Third-party attribution

The core task validation, scoring, and metrics in
`src/jev_inference/_vendor/jevbench/` are copied without modification from
[fstandhartinger/jevbench](https://github.com/fstandhartinger/jevbench), commit
`bb05a335bc809e61b20c0f745d25499a82b326fc` (MIT).
Copyright (c) 2026 Florian Standhartinger and contributors.
The complete license is included alongside the vendored files.

JevBench public data are downloaded separately from the same pinned commit.
The 48 easy, 72 original, and 111 hard records each identify their license as MIT.
Their provenance and answer keys remain in the recorded dataset, but are never
included in model prompts. Generated reports are public-subset diagnostics,
not official JevBench submissions or leaderboard scores.
