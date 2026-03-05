import os
import sys
import time
import subprocess
import datetime
import traceback

def main():
    print("=" * 80)
    print("                 ExoIntel – Automated Pipeline Orchestrator")
    print("=" * 80)
    print("This orchestrator runs the complete ExoIntel AI analytics pipeline end-to-end:")
    print("  1. Dataset Intelligence & Feature Engineering")
    print("  2. Machine Learning Model Training")
    print("  3. Planet Discovery & Ranking Engine")
    print("  4. Explainable AI (SHAP) Engine")
    print("  5. Scientific Insight Engine\n")

    start_time = time.time()
    
    # Establish logging
    log_dir = "pipeline_logs"
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file_path = os.path.join(log_dir, f"pipeline_run_{timestamp}.log")
    
    def log_and_print(msg):
        print(msg)
        with open(log_file_path, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
            
    log_and_print(f"Pipeline started at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log_and_print("-" * 80)

    # Define the sequence of modules to run
    # Format: (Step Name, module_path)
    pipeline_steps = [
        ("Phase 2: Dataset Intelligence & Feature Engineering", "src.data_analysis.dataset_analysis"),
        ("Phase 1: Machine Learning Model Training", "src.ml_models.train_habitability_model"),
        ("Phase 3: Planet Discovery & Ranking Engine", "src.discovery.planet_discovery_engine"),
        ("Phase 5: Explainable AI (SHAP) Engine", "src.ml_models.explainability_engine"),
        ("Phase 6: Scientific Insight Engine", "src.analytics.insight_engine")
    ]

    has_error = False

    for i, (step_name, module_path) in enumerate(pipeline_steps, 1):
        step_start = time.time()
        log_and_print(f"\n[{i}/{len(pipeline_steps)}] {step_name}...")
        log_and_print(f"Executing module: {module_path}")
        
        try:
            # Run the module as a subprocess to keep environments isolated
            result = subprocess.run(
                [sys.executable, "-m", module_path],
                capture_output=True,
                text=True,
                check=True
            )
            step_duration = time.time() - step_start
            
            # Print output nicely
            output_lines = result.stdout.strip().split('\n')
            for line in output_lines:
                if line.strip():
                    log_and_print(f"  | {line}")
            
            log_and_print(f"[OK] Completed in {step_duration:.2f} seconds.")
            
        except subprocess.CalledProcessError as e:
            has_error = True
            step_duration = time.time() - step_start
            log_and_print(f"[ERROR] Step failed after {step_duration:.2f} seconds with exit code {e.returncode}.")
            log_and_print("\nStandard Output:")
            log_and_print(e.stdout)
            log_and_print("\nStandard Error:")
            log_and_print(e.stderr)
            break
        except Exception as e:
            has_error = True
            log_and_print(f"[ERROR] Unexpected exception: {str(e)}")
            log_and_print(traceback.format_exc())
            break

    total_duration = time.time() - start_time
    
    log_and_print("\n" + "=" * 80)
    if has_error:
        log_and_print(f"❌ Pipeline FAILED after {total_duration:.2f} seconds.")
    else:
        log_and_print(f"✅ Pipeline COMPLETED SUCCESSFULLY in {total_duration:.2f} seconds.")
    log_and_print("=" * 80)
    
    print(f"\nExecution summary log saved to: {log_file_path}")
    
    if has_error:
        sys.exit(1)

if __name__ == "__main__":
    main()
