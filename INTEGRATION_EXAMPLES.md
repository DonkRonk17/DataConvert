# DataConvert - Integration Examples

## 🎯 INTEGRATION PHILOSOPHY

DataConvert is designed to work seamlessly with other Team Brain tools. This document provides **copy-paste-ready code examples** for common integration patterns.

---

## 📚 TABLE OF CONTENTS

1. [Pattern 1: DataConvert + ContextCompressor](#pattern-1-dataconvert--contextcompressor)
2. [Pattern 2: DataConvert + SynapseLink](#pattern-2-dataconvert--synapselink)
3. [Pattern 3: DataConvert + ConfigManager](#pattern-3-dataconvert--configmanager)
4. [Pattern 4: DataConvert + TaskQueuePro](#pattern-4-dataconvert--taskqueuepro)
5. [Pattern 5: DataConvert + SessionReplay](#pattern-5-dataconvert--sessionreplay)
6. [Pattern 6: DataConvert + TokenTracker](#pattern-6-dataconvert--tokentracker)
7. [Pattern 7: DataConvert + LogHunter](#pattern-7-dataconvert--loghunter)
8. [Pattern 8: DataConvert + AgentHealth](#pattern-8-dataconvert--agenthealth)
9. [Pattern 9: Multi-Tool Data Pipeline](#pattern-9-multi-tool-data-pipeline)
10. [Pattern 10: Full Team Brain Integration](#pattern-10-full-team-brain-integration)

---

## Pattern 1: DataConvert + ContextCompressor

**Use Case:** Compress large data, convert to different formats for sharing

**Why:** Large JSON files can be compressed before conversion to save tokens and storage

**Code:**

```python
from contextcompressor import ContextCompressor
from dataconvert import DataConvert

# Step 1: Load large data
large_json = DataConvert.read_file("large_dataset.json")
data = DataConvert.json_to_dict(large_json)

# Step 2: Compress if needed
compressor = ContextCompressor()
if len(large_json) > 10000:  # Compress if > 10KB
    compressed = compressor.compress_text(large_json, method="summary")
    print(f"Compressed: {len(large_json)} -> {len(compressed.compressed_text)} chars")
    data = DataConvert.json_to_dict(compressed.compressed_text)

# Step 3: Convert to desired format
yaml_output = DataConvert.dict_to_yaml(data)
csv_output = DataConvert.dict_to_csv(data if isinstance(data, list) else [data])

# Step 4: Save
DataConvert.write_file("output.yaml", yaml_output)
DataConvert.write_file("output.csv", csv_output)

print("[OK] Compressed and converted successfully")
```

**Result:** Large JSON compressed and converted to multiple formats

---

## Pattern 2: DataConvert + SynapseLink

**Use Case:** Export Synapse messages to different formats for analysis

**Why:** Analyze team communication patterns in spreadsheet or archive format

**Code:**

```python
from synapselink import SynapseLink
from dataconvert import DataConvert
from datetime import datetime

# Step 1: Get Synapse messages
synapse = SynapseLink()
messages = synapse.get_messages(agent="ATLAS", days=7)

# Step 2: Convert to list of dicts for processing
message_list = []
for msg in messages:
    message_list.append({
        "id": msg.get("msg_id", ""),
        "from": msg.get("from", ""),
        "to": str(msg.get("to", [])),
        "subject": msg.get("subject", ""),
        "timestamp": msg.get("timestamp", ""),
        "priority": msg.get("priority", "NORMAL")
    })

# Step 3: Export to CSV for spreadsheet analysis
csv_output = DataConvert.dict_to_csv(message_list)
DataConvert.write_file("synapse_export.csv", csv_output)

# Step 4: Export to YAML for documentation
yaml_output = DataConvert.dict_to_yaml(message_list)
DataConvert.write_file("synapse_archive.yaml", yaml_output)

# Step 5: Generate XML report
xml_output = DataConvert.dict_to_xml(
    {"messages": message_list}, 
    root_name="synapse_report"
)
DataConvert.write_file("synapse_report.xml", xml_output)

print(f"[OK] Exported {len(message_list)} messages to CSV, YAML, and XML")
```

**Result:** Synapse messages exported in 3 formats for different use cases

---

## Pattern 3: DataConvert + ConfigManager

**Use Case:** Migrate configurations between formats

**Why:** Different systems need different config formats (JSON, YAML, XML)

**Code:**

```python
from configmanager import ConfigManager
from dataconvert import DataConvert

# Step 1: Load current configuration
config = ConfigManager()
current_config = config.get_all()

# Step 2: Create backup in original format
json_backup = DataConvert.dict_to_json(current_config, pretty=True)
DataConvert.write_file("config_backup.json", json_backup)

# Step 3: Convert to YAML for Kubernetes
yaml_config = DataConvert.dict_to_yaml(current_config)
DataConvert.write_file("kubernetes_config.yaml", yaml_config)

# Step 4: Convert to XML for legacy systems
xml_config = DataConvert.dict_to_xml(current_config, root_name="configuration")
DataConvert.write_file("legacy_config.xml", xml_config)

# Step 5: Load new config from YAML
new_yaml = DataConvert.read_file("updated_config.yaml")
new_config = DataConvert.yaml_to_dict(new_yaml)

# Step 6: Update ConfigManager
for key, value in new_config.items():
    config.set(key, value)
config.save()

print("[OK] Config migrated and updated from YAML")
```

**Result:** Configuration migrated between formats, backups created

---

## Pattern 4: DataConvert + TaskQueuePro

**Use Case:** Export tasks to CSV for reporting, import from CSV

**Why:** Generate task reports for stakeholders, bulk import tasks

**Code:**

```python
from taskqueuepro import TaskQueuePro
from dataconvert import DataConvert

# Step 1: Get all tasks
queue = TaskQueuePro()
tasks = queue.list_tasks()

# Step 2: Convert to CSV for spreadsheet
task_list = []
for task in tasks:
    task_list.append({
        "id": task.id,
        "title": task.title,
        "agent": task.agent,
        "priority": task.priority,
        "status": task.status,
        "created": task.created_at
    })

csv_output = DataConvert.dict_to_csv(task_list)
DataConvert.write_file("tasks_report.csv", csv_output)

# Step 3: Generate XML report
xml_output = DataConvert.dict_to_xml(
    {"task_report": {"generated": "2026-01-26", "tasks": task_list}},
    root_name="report"
)
DataConvert.write_file("tasks_report.xml", xml_output)

# Step 4: Import tasks from CSV (reverse operation)
import_csv = DataConvert.read_file("new_tasks.csv")
new_tasks = DataConvert.csv_to_dict(import_csv)

for task_data in new_tasks:
    queue.create_task(
        title=task_data["title"],
        agent=task_data["agent"],
        priority=int(task_data.get("priority", 3))
    )

print(f"[OK] Exported {len(task_list)} tasks, imported {len(new_tasks)} new tasks")
```

**Result:** Bidirectional task data exchange via CSV

---

## Pattern 5: DataConvert + SessionReplay

**Use Case:** Archive session data in multiple formats

**Why:** Long-term storage in human-readable format, share sessions

**Code:**

```python
from sessionreplay import SessionReplay
from dataconvert import DataConvert
from datetime import datetime

# Step 1: Get session data
replay = SessionReplay()
session = replay.get_session("session_123")

# Step 2: Convert to dictionary
session_data = {
    "session_id": session.session_id,
    "agent": session.agent,
    "task": session.task,
    "started": str(session.started_at),
    "ended": str(session.ended_at),
    "status": session.status,
    "events": session.events,
    "decisions": session.decisions
}

# Step 3: Archive in YAML (human-readable)
yaml_archive = DataConvert.dict_to_yaml(session_data)
archive_name = f"session_{session.session_id}_{datetime.now().strftime('%Y%m%d')}.yaml"
DataConvert.write_file(f"archives/{archive_name}", yaml_archive)

# Step 4: Export events to CSV for analysis
events_csv = DataConvert.dict_to_csv(session.events)
DataConvert.write_file(f"archives/events_{session.session_id}.csv", events_csv)

# Step 5: Generate JSON for API sharing
json_export = DataConvert.dict_to_json(session_data, pretty=True)
DataConvert.write_file(f"exports/session_{session.session_id}.json", json_export)

print(f"[OK] Session {session.session_id} archived in YAML, CSV, and JSON")
```

**Result:** Session data preserved in multiple formats for different purposes

---

## Pattern 6: DataConvert + TokenTracker

**Use Case:** Export cost data for financial analysis

**Why:** Generate reports for budget tracking, cost allocation

**Code:**

```python
from tokentracker import TokenTracker
from dataconvert import DataConvert

# Step 1: Get usage data
tracker = TokenTracker()
monthly = tracker.get_monthly_summary()
daily = tracker.get_daily_breakdown()

# Step 2: Export daily breakdown to CSV for Excel
csv_output = DataConvert.dict_to_csv(daily)
DataConvert.write_file("token_usage_daily.csv", csv_output)

# Step 3: Export summary to YAML for documentation
yaml_output = DataConvert.dict_to_yaml(monthly)
DataConvert.write_file("token_summary.yaml", yaml_output)

# Step 4: Generate XML report for accounting
xml_report = DataConvert.dict_to_xml({
    "token_report": {
        "period": monthly.get("period", ""),
        "total_tokens": monthly.get("total_tokens", 0),
        "total_cost": monthly.get("total_cost", 0),
        "budget": monthly.get("budget", 60),
        "remaining": monthly.get("remaining", 0)
    }
}, root_name="financial_report")
DataConvert.write_file("token_report.xml", xml_report)

print(f"[OK] Token usage exported to CSV, YAML, and XML")
print(f"     Budget: ${monthly.get('budget', 60)}, Spent: ${monthly.get('total_cost', 0):.2f}")
```

**Result:** Cost data exported for financial tracking

---

## Pattern 7: DataConvert + LogHunter

**Use Case:** Convert log search results to reportable formats

**Why:** Share findings with team, analyze patterns in spreadsheet

**Code:**

```python
from loghunter import LogHunter
from dataconvert import DataConvert
from datetime import datetime

# Step 1: Search logs
hunter = LogHunter()
results = hunter.search(
    pattern="error|exception|failed",
    path="/var/log/app",
    last_hours=24
)

# Step 2: Convert matches to list
matches = []
for match in results.get("matches", []):
    matches.append({
        "file": match.get("file", ""),
        "line": match.get("line_number", 0),
        "content": match.get("content", "")[:100],  # Truncate long lines
        "timestamp": match.get("timestamp", "")
    })

# Step 3: Export to CSV for analysis
csv_output = DataConvert.dict_to_csv(matches)
DataConvert.write_file("error_report.csv", csv_output)

# Step 4: Generate summary in YAML
summary = {
    "generated": datetime.now().isoformat(),
    "total_matches": len(matches),
    "files_scanned": results.get("files_scanned", 0),
    "search_pattern": "error|exception|failed",
    "matches": matches[:10]  # First 10 for summary
}
yaml_output = DataConvert.dict_to_yaml(summary)
DataConvert.write_file("error_summary.yaml", yaml_output)

print(f"[OK] Found {len(matches)} errors, exported to CSV and YAML")
```

**Result:** Log analysis results in shareable formats

---

## Pattern 8: DataConvert + AgentHealth

**Use Case:** Export health metrics for monitoring dashboard

**Why:** Feed metrics to external monitoring tools

**Code:**

```python
from agenthealth import AgentHealth
from dataconvert import DataConvert

# Step 1: Get health data for all agents
health = AgentHealth()
all_agents = ["FORGE", "ATLAS", "CLIO", "NEXUS", "BOLT"]

health_data = []
for agent in all_agents:
    status = health.get_status(agent)
    health_data.append({
        "agent": agent,
        "status": status.get("status", "unknown"),
        "last_seen": status.get("last_seen", ""),
        "sessions_today": status.get("sessions_today", 0),
        "error_rate": status.get("error_rate", 0)
    })

# Step 2: Export to CSV for dashboard
csv_output = DataConvert.dict_to_csv(health_data)
DataConvert.write_file("agent_health.csv", csv_output)

# Step 3: Export to JSON for API
json_output = DataConvert.dict_to_json({"agents": health_data}, pretty=True)
DataConvert.write_file("agent_health.json", json_output)

# Step 4: Export to XML for legacy systems
xml_output = DataConvert.dict_to_xml(
    {"health_report": health_data},
    root_name="team_brain_health"
)
DataConvert.write_file("agent_health.xml", xml_output)

print(f"[OK] Health data for {len(all_agents)} agents exported")
```

**Result:** Agent health metrics in multiple formats for monitoring

---

## Pattern 9: Multi-Tool Data Pipeline

**Use Case:** Complete workflow using multiple tools with data conversion

**Why:** Demonstrate real production scenario

**Code:**

```python
"""
Multi-Tool Data Pipeline: Log Analysis -> Task Creation -> Notification
"""

from loghunter import LogHunter
from taskqueuepro import TaskQueuePro
from synapselink import quick_send
from dataconvert import DataConvert

# Step 1: Find errors in logs
print("[STEP 1] Searching logs for errors...")
hunter = LogHunter()
results = hunter.search("ERROR", "/var/log/app", last_hours=6)

errors = results.get("matches", [])
print(f"         Found {len(errors)} errors")

# Step 2: Convert to structured data
error_list = []
for err in errors:
    error_list.append({
        "file": err.get("file", ""),
        "line": err.get("line_number", 0),
        "message": err.get("content", "")[:200]
    })

# Step 3: Export to CSV for analysis
print("[STEP 2] Exporting to CSV...")
csv_output = DataConvert.dict_to_csv(error_list)
DataConvert.write_file("errors_analysis.csv", csv_output)

# Step 4: Create tasks for critical errors
print("[STEP 3] Creating tasks for critical errors...")
queue = TaskQueuePro()
critical_count = 0

for err in error_list:
    if "CRITICAL" in err.get("message", "").upper():
        queue.create_task(
            title=f"Investigate: {err['file']}",
            agent="NEXUS",
            priority=1,
            metadata={"error": err}
        )
        critical_count += 1

print(f"         Created {critical_count} tasks")

# Step 5: Generate YAML report
print("[STEP 4] Generating report...")
report = {
    "generated": "2026-01-26",
    "total_errors": len(error_list),
    "critical_errors": critical_count,
    "tasks_created": critical_count,
    "sample_errors": error_list[:5]
}
yaml_report = DataConvert.dict_to_yaml(report)
DataConvert.write_file("error_report.yaml", yaml_report)

# Step 6: Notify team
print("[STEP 5] Notifying team...")
quick_send(
    "FORGE,ATLAS",
    "Error Analysis Complete",
    f"Found {len(error_list)} errors, {critical_count} critical.\n"
    f"Tasks created: {critical_count}\n"
    f"Report: error_report.yaml",
    priority="HIGH" if critical_count > 0 else "NORMAL"
)

print("[DONE] Pipeline complete!")
```

**Result:** Fully instrumented, coordinated workflow

---

## Pattern 10: Full Team Brain Integration

**Use Case:** Ultimate integration - all tools working together

**Why:** Production-grade agent operation

**Code:**

```python
"""
Full Team Brain Stack Integration
All tools coordinated with DataConvert
"""

from taskqueuepro import TaskQueuePro
from sessionreplay import SessionReplay
from agenthealth import AgentHealth
from synapselink import quick_send
from tokentracker import TokenTracker
from configmanager import ConfigManager
from dataconvert import DataConvert

# Initialize all tools
queue = TaskQueuePro()
replay = SessionReplay()
health = AgentHealth()
tracker = TokenTracker()
config = ConfigManager()

# Start coordinated session
session_id = replay.start_session("ATLAS", task="Full integration test")
health.start_session("ATLAS", session_id=session_id)

try:
    # Task 1: Export current state
    print("[1/5] Exporting current state...")
    
    tasks = queue.list_tasks()
    tasks_csv = DataConvert.dict_to_csv([t.to_dict() for t in tasks])
    DataConvert.write_file("state/tasks.csv", tasks_csv)
    
    usage = tracker.get_monthly_summary()
    usage_yaml = DataConvert.dict_to_yaml(usage)
    DataConvert.write_file("state/usage.yaml", usage_yaml)
    
    current_config = config.get_all()
    config_json = DataConvert.dict_to_json(current_config)
    DataConvert.write_file("state/config.json", config_json)
    
    replay.log_event(session_id, "Exported state to 3 files")
    
    # Task 2: Process data
    print("[2/5] Processing data...")
    health.heartbeat("ATLAS", status="processing")
    
    # Convert between formats as needed
    DataConvert.write_file(
        "state/config.yaml",
        DataConvert.dict_to_yaml(current_config)
    )
    
    # Task 3: Generate report
    print("[3/5] Generating reports...")
    
    report = {
        "session_id": session_id,
        "tasks_count": len(tasks),
        "token_usage": usage,
        "config_keys": list(current_config.keys())
    }
    
    # Multiple formats
    DataConvert.write_file("reports/summary.json", DataConvert.dict_to_json(report))
    DataConvert.write_file("reports/summary.yaml", DataConvert.dict_to_yaml(report))
    DataConvert.write_file("reports/summary.xml", DataConvert.dict_to_xml(report, "report"))
    
    # Task 4: Complete session
    print("[4/5] Completing session...")
    replay.end_session(session_id, status="COMPLETED")
    health.end_session("ATLAS", session_id=session_id, status="success")
    
    # Task 5: Notify team
    print("[5/5] Notifying team...")
    quick_send(
        "TEAM",
        "Full Integration Test Complete",
        f"Session: {session_id}\n"
        f"Tasks exported: {len(tasks)}\n"
        f"Reports generated: 3 formats\n"
        f"Status: SUCCESS",
        priority="NORMAL"
    )
    
    print("\n[SUCCESS] Full Team Brain integration complete!")
    
except Exception as e:
    replay.log_error(session_id, str(e))
    replay.end_session(session_id, status="FAILED")
    health.log_error("ATLAS", str(e))
    health.end_session("ATLAS", session_id=session_id, status="failed")
    
    quick_send("FORGE", "Integration Test Failed", str(e), priority="HIGH")
    
    print(f"\n[ERROR] Integration failed: {e}")
```

**Result:** All Team Brain tools working together with DataConvert as the data transformation layer

---

## 📊 RECOMMENDED INTEGRATION PRIORITY

**Week 1 (Essential):**
1. [x] SynapseLink - Message export
2. [x] ConfigManager - Config migration
3. [x] TaskQueuePro - Task reports

**Week 2 (Productivity):**
4. [ ] TokenTracker - Cost reports
5. [ ] LogHunter - Error analysis
6. [ ] SessionReplay - Session archiving

**Week 3 (Advanced):**
7. [ ] ContextCompressor - Large data handling
8. [ ] AgentHealth - Health dashboards
9. [ ] Full stack integration

---

## 🔧 TROUBLESHOOTING INTEGRATIONS

**Import Errors:**
```python
# Ensure all tools are in Python path
import sys
from pathlib import Path
sys.path.append(str(Path.home() / "OneDrive/Documents/AutoProjects"))

# Then import
from dataconvert import DataConvert
from synapselink import SynapseLink
```

**Format Conversion Issues:**
```python
# Check data structure before converting
data = DataConvert.json_to_dict(content)
print(f"Type: {type(data)}")  # dict or list?
print(f"Keys: {data.keys() if isinstance(data, dict) else 'N/A'}")

# CSV requires list of flat dicts
if isinstance(data, dict):
    data = [data]  # Wrap single object in list
```

**File Encoding Issues:**
```python
# DataConvert uses UTF-8 by default
# If you have other encodings:
with open("file.json", "r", encoding="utf-8") as f:
    content = f.read()
data = DataConvert.json_to_dict(content)
```

---

**Last Updated:** January 2026  
**Maintained By:** FORGE (Team Brain)
