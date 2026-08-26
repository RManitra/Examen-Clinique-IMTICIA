#!/usr/bin/env bash
# Script d'exécution universel pour IconForge AI

set -e

INPUT_FILE=""
OUTPUT_DIR=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --input)
      INPUT_FILE="$2"
      shift 2
      ;;
    --output)
      OUTPUT_DIR="$2"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
done

if [[ -z "$INPUT_FILE" || -z "$OUTPUT_DIR" ]]; then
  echo "Usage: bash run.sh --input <requests.json> --output <outputs_dir>"
  exit 1
fi

python3 generate.py --input "$INPUT_FILE" --output "$OUTPUT_DIR"
