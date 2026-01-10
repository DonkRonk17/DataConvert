#!/usr/bin/env python3
"""
DataConvert - Universal Data Format Converter
Convert between JSON, CSV, XML, and YAML formats with ease. Zero dependencies!
"""

import os
import sys
import io
import json
import csv
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import argparse
import re
from typing import Any, Dict, List, Union
from pathlib import Path

# Fix Unicode output on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Simple YAML parser/serializer (no external dependencies!)
class SimpleYAML:
    """Minimal YAML parser and serializer for basic structures"""
    
    @staticmethod
    def parse(text: str) -> Any:
        """Parse simple YAML to Python dict/list"""
        lines = text.strip().split('\n')
        return SimpleYAML._parse_lines(lines)
    
    @staticmethod
    def _parse_lines(lines: List[str], indent=0) -> Any:
        """Recursively parse YAML lines"""
        result = {}
        current_key = None
        list_items = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            if not stripped or stripped.startswith('#'):
                i += 1
                continue
            
            line_indent = len(line) - len(line.lstrip())
            
            if line_indent < indent:
                break
            
            if line_indent > indent:
                i += 1
                continue
            
            # List item
            if stripped.startswith('- '):
                value = stripped[2:].strip()
                if ':' in value:
                    # Dict in list
                    key, val = value.split(':', 1)
                    list_items.append({key.strip(): SimpleYAML._parse_value(val.strip())})
                else:
                    list_items.append(SimpleYAML._parse_value(value))
                i += 1
                continue
            
            # Key-value pair
            if ':' in stripped:
                key, value = stripped.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                if value:
                    result[key] = SimpleYAML._parse_value(value)
                else:
                    # Check if next line is indented (nested structure)
                    if i + 1 < len(lines):
                        next_line = lines[i + 1]
                        next_indent = len(next_line) - len(next_line.lstrip())
                        if next_indent > line_indent:
                            # Nested structure
                            sub_lines = []
                            j = i + 1
                            while j < len(lines):
                                sub_line = lines[j]
                                sub_indent = len(sub_line) - len(sub_line.lstrip())
                                if sub_indent <= line_indent and sub_line.strip():
                                    break
                                sub_lines.append(sub_line)
                                j += 1
                            result[key] = SimpleYAML._parse_lines(sub_lines, next_indent)
                            i = j
                            continue
                    else:
                        result[key] = None
            
            i += 1
        
        return list_items if list_items else result
    
    @staticmethod
    def _parse_value(value: str) -> Any:
        """Parse YAML value to Python type"""
        if not value or value == 'null':
            return None
        if value == 'true':
            return True
        if value == 'false':
            return False
        if value.isdigit():
            return int(value)
        try:
            return float(value)
        except ValueError:
            # Remove quotes if present
            if (value.startswith('"') and value.endswith('"')) or \
               (value.startswith("'") and value.endswith("'")):
                return value[1:-1]
            return value
    
    @staticmethod
    def serialize(data: Any, indent=0) -> str:
        """Serialize Python dict/list to YAML"""
        lines = []
        ind = '  ' * indent
        
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    lines.append(f"{ind}{key}:")
                    lines.append(SimpleYAML.serialize(value, indent + 1))
                else:
                    lines.append(f"{ind}{key}: {SimpleYAML._serialize_value(value)}")
        
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    lines.append(f"{ind}- ")
                    sub = SimpleYAML.serialize(item, indent + 1)
                    lines.append(sub.replace(ind + '  ', ind + '  ', 1))
                else:
                    lines.append(f"{ind}- {SimpleYAML._serialize_value(item)}")
        
        else:
            return str(data)
        
        return '\n'.join(lines)
    
    @staticmethod
    def _serialize_value(value: Any) -> str:
        """Serialize Python value to YAML"""
        if value is None:
            return 'null'
        if isinstance(value, bool):
            return 'true' if value else 'false'
        if isinstance(value, str) and (' ' in value or ':' in value):
            return f'"{value}"'
        return str(value)


class DataConvert:
    """Universal data format converter"""
    
    @staticmethod
    def read_file(filepath: str) -> str:
        """Read file content"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    @staticmethod
    def write_file(filepath: str, content: str):
        """Write content to file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    @staticmethod
    def json_to_dict(json_str: str) -> Union[Dict, List]:
        """Parse JSON string"""
        return json.loads(json_str)
    
    @staticmethod
    def dict_to_json(data: Union[Dict, List], pretty: bool = True) -> str:
        """Convert dict/list to JSON"""
        if pretty:
            return json.dumps(data, indent=2, ensure_ascii=False)
        return json.dumps(data, ensure_ascii=False)
    
    @staticmethod
    def csv_to_dict(csv_str: str) -> List[Dict]:
        """Parse CSV string"""
        lines = csv_str.strip().split('\n')
        reader = csv.DictReader(lines)
        return list(reader)
    
    @staticmethod
    def dict_to_csv(data: List[Dict]) -> str:
        """Convert list of dicts to CSV"""
        if not data:
            return ""
        
        output = io.StringIO()
        fieldnames = list(data[0].keys())
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()
    
    @staticmethod
    def xml_to_dict(xml_str: str) -> Dict:
        """Parse XML string"""
        root = ET.fromstring(xml_str)
        return DataConvert._element_to_dict(root)
    
    @staticmethod
    def _element_to_dict(element: ET.Element) -> Dict:
        """Convert XML element to dict"""
        result = {}
        
        # Add attributes
        if element.attrib:
            result['@attributes'] = element.attrib
        
        # Add text content
        if element.text and element.text.strip():
            result['#text'] = element.text.strip()
        
        # Add children
        for child in element:
            child_data = DataConvert._element_to_dict(child)
            if child.tag in result:
                # Multiple elements with same tag -> make it a list
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_data)
            else:
                result[child.tag] = child_data
        
        # Simplify single-text elements
        if len(result) == 1 and '#text' in result:
            return result['#text']
        
        return result if result else None
    
    @staticmethod
    def dict_to_xml(data: Dict, root_name: str = 'root', pretty: bool = True) -> str:
        """Convert dict to XML"""
        root = DataConvert._dict_to_element(data, root_name)
        xml_str = ET.tostring(root, encoding='unicode')
        
        if pretty:
            dom = minidom.parseString(xml_str)
            return dom.toprettyxml(indent='  ')
        return xml_str
    
    @staticmethod
    def _dict_to_element(data: Any, tag: str) -> ET.Element:
        """Convert dict to XML element"""
        element = ET.Element(tag)
        
        if isinstance(data, dict):
            # Handle attributes
            if '@attributes' in data:
                element.attrib.update(data['@attributes'])
            
            for key, value in data.items():
                if key == '@attributes':
                    continue
                if key == '#text':
                    element.text = str(value)
                elif isinstance(value, list):
                    for item in value:
                        element.append(DataConvert._dict_to_element(item, key))
                else:
                    element.append(DataConvert._dict_to_element(value, key))
        
        elif isinstance(data, list):
            for item in data:
                element.append(DataConvert._dict_to_element(item, 'item'))
        
        else:
            element.text = str(data) if data is not None else ''
        
        return element
    
    @staticmethod
    def yaml_to_dict(yaml_str: str) -> Union[Dict, List]:
        """Parse YAML string"""
        return SimpleYAML.parse(yaml_str)
    
    @staticmethod
    def dict_to_yaml(data: Union[Dict, List]) -> str:
        """Convert dict/list to YAML"""
        return SimpleYAML.serialize(data)
    
    @staticmethod
    def convert(input_format: str, output_format: str, data_str: str, root_name: str = 'root') -> str:
        """Convert between formats"""
        # Parse input
        if input_format == 'json':
            data = DataConvert.json_to_dict(data_str)
        elif input_format == 'csv':
            data = DataConvert.csv_to_dict(data_str)
        elif input_format == 'xml':
            data = DataConvert.xml_to_dict(data_str)
            data = {root_name: data}  # Wrap in root
        elif input_format == 'yaml':
            data = DataConvert.yaml_to_dict(data_str)
        else:
            raise ValueError(f"Unsupported input format: {input_format}")
        
        # Convert to output
        if output_format == 'json':
            return DataConvert.dict_to_json(data)
        elif output_format == 'csv':
            # CSV requires list of dicts
            if isinstance(data, dict):
                data = [data]
            return DataConvert.dict_to_csv(data)
        elif output_format == 'xml':
            # Extract root if wrapped
            if isinstance(data, dict) and len(data) == 1:
                root_key = list(data.keys())[0]
                return DataConvert.dict_to_xml(data[root_key], root_key)
            return DataConvert.dict_to_xml(data, root_name)
        elif output_format == 'yaml':
            return DataConvert.dict_to_yaml(data)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="DataConvert - Universal Data Format Converter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Supported formats: json, csv, xml, yaml

Examples:
  dataconvert data.json --to csv                # JSON to CSV
  dataconvert data.csv --to json --output out.json
  dataconvert data.xml --to yaml
  dataconvert data.json --to xml --root config
  dataconvert data.yaml --to json --pretty
        """
    )
    
    parser.add_argument('input', help='Input file')
    parser.add_argument('--to', required=True, choices=['json', 'csv', 'xml', 'yaml'],
                       help='Output format')
    parser.add_argument('--output', '-o', help='Output file (default: stdout)')
    parser.add_argument('--root', default='root', help='Root element name for XML')
    parser.add_argument('--pretty', action='store_true', help='Pretty print output')
    
    args = parser.parse_args()
    
    # Detect input format from extension
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ File not found: {args.input}")
        return 1
    
    input_ext = input_path.suffix.lower().lstrip('.')
    if input_ext not in ['json', 'csv', 'xml', 'yaml', 'yml']:
        print(f"❌ Unsupported input format: {input_ext}")
        print("💡 Supported: json, csv, xml, yaml")
        return 1
    
    if input_ext == 'yml':
        input_ext = 'yaml'
    
    try:
        # Read input
        print(f"📖 Reading {input_ext.upper()} from: {args.input}")
        content = DataConvert.read_file(str(input_path))
        
        # Convert
        print(f"🔄 Converting {input_ext.upper()} → {args.to.upper()}...")
        result = DataConvert.convert(input_ext, args.to, content, args.root)
        
        # Output
        if args.output:
            DataConvert.write_file(args.output, result)
            print(f"✅ Saved to: {args.output}")
        else:
            print(f"\n{'='*60}")
            print(result)
            print(f"{'='*60}\n")
        
        return 0
    
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        return 1
    except ET.ParseError as e:
        print(f"❌ Invalid XML: {e}")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n👋 Conversion cancelled")
        sys.exit(1)
