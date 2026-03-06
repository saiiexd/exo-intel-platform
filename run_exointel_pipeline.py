import os
import sys
import subprocess
import time
import argparse
from datetime import datetime

from src.config.config import config
from src.utils.logger import setup_logger
from src.utils.system_health_check import run_health_check

logger = setup_logger("PipelineOrchestrator")

# Core Production Steps
PIPELINE_STEPS = [
    {
        "name": "Dataset Analysis",
        "module": "src.data_analysis.dataset_analysis",
        "description": "Rebuilding cleaned and enriched research dataset..."
    },
    {
        "name": "Habitability Model Training",
        "module": "src.ml_models.train_habitability_model",
        "description": "Training the habitability prediction model..."
    },
    {
        "name": "Planet Discovery Engine",
        "module": "src.discovery.planet_discovery_engine",
        "description": "Ranking habitable planet candidates..."
    },
    {
        "name": "Explainability Engine",
        "module": "src.ml_models.explainability_engine",
        "description": "Computing explainability metrics (SHAP)..."
    },
    {
        "name": "Insight Engine",
        "module": "src.analytics.insight_engine",
        "description": "Generating scientific visualizations..."
    }
]

# Optional Research & Benchmark Steps
RESEARCH_STEPS = [
    {
        "name": "NASA Data Ingestion",
        "module": "src.data_ingestion.nasa_exoplanet_fetcher",
        "description": "Fetching latest confirmed exoplanet data from NASA Archive..."
    },
    {
        "name": "Experiment Orchestrator",
        "module": "src.ml_models.experiment_orchestrator",
        "description": "Running multi-algorithm research experiments..."
    },
    {
        "name": "Benchmark Evaluation",
        "module": "benchmarks.benchmark_scenarios",
        "description": "Evaluating model against scientific benchmarks..."
    },
    {
        "name": "Results Aggregator",
        "module": "src.analytics.results_aggregator",
        "description": "Synthesizing research findings into results/..."
    },
    {
        "name": "Discovery Summary Engine",
        "module": "src.analytics.discovery_summary_engine",
        "description": "Generating scientific research snapshot and formal report..."
    },
    {
        "name": "Platform Metrics Engine",
        "module": "src.metrics.platform_metrics_engine",
        "description": "Capturing operational metrics and system health snapshot..."
    }
]

def run_step(step, step_index, **kwargs):
    step_name = step["name"]
    module_path = step["module"]
    description = step["description"]
    
    logger.info(f"Executing Step {step_index}: {step_name}...")
    print(f"\n[{step_index}] {description}")
    
    start_time = time.time()
    try:
        # For modules that might need extra params (like metrics engine)
        env = os.environ.copy()
        if "duration" in kwargs:
            env["PIPELINE_DURATION"] = str(kwargs["duration"])
            
        result = subprocess.run([sys.executable, "-m", module_path], check=True, capture_output=True, text=True, env=env)
        duration = time.time() - start_time
        print(f"Success: {step_name} completed in {duration:.2f}s.")
        return {
            "step": step_index,
            "name": step_name,
            "status": "SUCCESS",
            "duration": duration,
            "output": result.stdout
        }
    except subprocess.CalledProcessError as e:
        duration = time.time() - start_time
        print(f"Failure: {step_name} FAILED after {duration:.2f}s.")
        print(f"Error:\n{e.stderr}")
        return {
            "step": step_index,
            "name": step_name,
            "status": "FAILED",
            "duration": duration,
            "error": e.stderr
        }

def main():
    parser = argparse.ArgumentParser(description="ExoIntel Autonomous Research Pipeline Orchestrator")
    parser.add_argument("--run-all", action="store_true", help="Execute all production and research steps.")
    parser.add_argument("--refresh-data", action="store_true", help="Fetch latest data from NASA Archive API.")
    parser.add_argument("--run-experiments", action="store_true", help="Perform algorithm benchmarking.")
    parser.add_argument("--run-benchmarks", action="store_true", help="Evaluate model against planetary scenarios.")
    args = parser.parse_args()

    start_time = time.time()
    timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_file_path = os.path.join(config.LOGS_DIR, f"autonomous_report_{timestamp_str}.txt")
    
    print("\n" + "="*60)
    print(f"ExoIntel Autonomous Research-Grade Pipeline")
    print("="*60)
    
    if not run_health_check():
        print("\nAborting: System health check failed.")
        sys.exit(1)
        
    execution_steps = []
    
    # Optional Data Ingestion (Step 0)
    if args.run_all or args.refresh_data:
        execution_steps.append(RESEARCH_STEPS[0])
        
    # Core Production Pipeline
    execution_steps.extend(PIPELINE_STEPS)
    
    # Optional Research Extensions
    if args.run_all or args.run_experiments:
        execution_steps.append(RESEARCH_STEPS[1]) # Experiment Orchestrator
    if args.run_all or args.run_benchmarks:
        execution_steps.append(RESEARCH_STEPS[2]) # Benchmark Evaluation
    if args.run_all:
        execution_steps.append(RESEARCH_STEPS[3]) # Results Aggregator
        
    # Intelligence & Monitoring (Always run at end or if run-all)
    execution_steps.append(RESEARCH_STEPS[4]) # Discovery Summary
    execution_steps.append(RESEARCH_STEPS[5]) # Platform Metrics

    execution_details = []
    pipeline_success = True
    
    for i, step in enumerate(execution_steps, 1):
        # We pass duration to the metrics engine step specifically
        kwargs = {}
        if step["name"] == "Platform Metrics Engine":
            kwargs["duration"] = time.time() - start_time
            
        detail = run_step(step, i, **kwargs)
        execution_details.append(detail)
        if detail["status"] != "SUCCESS":
            pipeline_success = False
            break

    total_duration = time.time() - start_time
    status_str = "SUCCESS" if pipeline_success else "FAILED"
    
    # Final Summary Report
    with open(report_file_path, "w", encoding="utf-8") as f:
        f.write(f"ExoIntel Autonomous Execution Report - {status_str}\n")
        f.write(f"Timestamp: {datetime.now().isoformat()}\n")
        f.write(f"Total Duration: {total_duration:.2f}s\n\n")
        for d in execution_details:
            f.write(f"Step {d['step']}: {d['name']} [{d['status']}] ({d['duration']:.2f}s)\n")

    print("\n" + "="*60)
    print(f"AUTONOMOUS PIPELINE COMPLETE - STATUS: {status_str} - TIME: {total_duration:.2f}s")
    print(f"Report: {report_file_path}")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
