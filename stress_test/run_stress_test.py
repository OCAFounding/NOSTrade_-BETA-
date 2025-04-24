#!/usr/bin/env python3
"""
NOS Trade Multi-Agent Stress Test Runner

This script runs the multi-agent stress test with configurable parameters.
"""

import argparse
import logging
import os
import sys
from datetime import datetime

from stress_test.multi_agent_simulator import run_stress_test
from stress_test.visualization import generate_visualization_report

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run NOS Trade multi-agent stress test")
    
    # Agent configuration
    parser.add_argument("--agents", nargs="+", help="List of agent names to simulate")
    parser.add_argument("--tasks", nargs="+", help="List of tasks to perform")
    
    # Probability settings
    parser.add_argument("--missing-data-prob", type=float, default=0.2,
                        help="Probability of missing data (0.0-1.0)")
    parser.add_argument("--failure-prob", type=float, default=0.1,
                        help="Probability of task failure (0.0-1.0)")
    
    # Operation settings
    parser.add_argument("--operations", type=int, default=100,
                        help="Number of operations each agent performs")
    parser.add_argument("--min-delay", type=float, default=0.05,
                        help="Minimum delay between operations in seconds")
    parser.add_argument("--max-delay", type=float, default=0.15,
                        help="Maximum delay between operations in seconds")
    
    # Output settings
    parser.add_argument("--output-dir", default="stress_test_output",
                        help="Directory to store output files")
    parser.add_argument("--no-visualization", action="store_true",
                        help="Skip visualization report generation")
    
    # Logging settings
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        default="INFO", help="Logging level")
    
    return parser.parse_args()

def main():
    """Main entry point."""
    args = parse_args()
    
    # Configure logging
    log_file = os.path.join(args.output_dir, f"stress_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    os.makedirs(args.output_dir, exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Starting NOS Trade multi-agent stress test")
    logger.info(f"Output directory: {args.output_dir}")
    
    # Run the stress test
    try:
        stats = run_stress_test(
            agents=args.agents,
            tasks=args.tasks,
            missing_data_prob=args.missing_data_prob,
            failure_prob=args.failure_prob,
            operations_per_agent=args.operations,
            min_delay=args.min_delay,
            max_delay=args.max_delay,
            output_dir=args.output_dir
        )
        
        # Print summary
        print("\nStress Test Summary:")
        print(f"Total operations: {stats['total_operations']}")
        print(f"Successful operations: {stats['successful_operations']}")
        print(f"Failed operations: {stats['failed_operations']}")
        print(f"Missing data events: {stats['missing_data_events']}")
        print(f"Start time: {stats['start_time']}")
        print(f"End time: {stats['end_time']}")
        
        # Generate visualization report if requested
        if not args.no_visualization:
            logger.info("Generating visualization report")
            generate_visualization_report(args.output_dir)
            print(f"\nVisualization report generated: {os.path.join(args.output_dir, 'stress_test_report.html')}")
        
        logger.info("Stress test completed successfully")
        return 0
    
    except Exception as e:
        logger.exception("Error during stress test")
        print(f"\nError: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 