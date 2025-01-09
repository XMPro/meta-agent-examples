# Package Publishing Guide

This repository contains Python libraries that are published to package indexers (public or private). Each library is built and distributed independently.

## Building and Publishing

Each package uses `pyproject.toml` for build configuration. To build and publish:

1. Build the package:
```bash
python -m build
```
Creates distribution files in `/dist`

2. Upload to indexer:
```bash
python -m twine upload dist/*
```
Requires appropriate credentials.

## Structure
```
packages/
└── your-package/
    ├── src/
    ├── tests/
    ├── pyproject.toml
    └── README.md
```

## Need Help?
Contact Jaun for assistance with builds, deployments, or credentials:
jvh@xmpro.com

## Note
These packages support industrial data processing. Keep them modular and cleanly separated from implementations.