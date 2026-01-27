# DataConvert - Usage Examples

**10 Real-World Examples with Full Input/Output**

Quick navigation:
- [Example 1: Basic JSON to CSV](#example-1-basic-json-to-csv)
- [Example 2: CSV to JSON with Pretty Print](#example-2-csv-to-json-with-pretty-print)
- [Example 3: JSON to YAML Configuration](#example-3-json-to-yaml-configuration)
- [Example 4: XML to JSON Parsing](#example-4-xml-to-json-parsing)
- [Example 5: YAML to JSON for API](#example-5-yaml-to-json-for-api)
- [Example 6: JSON to XML with Custom Root](#example-6-json-to-xml-with-custom-root)
- [Example 7: Batch CSV Processing](#example-7-batch-csv-processing)
- [Example 8: Nested Data Conversion](#example-8-nested-data-conversion)
- [Example 9: Python API Usage](#example-9-python-api-usage)
- [Example 10: Full Production Workflow](#example-10-full-production-workflow)

---

## Example 1: Basic JSON to CSV

**Scenario:** Export user data from JSON format to CSV for spreadsheet analysis.

**Input file (`users.json`):**
```json
[
  {"name": "Alice Johnson", "email": "alice@example.com", "age": 28},
  {"name": "Bob Smith", "email": "bob@example.com", "age": 34},
  {"name": "Carol White", "email": "carol@example.com", "age": 25}
]
```

**Command:**
```bash
python dataconvert.py users.json --to csv --output users.csv
```

**Output (`users.csv`):**
```csv
name,email,age
Alice Johnson,alice@example.com,28
Bob Smith,bob@example.com,34
Carol White,carol@example.com,25
```

**Console Output:**
```
[READ] Reading JSON from: users.json
[CONVERT] Converting JSON -> CSV...
[OK] Saved to: users.csv
```

**What You Learned:**
- Basic JSON array to CSV conversion
- Output file specification with `--output`
- Clean tabular data for spreadsheets

---

## Example 2: CSV to JSON with Pretty Print

**Scenario:** Convert sales data CSV to JSON for API integration.

**Input file (`sales.csv`):**
```csv
product,price,quantity,region
Laptop,999.99,15,North
Mouse,29.99,100,East
Keyboard,79.99,50,West
Monitor,299.99,25,South
```

**Command:**
```bash
python dataconvert.py sales.csv --to json --pretty
```

**Output (stdout):**
```json
[
  {
    "product": "Laptop",
    "price": "999.99",
    "quantity": "15",
    "region": "North"
  },
  {
    "product": "Mouse",
    "price": "29.99",
    "quantity": "100",
    "region": "East"
  },
  {
    "product": "Keyboard",
    "price": "79.99",
    "quantity": "50",
    "region": "West"
  },
  {
    "product": "Monitor",
    "price": "299.99",
    "quantity": "25",
    "region": "South"
  }
]
```

**What You Learned:**
- CSV to JSON conversion
- Pretty print with `--pretty` flag
- All values from CSV are strings (preserve if needed)

---

## Example 3: JSON to YAML Configuration

**Scenario:** Convert application config from JSON to YAML format for Kubernetes deployment.

**Input file (`config.json`):**
```json
{
  "app": {
    "name": "my-service",
    "version": "1.0.0",
    "port": 8080
  },
  "database": {
    "host": "db.example.com",
    "port": 5432,
    "name": "production",
    "pool_size": 10
  },
  "features": {
    "cache_enabled": true,
    "debug_mode": false
  }
}
```

**Command:**
```bash
python dataconvert.py config.json --to yaml --output config.yaml
```

**Output (`config.yaml`):**
```yaml
app:
  name: my-service
  version: 1.0.0
  port: 8080
database:
  host: db.example.com
  port: 5432
  name: production
  pool_size: 10
features:
  cache_enabled: true
  debug_mode: false
```

**What You Learned:**
- JSON to YAML for config files
- Nested structures preserved
- Boolean values handled correctly

---

## Example 4: XML to JSON Parsing

**Scenario:** Parse XML API response into JSON for modern processing.

**Input file (`response.xml`):**
```xml
<?xml version="1.0"?>
<api_response>
  <status>success</status>
  <data>
    <user id="123">
      <name>John Doe</name>
      <email>john@example.com</email>
    </user>
    <user id="456">
      <name>Jane Doe</name>
      <email>jane@example.com</email>
    </user>
  </data>
  <timestamp>2026-01-26T10:30:00Z</timestamp>
</api_response>
```

**Command:**
```bash
python dataconvert.py response.xml --to json --output response.json
```

**Output (`response.json`):**
```json
{
  "api_response": {
    "status": "success",
    "data": {
      "user": [
        {
          "@attributes": {
            "id": "123"
          },
          "name": "John Doe",
          "email": "john@example.com"
        },
        {
          "@attributes": {
            "id": "456"
          },
          "name": "Jane Doe",
          "email": "jane@example.com"
        }
      ]
    },
    "timestamp": "2026-01-26T10:30:00Z"
  }
}
```

**What You Learned:**
- XML to JSON conversion
- XML attributes become `@attributes` object
- Repeated elements become arrays

---

## Example 5: YAML to JSON for API

**Scenario:** Convert YAML config to JSON for REST API consumption.

**Input file (`deployment.yaml`):**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app
  namespace: production
spec:
  selector:
    app: my-app
  ports:
    port: 80
    targetPort: 8080
  type: ClusterIP
```

**Command:**
```bash
python dataconvert.py deployment.yaml --to json --pretty
```

**Output:**
```json
{
  "apiVersion": "v1",
  "kind": "Service",
  "metadata": {
    "name": "my-app",
    "namespace": "production"
  },
  "spec": {
    "selector": {
      "app": "my-app"
    },
    "ports": {
      "port": 80,
      "targetPort": 8080
    },
    "type": "ClusterIP"
  }
}
```

**What You Learned:**
- YAML to JSON for API payloads
- Kubernetes-style YAML supported
- Numbers and strings preserved

---

## Example 6: JSON to XML with Custom Root

**Scenario:** Generate XML report with custom root element.

**Input file (`report.json`):**
```json
{
  "title": "Monthly Sales Report",
  "period": "January 2026",
  "total_sales": 125000,
  "items_sold": 450,
  "top_products": ["Laptop", "Monitor", "Keyboard"]
}
```

**Command:**
```bash
python dataconvert.py report.json --to xml --root sales_report --pretty
```

**Output:**
```xml
<?xml version="1.0" ?>
<sales_report>
  <title>Monthly Sales Report</title>
  <period>January 2026</period>
  <total_sales>125000</total_sales>
  <items_sold>450</items_sold>
  <top_products>
    <item>Laptop</item>
    <item>Monitor</item>
    <item>Keyboard</item>
  </top_products>
</sales_report>
```

**What You Learned:**
- Custom XML root with `--root` flag
- Arrays convert to repeated elements
- Pretty XML output with `--pretty`

---

## Example 7: Batch CSV Processing

**Scenario:** Convert all CSV files in a directory to JSON.

**Bash Script:**
```bash
#!/bin/bash
# convert_all_csv.sh

for file in *.csv; do
  if [ -f "$file" ]; then
    output="${file%.csv}.json"
    echo "Converting $file -> $output"
    python dataconvert.py "$file" --to json --output "$output" --pretty
  fi
done

echo "Done! Converted all CSV files to JSON."
```

**PowerShell Script:**
```powershell
# convert_all_csv.ps1

Get-ChildItem *.csv | ForEach-Object {
    $output = $_.BaseName + ".json"
    Write-Host "Converting $($_.Name) -> $output"
    python dataconvert.py $_.Name --to json --output $output --pretty
}

Write-Host "Done! Converted all CSV files to JSON."
```

**What You Learned:**
- Batch processing with shell scripts
- Cross-platform automation
- Output naming conventions

---

## Example 8: Nested Data Conversion

**Scenario:** Convert deeply nested configuration between formats.

**Input file (`nested.json`):**
```json
{
  "application": {
    "server": {
      "http": {
        "port": 8080,
        "ssl": {
          "enabled": true,
          "cert_path": "/etc/ssl/cert.pem"
        }
      },
      "grpc": {
        "port": 9090,
        "reflection": true
      }
    },
    "logging": {
      "level": "info",
      "handlers": ["console", "file"]
    }
  }
}
```

**Command (JSON → YAML → JSON roundtrip):**
```bash
# Step 1: JSON to YAML
python dataconvert.py nested.json --to yaml --output nested.yaml

# Step 2: YAML back to JSON
python dataconvert.py nested.yaml --to json --output nested_roundtrip.json --pretty
```

**Intermediate (`nested.yaml`):**
```yaml
application:
  server:
    http:
      port: 8080
      ssl:
        enabled: true
        cert_path: /etc/ssl/cert.pem
    grpc:
      port: 9090
      reflection: true
  logging:
    level: info
    handlers:
```

**What You Learned:**
- Deep nesting is preserved
- Format roundtrip testing
- Multi-step conversion workflows

---

## Example 9: Python API Usage

**Scenario:** Use DataConvert programmatically in Python code.

**Python Script:**
```python
#!/usr/bin/env python3
"""Example: Using DataConvert as a library."""

from dataconvert import DataConvert

# Example 1: Parse JSON string
json_data = '{"name": "Test", "values": [1, 2, 3]}'
parsed = DataConvert.json_to_dict(json_data)
print(f"Parsed: {parsed}")
# Output: Parsed: {'name': 'Test', 'values': [1, 2, 3]}

# Example 2: Convert between formats
csv_data = "product,price\nWidget,9.99\nGadget,19.99"
json_result = DataConvert.convert("csv", "json", csv_data)
print(f"CSV -> JSON:\n{json_result}")

# Example 3: Serialize to different formats
data = {"config": {"host": "localhost", "port": 8080}}

# To YAML
yaml_output = DataConvert.dict_to_yaml(data)
print(f"YAML:\n{yaml_output}")

# To XML
xml_output = DataConvert.dict_to_xml(data, root_name="settings")
print(f"XML:\n{xml_output}")

# Example 4: File operations
DataConvert.write_file("output.json", DataConvert.dict_to_json(data))
loaded = DataConvert.json_to_dict(DataConvert.read_file("output.json"))
print(f"Loaded from file: {loaded}")
```

**Output:**
```
Parsed: {'name': 'Test', 'values': [1, 2, 3]}
CSV -> JSON:
[
  {
    "product": "Widget",
    "price": "9.99"
  },
  {
    "product": "Gadget",
    "price": "19.99"
  }
]
YAML:
config:
  host: localhost
  port: 8080
XML:
<?xml version="1.0" ?>
<settings>
  <config>
    <host>localhost</host>
    <port>8080</port>
  </config>
</settings>
Loaded from file: {'config': {'host': 'localhost', 'port': 8080}}
```

**What You Learned:**
- Import DataConvert as a module
- Direct method calls for parsing
- Programmatic format conversion
- File I/O operations

---

## Example 10: Full Production Workflow

**Scenario:** Complete data pipeline - fetch API data (JSON), transform to CSV for analysis, generate XML report.

**Workflow Script:**
```python
#!/usr/bin/env python3
"""
Production Data Pipeline Example

Flow: JSON API Data -> CSV Analysis -> XML Report
"""

import json
from dataconvert import DataConvert

# Step 1: Simulate API response (in production, use requests library)
api_response = '''
{
  "status": "success",
  "data": {
    "orders": [
      {"id": "ORD-001", "customer": "Acme Corp", "total": 1500.00, "status": "shipped"},
      {"id": "ORD-002", "customer": "TechStart", "total": 3200.00, "status": "delivered"},
      {"id": "ORD-003", "customer": "DataFlow", "total": 890.00, "status": "processing"},
      {"id": "ORD-004", "customer": "CloudNine", "total": 2100.00, "status": "shipped"}
    ]
  }
}
'''

# Step 2: Parse JSON and extract orders
data = DataConvert.json_to_dict(api_response)
orders = data["data"]["orders"]
print(f"[INFO] Loaded {len(orders)} orders from API")

# Step 3: Convert to CSV for spreadsheet analysis
csv_output = DataConvert.dict_to_csv(orders)
DataConvert.write_file("orders.csv", csv_output)
print("[OK] Saved orders.csv for analysis")

# Step 4: Calculate summary statistics
total_revenue = sum(float(o["total"]) for o in orders)
shipped_orders = [o for o in orders if o["status"] == "shipped"]

# Step 5: Generate XML report
report_data = {
    "generated": "2026-01-26",
    "total_orders": len(orders),
    "total_revenue": total_revenue,
    "shipped_count": len(shipped_orders),
    "orders": orders
}

xml_report = DataConvert.dict_to_xml(report_data, root_name="sales_report")
DataConvert.write_file("report.xml", xml_report)
print("[OK] Saved report.xml")

# Step 6: Also save as YAML for DevOps
yaml_report = DataConvert.dict_to_yaml(report_data)
DataConvert.write_file("report.yaml", yaml_report)
print("[OK] Saved report.yaml")

print("\n[DONE] Pipeline complete!")
print(f"  - Total orders: {len(orders)}")
print(f"  - Total revenue: ${total_revenue:,.2f}")
print(f"  - Shipped: {len(shipped_orders)}")
```

**Output Files:**

`orders.csv`:
```csv
id,customer,total,status
ORD-001,Acme Corp,1500.0,shipped
ORD-002,TechStart,3200.0,delivered
ORD-003,DataFlow,890.0,processing
ORD-004,CloudNine,2100.0,shipped
```

`report.yaml`:
```yaml
generated: 2026-01-26
total_orders: 4
total_revenue: 7690.0
shipped_count: 2
orders:
  - id: ORD-001
    customer: Acme Corp
    total: 1500.0
    status: shipped
  ...
```

**Console Output:**
```
[INFO] Loaded 4 orders from API
[OK] Saved orders.csv for analysis
[OK] Saved report.xml
[OK] Saved report.yaml

[DONE] Pipeline complete!
  - Total orders: 4
  - Total revenue: $7,690.00
  - Shipped: 2
```

**What You Learned:**
- Complete data pipeline
- Multi-format output generation
- Combining with Python business logic
- Production-ready workflow patterns

---

## Quick Reference

| From | To | Command |
|------|-----|---------|
| JSON | CSV | `dataconvert file.json --to csv` |
| JSON | XML | `dataconvert file.json --to xml --root data` |
| JSON | YAML | `dataconvert file.json --to yaml` |
| CSV | JSON | `dataconvert file.csv --to json --pretty` |
| CSV | XML | `dataconvert file.csv --to xml` |
| CSV | YAML | `dataconvert file.csv --to yaml` |
| XML | JSON | `dataconvert file.xml --to json` |
| XML | CSV | `dataconvert file.xml --to csv` |
| XML | YAML | `dataconvert file.xml --to yaml` |
| YAML | JSON | `dataconvert file.yaml --to json` |
| YAML | CSV | `dataconvert file.yaml --to csv` |
| YAML | XML | `dataconvert file.yaml --to xml` |

---

**Last Updated:** January 2026  
**Maintained By:** FORGE (Team Brain)
