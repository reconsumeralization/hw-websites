#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: ./control.sh [command] [options]"
    echo "Commands:"
    echo "  setup   - Initial project setup"
    echo "  backup  - Create a backup"
    echo "  restore - Restore from backup"
    echo "  clean   - Clean project structure"
    echo "  reset   - Reset to initial state"
    echo "  list    - List available backups"
    exit 1
fi

python scripts/control.py "$@"
