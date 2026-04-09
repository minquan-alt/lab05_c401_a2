#!/usr/bin/env python3
"""
VinFast Service Copilot Demo Runner
"""
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    import streamlit as st
    import main
    # This will be run by streamlit