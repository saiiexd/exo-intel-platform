import os
import sys
import subprocess
import time
from datetime import datetime

from src.config.config import config
from src.utils.logger import setup_logger
from src.utils.system_health_check import run_health_check

logger = setup_logger("PipelineOrchestrator")

# Define the pipeline steps as modules for robust execution
PIPELINE_STEPS = [
    {
        "name": "Dataset Analysis",
        "module": "src.data_analysis.dataset_analysis",
        "description": "Step 1: Running dataset analysis to rebuild cleaned and enriched dataset..."
    },
    {
        "name": "Habitability Model Training",
        "module": "src.ml_models.train_habitability_model",
        "description": "Step 2: Training habitability model..."
    },
    {
        "name": "Planet Discovery Engine",
        "module": "src.discovery.planet_discovery_engine",
        "description": "Step 3: Running discovery engine to rank habitable planet candidates..."
    },
    {
        "name": "Explainability Engine",
        "module": "src.ml_models.explainability_engine",
        "description": "Step 4: Computing explainability SHAP metrics..."
    },
    {
        "name": "Insight Engine",
        "module": "src.analytics.insight_engine",
        "description": "Step 5: Generating scientific insights and visual analytics..."
    },
    {
        "name": "Discovery Summary Generator",
        "module": "src.analytics.discovery_summary_generator",
        "description": "Step 6: Generating high-level discovery research summary report..."
    }
]

def main():
    start_time = time.time()
    timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    report_file_path = os.path.join(config.LOGS_DIR, f"execution_report_{timestamp_str}.txt")
    
    print("="*60)
    print(f"🚀 Starting ExoIntel Pipeline Orchestrator at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Run Health Check First
    if not run_health_check():
        print("\n❌ Pipeline aborted: System health check failed.")
        sys.exit(1)
        
    execution_details = []
    pipeline_success = True
    
    for i, step in enumerate(PIPELINE_STEPS, 1):
        step_name = step["name"]
        module_path = step["module"]
        description = step["description"]
        
        logger.info(f"Executing {step_name}...")
        print(f"\n{description}")
        
        step_start_time = time.time()
        
        try:
            # Execute the script as a module
            result = subprocess.run([sys.executable, "-m", module_path], check=True, capture_output=True, text=True)
            step_duration = time.time() - step_start_time
            
            logger.info(f"✅ {step_name} completed in {step_duration:.2f}s")
            print(f"✅ {step_name} completed successfully in {step_duration:.2f} seconds.")
            
            execution_details.append({
                "step": i,
                "name": step_name,
                "status": "SUCCESS",
                "duration": step_duration,
                "output": result.stdout
            })
            
        except subprocess.CalledProcessError as e:
            step_duration = time.time() - step_start_time
            logger.error(f"❌ {step_name} FAILED: {e.stderr}")
            print(f"❌ {step_name} FAILED after {step_duration:.2f} seconds.")
            print(f"Error Output:\n{e.stderr}")
            
            execution_details.append({
                "step": i,
                "name": step_name,
                "status": "FAILED",
                "duration": step_duration,
                "error": e.stderr,
                "output": e.stdout
            })
            
            pipeline_success = False
            break # Stop the pipeline if a step fails
        except Exception as e:
            step_duration = time.time() - step_start_time
            logger.exception(f"❌ {step_name} encountered an unexpected error.")
            print(f"❌ {step_name} FAILED due to unexpected error after {step_duration:.2f} seconds.")
            print(f"Exception: {str(e)}")
            
            execution_details.append({
                "step": i,
                "name": step_name,
                "status": "ERROR",
                "duration": step_duration,
                "error": str(e),
                "output": ""
            })
            
            pipeline_success = False
            break

    total_duration = time.time() - start_time
    status_str = "SUCCESS" if pipeline_success else "FAILED"
    
    print("\n" + "="*60)
    print(f"🛑 ExoIntel Pipeline Finished - Status: {status_str} - Total Time: {total_duration:.2f}s")
    print("="*60)
    
    # Write the report to a log file
    with open(report_file_path, "w", encoding="utf-8") as f:
        f.write("============================================================\n")
        f.write(f"ExoIntel Pipeline Execution Report\n")
        f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Status: {status_str}\n")
        f.write(f"Total Pipeline Duration: {total_duration:.2f} seconds\n")
        f.write("============================================================\n\n")
        
        f.write("Step Details:\n")
        f.write("-" * 30 + "\n")
        for detail in execution_details:
            f.write(f"Step {detail['step']}: {detail['name']}\n")
            f.write(f"Status: {detail['status']}\n")
            f.write(f"Duration: {detail['duration']:.2f} seconds\n")
            if detail['status'] != "SUCCESS":
                f.write(f"Error:\n{detail.get('error', '')}\n")
            f.write("-" * 30 + "\n")

    logger.info(f"Pipeline finished with status: {status_str}")
    print(f"\n📝 Detailed execution report saved to: {report_file_path}\n")

if __name__ == "__main__":
    main()
