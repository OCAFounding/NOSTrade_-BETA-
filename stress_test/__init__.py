"""
NOS Trade Multi-Agent Stress Test Module

This module provides tools for stress testing the NOS Trade multi-agent trading system.
It simulates multiple trading agents operating concurrently under various stress conditions
to evaluate system performance, reliability, and error handling.
"""

from .multi_agent_simulator import MultiAgentSimulator, run_stress_test

__all__ = ['MultiAgentSimulator', 'run_stress_test'] 