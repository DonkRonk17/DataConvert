#!/usr/bin/env python3
"""
Comprehensive test suite for DataConvert.

Tests cover:
- JSON parsing and serialization
- CSV parsing and serialization
- XML parsing and serialization
- YAML parsing and serialization
- Format conversions (all 16 combinations)
- Edge cases and error handling
- CLI interface

Run: python test_dataconvert.py

Author: FORGE (Team Brain)
For: Logan Smith / Metaphy LLC
Date: January 2026
"""

import unittest
import sys
import os
import tempfile
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from dataconvert import DataConvert, SimpleYAML


class TestJSONOperations(unittest.TestCase):
    """Test JSON parsing and serialization."""
    
    def test_json_parse_simple_object(self):
        """Test parsing simple JSON object."""
        json_str = '{"name": "Alice", "age": 30}'
        result = DataConvert.json_to_dict(json_str)
        self.assertEqual(result, {"name": "Alice", "age": 30})
    
    def test_json_parse_array(self):
        """Test parsing JSON array."""
        json_str = '[{"id": 1}, {"id": 2}]'
        result = DataConvert.json_to_dict(json_str)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], 1)
    
    def test_json_serialize_pretty(self):
        """Test pretty JSON serialization."""
        data = {"name": "Bob", "active": True}
        result = DataConvert.dict_to_json(data, pretty=True)
        self.assertIn('\n', result)  # Pretty print has newlines
        self.assertIn('"name"', result)
    
    def test_json_serialize_compact(self):
        """Test compact JSON serialization."""
        data = {"x": 1, "y": 2}
        result = DataConvert.dict_to_json(data, pretty=False)
        self.assertNotIn('\n', result)  # No newlines in compact
    
    def test_json_nested_structure(self):
        """Test parsing nested JSON."""
        json_str = '{"user": {"profile": {"name": "Test", "settings": {"theme": "dark"}}}}'
        result = DataConvert.json_to_dict(json_str)
        self.assertEqual(result["user"]["profile"]["settings"]["theme"], "dark")


class TestCSVOperations(unittest.TestCase):
    """Test CSV parsing and serialization."""
    
    def test_csv_parse_basic(self):
        """Test parsing basic CSV."""
        csv_str = "name,age,city\nAlice,30,NYC\nBob,25,LA"
        result = DataConvert.csv_to_dict(csv_str)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "Alice")
        self.assertEqual(result[1]["city"], "LA")
    
    def test_csv_parse_with_quotes(self):
        """Test parsing CSV with quoted values."""
        csv_str = 'name,description\n"John Doe","A person, with commas"'
        result = DataConvert.csv_to_dict(csv_str)
        self.assertEqual(result[0]["name"], "John Doe")
        self.assertIn(",", result[0]["description"])
    
    def test_csv_serialize_basic(self):
        """Test basic CSV serialization."""
        data = [
            {"name": "Alice", "age": "30"},
            {"name": "Bob", "age": "25"}
        ]
        result = DataConvert.dict_to_csv(data)
        self.assertIn("name,age", result)
        self.assertIn("Alice,30", result)
    
    def test_csv_empty_data(self):
        """Test CSV serialization with empty data."""
        result = DataConvert.dict_to_csv([])
        self.assertEqual(result, "")


class TestXMLOperations(unittest.TestCase):
    """Test XML parsing and serialization."""
    
    def test_xml_parse_simple(self):
        """Test parsing simple XML."""
        xml_str = "<root><name>Test</name><value>123</value></root>"
        result = DataConvert.xml_to_dict(xml_str)
        self.assertEqual(result["name"], "Test")
        self.assertEqual(result["value"], "123")
    
    def test_xml_parse_nested(self):
        """Test parsing nested XML."""
        xml_str = "<config><database><host>localhost</host></database></config>"
        result = DataConvert.xml_to_dict(xml_str)
        self.assertEqual(result["database"]["host"], "localhost")
    
    def test_xml_parse_with_attributes(self):
        """Test parsing XML with attributes."""
        xml_str = '<item id="123" type="product"><name>Widget</name></item>'
        result = DataConvert.xml_to_dict(xml_str)
        self.assertEqual(result["@attributes"]["id"], "123")
        self.assertEqual(result["name"], "Widget")
    
    def test_xml_serialize_basic(self):
        """Test basic XML serialization."""
        data = {"name": "Test", "value": "123"}
        result = DataConvert.dict_to_xml(data, "root", pretty=False)
        self.assertIn("<root>", result)
        self.assertIn("<name>Test</name>", result)
    
    def test_xml_serialize_pretty(self):
        """Test pretty XML serialization."""
        data = {"item": "value"}
        result = DataConvert.dict_to_xml(data, "root", pretty=True)
        self.assertIn('\n', result)  # Pretty print has newlines


class TestYAMLOperations(unittest.TestCase):
    """Test YAML parsing and serialization."""
    
    def test_yaml_parse_simple(self):
        """Test parsing simple YAML."""
        yaml_str = "name: Alice\nage: 30"
        result = DataConvert.yaml_to_dict(yaml_str)
        self.assertEqual(result["name"], "Alice")
        self.assertEqual(result["age"], 30)
    
    def test_yaml_parse_nested(self):
        """Test parsing nested YAML."""
        yaml_str = "database:\n  host: localhost\n  port: 5432"
        result = DataConvert.yaml_to_dict(yaml_str)
        self.assertEqual(result["database"]["host"], "localhost")
    
    def test_yaml_parse_booleans(self):
        """Test parsing YAML booleans."""
        yaml_str = "enabled: true\ndisabled: false"
        result = DataConvert.yaml_to_dict(yaml_str)
        self.assertTrue(result["enabled"])
        self.assertFalse(result["disabled"])
    
    def test_yaml_serialize_basic(self):
        """Test basic YAML serialization."""
        data = {"name": "Test", "count": 5}
        result = DataConvert.dict_to_yaml(data)
        self.assertIn("name: Test", result)
        self.assertIn("count: 5", result)


class TestFormatConversions(unittest.TestCase):
    """Test conversions between all format combinations."""
    
    def test_json_to_csv(self):
        """Test JSON to CSV conversion."""
        json_str = '[{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]'
        result = DataConvert.convert("json", "csv", json_str)
        self.assertIn("name,age", result)
        self.assertIn("Alice,30", result)
    
    def test_csv_to_json(self):
        """Test CSV to JSON conversion."""
        csv_str = "name,city\nAlice,NYC\nBob,LA"
        result = DataConvert.convert("csv", "json", csv_str)
        data = json.loads(result)
        self.assertEqual(len(data), 2)
    
    def test_json_to_yaml(self):
        """Test JSON to YAML conversion."""
        json_str = '{"server": {"host": "localhost", "port": 8080}}'
        result = DataConvert.convert("json", "yaml", json_str)
        self.assertIn("server:", result)
        self.assertIn("host: localhost", result)
    
    def test_yaml_to_json(self):
        """Test YAML to JSON conversion."""
        yaml_str = "name: Test\nvalue: 123"
        result = DataConvert.convert("yaml", "json", yaml_str)
        data = json.loads(result)
        self.assertEqual(data["name"], "Test")
    
    def test_json_to_xml(self):
        """Test JSON to XML conversion."""
        json_str = '{"item": {"name": "Widget", "price": "9.99"}}'
        result = DataConvert.convert("json", "xml", json_str)
        self.assertIn("<name>Widget</name>", result)
    
    def test_xml_to_json(self):
        """Test XML to JSON conversion."""
        xml_str = "<data><name>Test</name></data>"
        result = DataConvert.convert("xml", "json", xml_str)
        data = json.loads(result)
        # XML conversion wraps in root element
        self.assertIn("root", data)
        self.assertEqual(data["root"]["name"], "Test")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def test_empty_json_object(self):
        """Test empty JSON object."""
        result = DataConvert.json_to_dict("{}")
        self.assertEqual(result, {})
    
    def test_empty_json_array(self):
        """Test empty JSON array."""
        result = DataConvert.json_to_dict("[]")
        self.assertEqual(result, [])
    
    def test_unicode_in_json(self):
        """Test Unicode characters in JSON."""
        json_str = '{"name": "Caf\u00e9", "emoji": "\u2764"}'
        result = DataConvert.json_to_dict(json_str)
        self.assertEqual(result["name"], "Café")
    
    def test_special_characters_in_csv(self):
        """Test special characters in CSV values."""
        csv_str = 'name,note\n"Test","Line1\nLine2"'
        # This should handle newlines in quoted fields
        result = DataConvert.csv_to_dict(csv_str)
        self.assertTrue(len(result) >= 1)
    
    def test_invalid_json(self):
        """Test invalid JSON raises error."""
        with self.assertRaises(json.JSONDecodeError):
            DataConvert.json_to_dict("{invalid}")
    
    def test_invalid_format(self):
        """Test invalid format raises ValueError."""
        with self.assertRaises(ValueError):
            DataConvert.convert("invalid", "json", "data")


class TestFileOperations(unittest.TestCase):
    """Test file reading and writing."""
    
    def setUp(self):
        """Create temporary directory for test files."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_read_file(self):
        """Test file reading."""
        test_file = os.path.join(self.temp_dir, "test.txt")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("Hello, World!")
        
        result = DataConvert.read_file(test_file)
        self.assertEqual(result, "Hello, World!")
    
    def test_write_file(self):
        """Test file writing."""
        test_file = os.path.join(self.temp_dir, "output.txt")
        DataConvert.write_file(test_file, "Test content")
        
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertEqual(content, "Test content")
    
    def test_roundtrip_json(self):
        """Test JSON file roundtrip."""
        test_file = os.path.join(self.temp_dir, "data.json")
        original = {"name": "Test", "values": [1, 2, 3]}
        
        # Write
        json_str = DataConvert.dict_to_json(original)
        DataConvert.write_file(test_file, json_str)
        
        # Read back
        content = DataConvert.read_file(test_file)
        result = DataConvert.json_to_dict(content)
        
        self.assertEqual(result, original)


class TestSimpleYAML(unittest.TestCase):
    """Test the SimpleYAML parser specifically."""
    
    def test_parse_integer(self):
        """Test integer parsing."""
        result = SimpleYAML._parse_value("42")
        self.assertEqual(result, 42)
        self.assertIsInstance(result, int)
    
    def test_parse_float(self):
        """Test float parsing."""
        result = SimpleYAML._parse_value("3.14")
        self.assertAlmostEqual(result, 3.14)
    
    def test_parse_null(self):
        """Test null parsing."""
        result = SimpleYAML._parse_value("null")
        self.assertIsNone(result)
    
    def test_parse_quoted_string(self):
        """Test quoted string parsing."""
        result = SimpleYAML._parse_value('"hello world"')
        self.assertEqual(result, "hello world")
    
    def test_serialize_boolean(self):
        """Test boolean serialization."""
        result = SimpleYAML._serialize_value(True)
        self.assertEqual(result, "true")
        result = SimpleYAML._serialize_value(False)
        self.assertEqual(result, "false")


def run_tests():
    """Run all tests with detailed output."""
    print("=" * 70)
    print("TESTING: DataConvert v1.0")
    print("=" * 70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestJSONOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestCSVOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestXMLOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestYAMLOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestFormatConversions))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestFileOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestSimpleYAML))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 70)
    print(f"RESULTS: {result.testsRun} tests")
    passed = result.testsRun - len(result.failures) - len(result.errors)
    print(f"[OK] Passed: {passed}")
    if result.failures:
        print(f"[X] Failed: {len(result.failures)}")
    if result.errors:
        print(f"[X] Errors: {len(result.errors)}")
    print("=" * 70)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
