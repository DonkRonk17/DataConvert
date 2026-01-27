# DataConvert - Quick Start Guides

## 📖 ABOUT THESE GUIDES

Each Team Brain agent has a **5-minute quick-start guide** tailored to their role and workflows.

**Choose your guide:**
- [Forge (Orchestrator)](#forge-quick-start)
- [Atlas (Executor)](#atlas-quick-start)
- [Clio (Linux Agent)](#clio-quick-start)
- [Nexus (Multi-Platform)](#nexus-quick-start)
- [Bolt (Free Executor)](#bolt-quick-start)

---

## 🔥 FORGE QUICK START

**Role:** Orchestrator / Reviewer  
**Time:** 5 minutes  
**Goal:** Learn to use DataConvert for spec and config file management

### Step 1: Installation Check

```bash
# Verify DataConvert is available
cd C:\Users\logan\OneDrive\Documents\AutoProjects\DataConvert
python dataconvert.py --help

# Expected: Help message with supported formats
```

### Step 2: First Use - Convert Spec File

```bash
# Convert a JSON tool spec to YAML
python dataconvert.py tool_spec.json --to yaml --output tool_spec.yaml
```

**Expected Output:**
```
[READ] Reading JSON from: tool_spec.json
[CONVERT] Converting JSON -> YAML...
[OK] Saved to: tool_spec.yaml
```

### Step 3: Python API for Orchestration

```python
# In your Forge session
from dataconvert import DataConvert

# Convert spec from JSON to YAML
spec_json = '{"name": "NewTool", "version": "1.0", "priority": "HIGH"}'
spec_data = DataConvert.json_to_dict(spec_json)
yaml_output = DataConvert.dict_to_yaml(spec_data)

print(yaml_output)
# name: NewTool
# version: 1.0
# priority: HIGH
```

### Step 4: Common Forge Commands

```bash
# Convert session summary to YAML
python dataconvert.py session_summary.json --to yaml

# Generate XML report for external systems
python dataconvert.py report.json --to xml --root forge_report --pretty

# Convert roadmap to different formats
python dataconvert.py roadmap.json --to yaml -o roadmap.yaml
```

### Forge Integration Tips

1. **Spec Management:** Convert tool specs between JSON (development) and YAML (deployment)
2. **Report Generation:** Export session data to XML for external tools
3. **Config Migration:** Help agents migrate config formats

### Next Steps for Forge

1. Read [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) - Forge section
2. Try [EXAMPLES.md](EXAMPLES.md) - Example 3 (Config conversion)
3. Use in spec review workflows

---

## ⚡ ATLAS QUICK START

**Role:** Executor / Builder  
**Time:** 5 minutes  
**Goal:** Learn to use DataConvert for test data and build pipelines

### Step 1: Installation Check

```bash
cd C:\Users\logan\OneDrive\Documents\AutoProjects\DataConvert
python -c "from dataconvert import DataConvert; print('[OK] DataConvert imported')"
```

### Step 2: First Use - Generate Test Fixtures

```python
# In your Atlas session
from dataconvert import DataConvert

# Create test data
test_data = [
    {"id": 1, "name": "Test1", "active": True},
    {"id": 2, "name": "Test2", "active": False}
]

# Generate fixtures in multiple formats
json_out = DataConvert.dict_to_json(test_data)
csv_out = DataConvert.dict_to_csv(test_data)
yaml_out = DataConvert.dict_to_yaml(test_data)

# Save
DataConvert.write_file("tests/fixtures/data.json", json_out)
DataConvert.write_file("tests/fixtures/data.csv", csv_out)
DataConvert.write_file("tests/fixtures/data.yaml", yaml_out)

print("[OK] Test fixtures generated in 3 formats!")
```

### Step 3: CLI for Quick Conversions

```bash
# Convert API response mock to CSV for testing
python dataconvert.py mock_response.json --to csv -o tests/mock_data.csv

# Generate YAML config from JSON template
python dataconvert.py config_template.json --to yaml -o tests/config.yaml
```

### Step 4: Common Atlas Commands

```bash
# Generate test data
python dataconvert.py sample.csv --to json --pretty -o tests/sample.json

# Convert build manifest
python dataconvert.py manifest.json --to yaml

# Transform API responses
python dataconvert.py response.xml --to json --pretty
```

### Atlas Integration Tips

1. **Test Fixtures:** Generate test data in multiple formats from single source
2. **API Mocking:** Convert API responses for offline testing
3. **Build Configs:** Transform build configs between formats

### Next Steps for Atlas

1. Integrate into Holy Grail automation
2. Add to tool build checklist
3. Use for every new tool's test fixtures

---

## 🐧 CLIO QUICK START

**Role:** Linux / Ubuntu Agent  
**Time:** 5 minutes  
**Goal:** Learn to use DataConvert in Linux environment

### Step 1: Linux Installation

```bash
# Clone from GitHub (if not already present)
cd /opt/tools
git clone https://github.com/DonkRonk17/DataConvert.git
cd DataConvert

# Verify
python3 dataconvert.py --help
```

### Step 2: First Use - Linux Data Pipeline

```bash
# Convert JSON log to CSV for analysis
python3 dataconvert.py /var/log/app/events.json --to csv -o /tmp/events.csv

# Check result
head /tmp/events.csv
```

### Step 3: Bash Integration

```bash
#!/bin/bash
# clio_data_pipeline.sh

# Convert daily logs to CSV
LOG_DATE=$(date -d 'yesterday' +%Y-%m-%d)
LOG_FILE="/var/log/app/${LOG_DATE}.json"
OUTPUT_FILE="/data/analysis/${LOG_DATE}.csv"

python3 /opt/tools/DataConvert/dataconvert.py "$LOG_FILE" --to csv -o "$OUTPUT_FILE"
echo "[OK] Converted $LOG_FILE -> $OUTPUT_FILE"
```

### Step 4: Common Clio Commands

```bash
# Batch convert configs
for f in /etc/myapp/*.json; do
  python3 dataconvert.py "$f" --to yaml -o "${f%.json}.yaml"
done

# Pipe to other tools
python3 dataconvert.py input.json --to csv | cut -d',' -f1,3

# Convert and compress
python3 dataconvert.py data.xml --to json | gzip > data.json.gz
```

### Clio Integration Tips

1. **Cron Jobs:** Schedule daily conversions
2. **Pipelines:** Chain with grep, awk, jq
3. **Systemd:** Add to service scripts

### Next Steps for Clio

1. Add to ABIOS startup scripts
2. Test on Ubuntu environment
3. Create cron jobs for automated conversions

---

## 🌐 NEXUS QUICK START

**Role:** Multi-Platform Agent  
**Time:** 5 minutes  
**Goal:** Learn cross-platform usage of DataConvert

### Step 1: Platform Detection

```python
import platform
from dataconvert import DataConvert

# Check platform
print(f"Platform: {platform.system()}")
print(f"DataConvert: Ready")

# Same code works everywhere!
data = {"test": "value"}
print(DataConvert.dict_to_yaml(data))
```

### Step 2: First Use - Cross-Platform Config

```python
from pathlib import Path
import platform
from dataconvert import DataConvert

# Platform-aware paths
if platform.system() == "Windows":
    config_dir = Path.home() / "AppData" / "Local" / "MyApp"
else:
    config_dir = Path.home() / ".config" / "myapp"

# Convert configs regardless of platform
for json_file in config_dir.glob("*.json"):
    content = DataConvert.read_file(str(json_file))
    data = DataConvert.json_to_dict(content)
    yaml_output = DataConvert.dict_to_yaml(data)
    
    yaml_file = json_file.with_suffix(".yaml")
    DataConvert.write_file(str(yaml_file), yaml_output)
    print(f"[OK] {json_file.name} -> {yaml_file.name}")
```

### Step 3: Platform-Specific Considerations

**Windows:**
```bash
# PowerShell
python dataconvert.py .\config.json --to yaml -o .\config.yaml
```

**Linux/macOS:**
```bash
# Bash
python3 dataconvert.py ./config.json --to yaml -o ./config.yaml
```

### Step 4: Common Nexus Commands

```bash
# Windows PowerShell batch
Get-ChildItem *.json | ForEach-Object {
    python dataconvert.py $_.Name --to yaml -o ($_.BaseName + ".yaml")
}

# Linux/macOS batch
for f in *.json; do
    python3 dataconvert.py "$f" --to yaml -o "${f%.json}.yaml"
done
```

### Nexus Integration Tips

1. **Path Handling:** Use pathlib for cross-platform paths
2. **Encoding:** UTF-8 handled automatically
3. **Testing:** Test on all target platforms

### Next Steps for Nexus

1. Test on all 3 platforms
2. Report platform-specific issues
3. Add to multi-platform workflows

---

## 🆓 BOLT QUICK START

**Role:** Free Executor (Cline + Grok)  
**Time:** 5 minutes  
**Goal:** Learn to use DataConvert for batch automation without API costs

### Step 1: Verify Free Access

```bash
# No API key required!
cd C:\Users\logan\OneDrive\Documents\AutoProjects\DataConvert
python dataconvert.py --help
```

### Step 2: First Use - Batch Processing

```bash
# Convert all CSV files in directory to JSON
for file in data/*.csv; do
    output="${file%.csv}.json"
    python dataconvert.py "$file" --to json -o "$output"
    echo "[OK] $file -> $output"
done
```

### Step 3: Automation Scripts

```bash
#!/bin/bash
# bolt_batch_convert.sh
# Cost-free batch conversion script

INPUT_DIR="./input"
OUTPUT_DIR="./output"
FROM_FORMAT="csv"
TO_FORMAT="json"

mkdir -p "$OUTPUT_DIR"

for file in "$INPUT_DIR"/*.$FROM_FORMAT; do
    filename=$(basename "$file" .$FROM_FORMAT)
    output="$OUTPUT_DIR/$filename.$TO_FORMAT"
    
    python dataconvert.py "$file" --to "$TO_FORMAT" -o "$output"
done

echo "[OK] Batch conversion complete!"
```

### Step 4: Common Bolt Commands

```bash
# Mass conversion
find ./data -name "*.xml" -exec python dataconvert.py {} --to json \;

# Convert and validate
python dataconvert.py input.json --to csv && echo "[OK] Valid"

# Pipeline processing
cat data.json | python -c "
from dataconvert import DataConvert
import sys
data = DataConvert.json_to_dict(sys.stdin.read())
print(DataConvert.dict_to_csv(data if isinstance(data, list) else [data]))
"
```

### Bolt Integration Tips

1. **Offline Mode:** Works without internet
2. **Batch First:** Process files in bulk
3. **No Dependencies:** Zero setup required

### Next Steps for Bolt

1. Add to Cline workflows
2. Use for repetitive conversion tasks
3. Report any issues via Synapse

---

## 📚 ADDITIONAL RESOURCES

**For All Agents:**
- Full Documentation: [README.md](README.md)
- Examples: [EXAMPLES.md](EXAMPLES.md)
- Integration Plan: [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md)
- Integration Examples: [INTEGRATION_EXAMPLES.md](INTEGRATION_EXAMPLES.md)
- Cheat Sheet: [CHEAT_SHEET.txt](CHEAT_SHEET.txt)

**Support:**
- GitHub Issues: https://github.com/DonkRonk17/DataConvert/issues
- Synapse: Post in THE_SYNAPSE/active/
- Direct: Message tool builder

---

**Last Updated:** January 2026  
**Maintained By:** FORGE (Team Brain)
