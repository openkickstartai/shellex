# shellex

Natural language to shell commands, powered by local LLMs.

## Install

```bash
pip install shellex
```

Requires [Ollama](https://ollama.ai) running locally:
```bash
ollama pull llama3.2
```

## Usage

```bash
# Basic
shellex "find all Python files larger than 1MB"
# -> find . -name "*.py" -size +1M
# Execute? [y/N]

# With explanation
shellex -e "show disk usage sorted by size"
# -> du -sh * | sort -rh | head -20

# Auto-execute (no confirmation)
shellex -y "count lines in all .go files"
```

## Safety

- Commands are **always shown before execution** (unless `-y`)
- Destructive commands (`rm -rf`, `dd`, `mkfs`) trigger extra warning
- All commands logged to `~/.local/share/shellex/history.jsonl`

## Testing

```bash
pip install -e .
pytest -v
```

## License

MIT
