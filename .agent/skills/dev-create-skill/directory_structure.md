# Skill Scaffold Shapes

Use the smallest scaffold that fully supports the skill.

## Default scaffold

The default `init_skill.py` output keeps the skill instruction-first and ships only the schema bundle needed to understand the local contract.

```plaintext
my-skill/
├── README.md
├── SKILL.md
└── resources/
    └── schema/
        └── skill/
            ├── README.md
            ├── example.md
            └── skill.d.ts
```

## With `--resources scripts`

Add `scripts/` only when deterministic execution is safer than regenerating code in the prompt body.

```plaintext
my-skill/
├── README.md
├── SKILL.md
├── resources/
│   └── schema/
│       └── skill/
│           ├── README.md
│           ├── example.md
│           └── skill.d.ts
└── scripts/
```

## With `--resources assets`

Add `assets/` only when the skill needs reusable templates, images, fonts, or other output files that should not be loaded as prompt context.

```plaintext
my-skill/
├── README.md
├── SKILL.md
├── assets/
└── resources/
    └── schema/
        └── skill/
            ├── README.md
            ├── example.md
            └── skill.d.ts
```

## With `--resources resources --examples`

Add a resource example file only when you want a placeholder document to replace during authoring.

```plaintext
my-skill/
├── README.md
├── SKILL.md
└── resources/
    ├── reference.md
    └── schema/
        └── skill/
            ├── README.md
            ├── example.md
            └── skill.d.ts
```

## With `--examples`

`--examples` adds placeholder example files only inside the optional folders you requested. Use it for rapid iteration, then replace or delete those files before packaging the final skill.

## Root README Contract

Every skill root now includes a `README.md` with:

- `<document_purpose>`
- `<authority_order>`
- `<schema_relationships>`
- `<modification_history>`

The canonical authority for schema definitions remains `.agent/schemas/`; skill-local `resources/schema/<schema-id>/` directories are vendored read-only mirrors for packaging and local reference.
