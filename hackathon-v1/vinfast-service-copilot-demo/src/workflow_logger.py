"""
Logging utilities for workflow monitoring
Provides detailed logging at each step of the diagnosis workflow
"""
import logging
import sys
from datetime import datetime
from typing import Any, Dict

class WorkflowLogger:
    """Enhanced logger for workflow steps with formatting"""
    
    def __init__(self, name: str = "VinFastCopilot"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers
        self.logger.handlers = []
        
        # Console handler with formatting
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%H:%M:%S'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def step(self, step_name: str):
        """Log a workflow step"""
        self.logger.info(f"{'='*60}")
        self.logger.info(f"STEP: {step_name}")
        self.logger.info(f"{'='*60}")
    
    def reasoning(self, agent_name: str, reasoning: str):
        """Log agent reasoning"""
        self.logger.info(f"\n🧠 [{agent_name}] REASONING:")
        for line in reasoning.split('\n'):
            if line.strip():
                self.logger.info(f"   {line}")
    
    def tool_call(self, tool_name: str, params: Dict[str, Any]):
        """Log tool invocation"""
        self.logger.info(f"\n🔧 TOOL CALL: {tool_name}")
        for key, value in params.items():
            if isinstance(value, (str, int, float, bool)):
                self.logger.info(f"   ├─ {key}: {value}")
            else:
                self.logger.info(f"   ├─ {key}: {type(value).__name__}")
    
    def tool_result(self, tool_name: str, result: Any):
        """Log tool result"""
        self.logger.info(f"\n📤 TOOL RESULT: {tool_name}")
        if isinstance(result, dict):
            for key, value in result.items():
                if isinstance(value, str) and len(value) > 100:
                    self.logger.info(f"   ├─ {key}: {value[:100]}...")
                else:
                    self.logger.info(f"   ├─ {key}: {value}")
        elif isinstance(result, list):
            self.logger.info(f"   ├─ Length: {len(result)}")
            for i, item in enumerate(result[:3]):
                self.logger.info(f"   ├─ [{i}]: {item}")
        else:
            self.logger.info(f"   └─ Result: {str(result)[:200]}")
    
    def state_update(self, field: str, value: Any):
        """Log state changes"""
        if isinstance(value, str) and len(value) > 100:
            display_value = value[:100] + "..."
        else:
            display_value = value
        self.logger.info(f"📍 STATE UPDATE: {field} = {display_value}")
    
    def confidence(self, score: float, threshold: float = 0.7):
        """Log confidence score"""
        status = "✅ HIGH" if score >= threshold else "⚠️  LOW"
        self.logger.info(f"📊 CONFIDENCE: {status} ({score:.2f})")
    
    def success(self, message: str):
        """Log success"""
        self.logger.info(f"\n✅ SUCCESS: {message}")
    
    def warning(self, message: str):
        """Log warning"""
        self.logger.warning(f"\n⚠️  WARNING: {message}")
    
    def error(self, message: str):
        """Log error"""
        self.logger.error(f"\n❌ ERROR: {message}")
    
    def info(self, message: str):
        """Log info"""
        self.logger.info(f"ℹ️  {message}")
    
    def section(self, title: str):
        """Log section header"""
        self.logger.info(f"\n{'─'*60}")
        self.logger.info(f"  {title.upper()}")
        self.logger.info(f"{'─'*60}")

# Global logger instance
workflow_logger = WorkflowLogger()

def log_workflow_step(stage: str, details: Dict = None):
    """Helper function to log workflow steps"""
    workflow_logger.step(stage)
    if details:
        for key, value in details.items():
            workflow_logger.state_update(key, value)

def log_agent_input(agent_name: str, inputs: Dict):
    """Log agent inputs"""
    workflow_logger.section(f"{agent_name} Input")
    for key, value in inputs.items():
        if isinstance(value, str) and len(value) > 100:
            workflow_logger.info(f"{key}: {value[:100]}...")
        else:
            workflow_logger.info(f"{key}: {value}")

def log_agent_output(agent_name: str, outputs: Dict):
    """Log agent outputs"""
    workflow_logger.section(f"{agent_name} Output")
    for key, value in outputs.items():
        if isinstance(value, str) and len(value) > 100:
            workflow_logger.info(f"{key}: {value[:100]}...")
        else:
            workflow_logger.info(f"{key}: {value}")
