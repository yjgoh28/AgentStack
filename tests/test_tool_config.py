import os, sys
import unittest
import importlib.resources
from pathlib import Path
from agentstack.generation.tool_generation import get_package_path, ToolConfig

BASE_PATH = Path(__file__).parent

def all_tool_names():
    tools_dir = get_package_path() / 'tools'
    for file in tools_dir.iterdir():
        if file.is_file() and file.suffix == '.json':
            yield file.stem

class ToolConfigTest(unittest.TestCase):
    def test_minimal_json(self):
        config = ToolConfig.from_json(BASE_PATH / "fixtures/tool_config_min.json")
        assert config.name == "tool_name"
        assert config.category == "category"
        assert config.tools == ["tool1", "tool2"]
        assert config.url is None
        assert config.tools_bundled is False
        assert config.cta is None
        assert config.env is None
        assert config.packages is None
        assert config.post_install is None
        assert config.post_remove is None
    
    def test_maximal_json(self):
        config = ToolConfig.from_json(BASE_PATH / "fixtures/tool_config_max.json")
        assert config.name == "tool_name"
        assert config.category == "category"
        assert config.tools == ["tool1", "tool2"]
        assert config.url == "https://example.com"
        assert config.tools_bundled is True
        assert config.cta == "Click me!"
        assert config.env == "test"
        assert config.packages == ["package1", "package2"]
        assert config.post_install == "install.sh"
        assert config.post_remove == "remove.sh"
    
    def test_all_json_configs_from_tool_name(self):
        for tool_name in all_tool_names():
            config = ToolConfig.from_tool_name(tool_name)
            assert config.name == tool_name
            # We can assume that pydantic validation caught any other issues

