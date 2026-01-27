# DataConvert - Integration Plan

## 🎯 INTEGRATION GOALS

This document outlines how DataConvert integrates with:
1. Team Brain agents (Forge, Atlas, Clio, Nexus, Bolt)
2. Existing Team Brain tools
3. BCH (Beacon Command Hub) - potential future integration
4. Logan's workflows

---

## 📦 BCH INTEGRATION

### Overview

DataConvert is a standalone CLI/library tool. Direct BCH integration is **not currently implemented** but could be added in future phases.

### Potential BCH Commands (Future)

```
@dataconvert json-to-csv <file>
@dataconvert csv-to-yaml <file>
@dataconvert convert <file> --to <format>
```

### Why Not Integrated Yet

1. **Standalone Value:** DataConvert is most useful at the command line during development
2. **File-Based:** Requires local file access, which BCH agents may not have
3. **Alternative:** Agents can use Python API directly in their code

### Future Integration Path

If BCH integration is desired:
1. Add DataConvert to BCH tool registry
2. Create command handlers for common conversions
3. Allow file upload/download through BCH
4. Return converted content in messages

---

## 🤖 AI AGENT INTEGRATION

### Integration Matrix

| Agent | Use Case | Integration Method | Priority |
|-------|----------|-------------------|----------|
| **Forge** | Config conversion, spec generation | Python API | HIGH |
| **Atlas** | Build tool, data pipeline | CLI + Python API | HIGH |
| **Clio** | Linux automation, data processing | CLI | HIGH |
| **Nexus** | Cross-platform workflows | CLI + Python API | MEDIUM |
| **Bolt** | Batch conversions, automation | CLI | MEDIUM |

### Agent-Specific Workflows

---

#### Forge (Orchestrator / Reviewer)

**Primary Use Case:** Convert configuration files and specifications between formats.

**Integration Steps:**
1. Add DataConvert to Python path
2. Use for spec file format conversion
3. Generate reports in multiple formats

**Example Workflow:**

```python
# Forge session: Converting tool spec from JSON to YAML
from dataconvert import DataConvert

# Read tool specification
spec_json = DataConvert.read_file("tool_spec.json")

# Convert to YAML for Kubernetes deployment
spec_data = DataConvert.json_to_dict(spec_json)
yaml_output = DataConvert.dict_to_yaml(spec_data)

# Save for deployment
DataConvert.write_file("tool_spec.yaml", yaml_output)
```

**Forge-Specific Commands:**

```bash
# Convert session log JSON to YAML for archive
python dataconvert.py session_log.json --to yaml -o archive/session.yaml

# Generate XML report for external systems
python dataconvert.py report.json --to xml --root forge_report
```

---

#### Atlas (Executor / Builder)

**Primary Use Case:** Data transformation during tool development, test data generation.

**Integration Steps:**
1. Include DataConvert in tool development workflow
2. Use for test fixture generation
3. Transform API responses during development

**Example Workflow:**

```python
# Atlas session: Building tool with data conversion
from dataconvert import DataConvert

# Generate test data in multiple formats
test_data = [
    {"id": 1, "name": "Test1", "active": True},
    {"id": 2, "name": "Test2", "active": False}
]

# Create test fixtures
json_output = DataConvert.dict_to_json(test_data)
DataConvert.write_file("tests/fixtures/data.json", json_output)

csv_output = DataConvert.dict_to_csv(test_data)
DataConvert.write_file("tests/fixtures/data.csv", csv_output)

yaml_output = DataConvert.dict_to_yaml(test_data)
DataConvert.write_file("tests/fixtures/data.yaml", yaml_output)

print("[OK] Generated test fixtures in 3 formats")
```

**Atlas-Specific Commands:**

```bash
# Generate test data from CSV
python dataconvert.py test_input.csv --to json -o tests/input.json

# Transform API response for analysis
python dataconvert.py api_response.json --to csv -o analysis/data.csv
```

---

#### Clio (Linux / Ubuntu Agent)

**Primary Use Case:** Linux automation, data pipeline scripts, format standardization.

**Platform Considerations:**
- Works identically on Linux
- Can be added to PATH for global access
- Integrates with bash scripts and cron jobs

**Example Workflow:**

```bash
#!/bin/bash
# Clio: Daily data transformation script

# Convert yesterday's logs to CSV for analysis
LOG_FILE="/var/log/app/$(date -d 'yesterday' +%Y-%m-%d).json"
OUTPUT_FILE="/data/analysis/$(date -d 'yesterday' +%Y-%m-%d).csv"

python3 /opt/tools/dataconvert.py "$LOG_FILE" --to csv -o "$OUTPUT_FILE"

echo "[OK] Converted log to CSV: $OUTPUT_FILE"
```

**Clio-Specific Commands:**

```bash
# Batch convert all JSON configs to YAML
for f in /etc/myapp/*.json; do
  python3 dataconvert.py "$f" --to yaml -o "${f%.json}.yaml"
done

# Convert and pipe to another tool
python3 dataconvert.py input.xml --to json | jq '.data'
```

---

#### Nexus (Multi-Platform Agent)

**Primary Use Case:** Cross-platform data transformation, consistent format handling.

**Cross-Platform Notes:**
- Uses pathlib for cross-platform paths
- UTF-8 encoding handled automatically
- Works on Windows, Linux, macOS

**Example Workflow:**

```python
# Nexus: Cross-platform config migration
from dataconvert import DataConvert
from pathlib import Path
import platform

# Detect platform and set paths
if platform.system() == "Windows":
    config_dir = Path.home() / "AppData" / "Local" / "MyApp"
else:
    config_dir = Path.home() / ".config" / "myapp"

# Convert all JSON configs to YAML
for json_file in config_dir.glob("*.json"):
    content = DataConvert.read_file(str(json_file))
    data = DataConvert.json_to_dict(content)
    yaml_output = DataConvert.dict_to_yaml(data)
    
    yaml_file = json_file.with_suffix(".yaml")
    DataConvert.write_file(str(yaml_file), yaml_output)
    print(f"[OK] Converted {json_file.name} -> {yaml_file.name}")
```

---

#### Bolt (Cline / Free Executor)

**Primary Use Case:** Batch processing, repetitive conversions, automation tasks.

**Cost Considerations:**
- Zero dependencies = no installation costs
- Batch processing reduces API calls
- Offline operation = no network costs

**Example Workflow:**

```bash
# Bolt: Mass conversion task

# Convert all CSV files to JSON
find ./data -name "*.csv" -exec sh -c '
  for file do
    output="${file%.csv}.json"
    python dataconvert.py "$file" --to json -o "$output"
  done
' sh {} +

# Validate conversions
echo "[OK] Batch conversion complete"
```

---

## 🔗 INTEGRATION WITH OTHER TEAM BRAIN TOOLS

### With ContextCompressor

**Use Case:** Compress large data before conversion, or convert compressed summaries.

**Integration Pattern:**

```python
from contextcompressor import ContextCompressor
from dataconvert import DataConvert

# Compress large JSON data
compressor = ContextCompressor()
large_json = DataConvert.read_file("large_data.json")
compressed = compressor.compress_text(large_json)

# Convert compressed summary to other formats
summary_data = DataConvert.json_to_dict(compressed.compressed_text)
yaml_summary = DataConvert.dict_to_yaml(summary_data)
print(yaml_summary)
```

### With SynapseLink

**Use Case:** Format Synapse messages for different outputs.

**Integration Pattern:**

```python
from synapselink import SynapseLink
from dataconvert import DataConvert

# Load Synapse messages
synapse = SynapseLink()
messages = synapse.get_messages("ATLAS")

# Convert to CSV for analysis
csv_output = DataConvert.dict_to_csv(messages)
DataConvert.write_file("synapse_messages.csv", csv_output)

# Convert to YAML for documentation
yaml_output = DataConvert.dict_to_yaml(messages)
DataConvert.write_file("synapse_archive.yaml", yaml_output)
```

### With ConfigManager

**Use Case:** Migrate configurations between formats.

**Integration Pattern:**

```python
from configmanager import ConfigManager
from dataconvert import DataConvert

# Load current config
config = ConfigManager()
current = config.get_all()

# Export to different formats
json_export = DataConvert.dict_to_json(current)
yaml_export = DataConvert.dict_to_yaml(current)
xml_export = DataConvert.dict_to_xml(current, "config")

# Save backups
DataConvert.write_file("config_backup.json", json_export)
DataConvert.write_file("config_backup.yaml", yaml_export)
DataConvert.write_file("config_backup.xml", xml_export)
```

### With TaskQueuePro

**Use Case:** Export task data for analysis or reporting.

**Integration Pattern:**

```python
from taskqueuepro import TaskQueuePro
from dataconvert import DataConvert

# Get all tasks
queue = TaskQueuePro()
tasks = queue.list_tasks()

# Convert to CSV for spreadsheet
csv_output = DataConvert.dict_to_csv(tasks)
DataConvert.write_file("tasks_export.csv", csv_output)

# Generate XML report
xml_report = DataConvert.dict_to_xml({"tasks": tasks}, "task_report")
DataConvert.write_file("tasks_report.xml", xml_report)
```

### With SessionReplay

**Use Case:** Convert session data between formats.

**Integration Pattern:**

```python
from sessionreplay import SessionReplay
from dataconvert import DataConvert

# Export session data
replay = SessionReplay()
session = replay.get_session("session_123")

# Convert to different formats for sharing
json_export = DataConvert.dict_to_json(session.to_dict())
yaml_export = DataConvert.dict_to_yaml(session.to_dict())

# Archive session
DataConvert.write_file("session_archive.yaml", yaml_export)
```

### With LogHunter

**Use Case:** Convert log analysis results to different formats.

**Integration Pattern:**

```python
from loghunter import LogHunter
from dataconvert import DataConvert

# Analyze logs
hunter = LogHunter()
results = hunter.search("error", "/var/log/app")

# Export findings to CSV
csv_output = DataConvert.dict_to_csv(results["matches"])
DataConvert.write_file("error_report.csv", csv_output)
```

### With TokenTracker

**Use Case:** Export cost tracking data for analysis.

**Integration Pattern:**

```python
from tokentracker import TokenTracker
from dataconvert import DataConvert

# Get usage data
tracker = TokenTracker()
usage = tracker.get_monthly_summary()

# Export to CSV for spreadsheet analysis
csv_output = DataConvert.dict_to_csv(usage["daily_breakdown"])
DataConvert.write_file("token_usage.csv", csv_output)

# Export to YAML for documentation
yaml_output = DataConvert.dict_to_yaml(usage)
DataConvert.write_file("token_report.yaml", yaml_output)
```

---

## 🚀 ADOPTION ROADMAP

### Phase 1: Core Adoption (Week 1)

**Goal:** All agents aware and can use basic features

**Steps:**
1. [x] Tool deployed to GitHub
2. [ ] Quick-start guides sent via Synapse
3. [ ] Each agent tests basic workflow
4. [ ] Feedback collected

**Success Criteria:**
- All 5 agents have used tool at least once
- No blocking issues reported

### Phase 2: Integration (Week 2-3)

**Goal:** Integrated into daily workflows

**Steps:**
1. [ ] Add to agent startup routines (if needed)
2. [ ] Create integration examples with existing tools
3. [ ] Update agent-specific workflows
4. [ ] Monitor usage patterns

**Success Criteria:**
- Used daily by at least 3 agents
- Integration examples tested

### Phase 3: Optimization (Week 4+)

**Goal:** Optimized and fully adopted

**Steps:**
1. [ ] Collect efficiency metrics
2. [ ] Implement v1.1 improvements
3. [ ] Create advanced workflow examples
4. [ ] Full Team Brain ecosystem integration

**Success Criteria:**
- Measurable time/cost savings
- Positive feedback from all agents
- v1.1 improvements identified

---

## 📊 SUCCESS METRICS

**Adoption Metrics:**
- Number of agents using tool: Target 5/5
- Daily usage count: Track via file access
- Integration with other tools: Target 5+ integrations

**Efficiency Metrics:**
- Time saved per conversion: ~1-5 minutes
- Format migrations simplified: Previously manual
- Error reduction: Eliminate format syntax errors

**Quality Metrics:**
- Bug reports: Target < 3/month
- Feature requests: Track for v1.1
- User satisfaction: Qualitative feedback

---

## 🛠️ TECHNICAL INTEGRATION DETAILS

### Import Paths

```python
# Standard import
from dataconvert import DataConvert

# Also available
from dataconvert import SimpleYAML
```

### Configuration Integration

DataConvert is configuration-free by design. No config file needed.

**Optional Environment Variables:**
```bash
# None required - zero configuration!
```

### Error Handling Integration

**Standardized Error Codes:**
- 0: Success
- 1: General error (file not found, invalid format)
- 2: Parse error (invalid JSON, XML, etc.)

**Exception Types:**
```python
# Catch specific errors
try:
    data = DataConvert.json_to_dict(content)
except json.JSONDecodeError as e:
    print(f"Invalid JSON: {e}")
except ValueError as e:
    print(f"Conversion error: {e}")
```

### Logging Integration

DataConvert uses simple print statements for CLI output. For integration:

```python
import logging

# Redirect output if needed
import sys
from io import StringIO

# Capture output
old_stdout = sys.stdout
sys.stdout = StringIO()

# Run conversion
DataConvert.convert("json", "csv", data)

# Get output
output = sys.stdout.getvalue()
sys.stdout = old_stdout

# Log instead
logging.info(output)
```

---

## 🔧 MAINTENANCE & SUPPORT

### Update Strategy

- Minor updates (v1.x): As needed
- Major updates (v2.0+): Quarterly
- Security patches: Immediate

### Support Channels

- GitHub Issues: Bug reports
- Synapse: Team Brain discussions
- Direct to Builder: Complex issues

### Known Limitations

1. **YAML Complexity:** Built-in YAML parser handles basic structures only. For complex YAML (anchors, tags), use PyYAML.
2. **Large Files:** Files >100MB may be slow. Use streaming for huge datasets.
3. **Data Types in CSV:** CSV loses type information (all values become strings).
4. **XML Attributes:** Complex XML with namespaces may need manual handling.

### Planned Improvements (v1.1)

1. [ ] TOML support
2. [ ] INI file support
3. [ ] Streaming for large files
4. [ ] Schema validation
5. [ ] Type preservation for CSV

---

## 📚 ADDITIONAL RESOURCES

- Main Documentation: [README.md](README.md)
- Examples: [EXAMPLES.md](EXAMPLES.md)
- Quick Start Guides: [QUICK_START_GUIDES.md](QUICK_START_GUIDES.md)
- Integration Examples: [INTEGRATION_EXAMPLES.md](INTEGRATION_EXAMPLES.md)
- Cheat Sheet: [CHEAT_SHEET.txt](CHEAT_SHEET.txt)
- GitHub: https://github.com/DonkRonk17/DataConvert

---

**Last Updated:** January 2026  
**Maintained By:** FORGE (Team Brain)
