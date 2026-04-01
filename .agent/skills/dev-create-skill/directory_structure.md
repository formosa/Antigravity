# Skill Scaffold Shapes

Use the smallest scaffold that fully supports the skill.

## Default scaffold

The default `init_skill.py` output keeps the skill instruction-first and ships only the schema bundle needed to understand the local contract.

```plaintext
my-skill/
├── SKILL.md
└── resources/
    └── schema/
        ├── README.md
        ├── example.md
        └── skill.d.ts
```

## With `--resources scripts`

Add `scripts/` only when deterministic execution is safer than regenerating code in the prompt body.

```plaintext
my-skill/
├── SKILL.md
├── resources/
│   └── schema/
│       ├── README.md
│       ├── example.md
│       └── skill.d.ts
└── scripts/
```

## With `--resources assets`

Add `assets/` only when the skill needs reusable templates, images, fonts, or other output files that should not be loaded as prompt context.

```plaintext
my-skill/
├── SKILL.md
├── assets/
└── resources/
    └── schema/
        ├── README.md
        ├── example.md
        └── skill.d.ts
```

## With `--resources resources --examples`

Add a resource example file only when you want a placeholder document to replace during authoring.

```plaintext
my-skill/
├── SKILL.md
└── resources/
    ├── reference.md
    └── schema/
        ├── README.md
        ├── example.md
        └── skill.d.ts
```

## With `--examples`

`--examples` adds placeholder example files only inside the optional folders you requested. Use it for rapid iteration, then replace or delete those files before packaging the final skill.
