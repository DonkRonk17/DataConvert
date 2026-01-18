<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/69627208-1584-4127-af8f-a32aa8a2803e" />

# 🔄 DataConvert - Universal Data Format Converter

**Simple. Fast. Zero Dependencies.**

Convert between JSON, CSV, XML, and YAML formats from the command line. No external packages required!

---

## 🎯 Why DataConvert?

**Problem:** Developers need to convert between data formats but:
- Use online tools (privacy risk, requires internet)
- Remember different commands/tools for each conversion
- Install heavy libraries for simple conversions

**Solution:** DataConvert provides:
- ✅ **All formats** - JSON, CSV, XML, YAML
- ✅ **Zero dependencies** - Pure Python standard library
- ✅ **Offline** - No internet required
- ✅ **Simple syntax** - One command for all conversions
- ✅ **Pretty printing** - Human-readable output
- ✅ **Cross-platform** - Works on Windows, macOS, Linux

---

## 🚀 Quick Start

```bash
# JSON to CSV
python dataconvert.py data.json --to csv

# CSV to JSON
python dataconvert.py data.csv --to json --output result.json

# JSON to YAML
python dataconvert.py config.json --to yaml

# XML to JSON
python dataconvert.py data.xml --to json
```

---

## 📖 Usage Guide

### Basic Conversion

```bash
# Syntax
python dataconvert.py <input_file> --to <format> [options]

# Formats: json, csv, xml, yaml

# Output to stdout (default)
python dataconvert.py data.json --to csv

# Output to file
python dataconvert.py data.json --to csv --output data.csv
# or
python dataconvert.py data.json --to csv -o data.csv
```

### Format-Specific Options

```bash
# XML: Specify root element name
python dataconvert.py data.json --to xml --root config

# Pretty print
python dataconvert.py data.json --to yaml --pretty
```

---

## 💡 Examples

### Example 1: JSON → CSV

Input (`users.json`):
```json
[
  {"name": "Alice", "age": 30, "city": "NYC"},
  {"name": "Bob", "age": 25, "city": "LA"}
]
```

Command:
```bash
python dataconvert.py users.json --to csv
```

Output:
```csv
name,age,city
Alice,30,NYC
Bob,25,LA
```

### Example 2: CSV → JSON

Input (`data.csv`):
```csv
product,price,stock
Laptop,999,15
Mouse,25,100
```

Command:
```bash
python dataconvert.py data.csv --to json --pretty
```

Output:
```json
[
  {
    "product": "Laptop",
    "price": "999",
    "stock": "15"
  },
  {
    "product": "Mouse",
    "price": "25",
    "stock": "100"
  }
]
```

### Example 3: JSON → YAML

Input (`config.json`):
```json
{
  "database": {
    "host": "localhost",
    "port": 5432,
    "name": "mydb"
  },
  "debug": true
}
```

Command:
```bash
python dataconvert.py config.json --to yaml
```

Output:
```yaml
database:
  host: localhost
  port: 5432
  name: mydb
debug: true
```

### Example 4: XML → JSON

Input (`data.xml`):
```xml
<users>
  <user>
    <name>Alice</name>
    <age>30</age>
  </user>
</users>
```

Command:
```bash
python dataconvert.py data.xml --to json
```

Output:
```json
{
  "users": {
    "user": {
      "name": "Alice",
      "age": "30"
    }
  }
}
```

---

## 🔄 Supported Conversions

All combinations supported:

| From ↓ / To → | JSON | CSV | XML | YAML |
|---------------|------|-----|-----|------|
| **JSON**      | ✅   | ✅  | ✅  | ✅   |
| **CSV**       | ✅   | ✅  | ✅  | ✅   |
| **XML**       | ✅   | ✅  | ✅  | ✅   |
| **YAML**      | ✅   | ✅  | ✅  | ✅   |

---

## 🔧 Use Cases

### For Developers
- Convert API responses (JSON) to CSV for analysis
- Transform config files between formats
- Parse XML data to JSON for processing
- Convert data for different tools/platforms

### For Data Analysis
- Convert JSON to CSV for Excel/spreadsheets
- Transform database exports between formats
- Prepare data for different analysis tools
- Convert scraping results to usable formats

### For DevOps
- Convert config files (JSON ↔ YAML)
- Transform deployment manifests
- Parse various log/data formats
- Standardize data across systems

---

## ❓ FAQ

### Q: Do I need to install anything?
**A:** Just Python 3.6+. No external packages required!

### Q: How does YAML work without PyYAML?
**A:** DataConvert includes a simple built-in YAML parser for basic structures. For complex YAML, use PyYAML separately.

### Q: Can it handle large files?
**A:** Yes, but very large files (>100MB) may be slow. For huge datasets, use streaming tools.

### Q: What about nested data?
**A:** JSON, XML, and YAML support nesting. CSV is flat, so nested data gets simplified.

### Q: Is the conversion lossless?
**A:** Mostly yes, but:
- CSV → other formats may lose data types (everything becomes strings)
- XML attributes may be represented differently
- Very complex YAML may not parse correctly

### Q: Can I batch convert files?
**A:** Not built-in, but easy with shell scripts:
```bash
# Convert all JSON files to CSV
for file in *.json; do
  python dataconvert.py "$file" --to csv -o "${file%.json}.csv"
done
```

---

## 🎨 Pretty Printing

```bash
# Pretty print JSON (indented)
python dataconvert.py data.csv --to json --pretty

# Pretty print XML (indented)
python dataconvert.py data.json --to xml --pretty

# YAML is always pretty (by design)
python dataconvert.py data.json --to yaml
```

---

## 📄 License

MIT License - Free to use, modify, and distribute.

---

<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/5bc8f0f3-33a9-4bba-910f-0d002b7f7d21" />



## 🤝 Contributing

Contributions welcome! Especially:
- Better YAML support
- Performance optimizations
- Additional format support (TOML, INI, etc.)

---

## 🚀 Quick Reference

```bash
# JSON conversions
dataconvert file.json --to csv
dataconvert file.json --to xml --root data
dataconvert file.json --to yaml

# CSV conversions  
dataconvert file.csv --to json
dataconvert file.csv --to xml
dataconvert file.csv --to yaml

# XML conversions
dataconvert file.xml --to json
dataconvert file.xml --to csv
dataconvert file.xml --to yaml

# YAML conversions
dataconvert file.yaml --to json
dataconvert file.yaml --to csv
dataconvert file.yaml --to xml

# With output file
dataconvert input.json --to csv -o output.csv
```

---

## 🙏 Credits

Created by **Randell Logan Smith and Team Brain** at [Metaphy LLC](https://metaphysicsandcomputing.com)

Part of the HMSS (Heavenly Morning Star System) ecosystem.

---

**🔄 Convert all the things!**
