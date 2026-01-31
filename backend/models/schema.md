┌──────────────────────────┐
│        story_jobs        │
├──────────────────────────┤
│ id (PK)                  │
│ job_id (UNIQUE)          │
│ session_id               │
│ theme                    │
│ status                   │
│ story_id (nullable) ─────┼──────────────┐
│ error (nullable)         │              │
│ created_at               │              │
│ completed_at (nullable)  │              │
└──────────────────────────┘              │
                                          │
                                          ▼
                               ┌──────────────────────┐
                               │        stories       │
                               ├──────────────────────┤
                               │ id (PK)              │
                               │ title                │
                               │ session_id           │
                               │ created_at           │
                               └─────────┬────────────┘
                                         │ 1
                                         │
                                         │
                                         │ N
                               ┌─────────▼────────────┐
                               │     story_nodes      │
                               ├──────────────────────┤
                               │ id (PK)              │
                               │ story_id (FK)        │
                               │ content              │
                               │ is_root              │
                               │ is_ending            │
                               │ is_winning_ending    │
                               │ options (JSON)       │
                               └──────────────────────┘
