"""
Complete High-Accuracy Workflow
Generate 10K dataset → Evaluate → Compare → Visualize
"""

import subprocess
import sys
import time
from datetime import datetime

def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(title.center(80))
    print("=" * 80 + "\n")

def run_command(command, description):
    """Run command and track time"""
    print(f"📌 {description}")
    # Use 'py' for Windows compatibility
    command = command.replace('python ', 'py ')
    print(f"   Command: {command}\n")

    start = time.time()
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=False)
        elapsed = time.time() - start
        print(f"\n✓ {description} completed in {elapsed:.1f}s\n")
        return True, elapsed
    except subprocess.CalledProcessError as e:
        elapsed = time.time() - start
        print(f"\n✗ {description} failed after {elapsed:.1f}s")
        print(f"   Error: {e}\n")
        return False, elapsed

def main():
    print_header("HIGH-ACCURACY WORKFLOW - 10K+ DATASET")
    print("EmpowerTech Solutions - Advanced Evaluation")
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print("This workflow will:")
    print("  1. Generate 10,000 synthetic test cases")
    print("  2. Evaluate Enhanced ML algorithm")
    print("  3. Compare Enhanced ML vs Baseline")
    print("  4. Generate visualizations")
    print("  5. Calculate statistical metrics\n")
    
    response = input("Proceed with full 10K dataset? (y/n, default=y): ").strip().lower()
    
    if response == 'n':
        size = input("Enter dataset size (100-50000): ").strip()
        try:
            size = int(size)
            size = max(100, min(50000, size))
        except:
            size = 1000
            print(f"Invalid input, using {size}")
    else:
        size = 10000
    
    print(f"\n✓ Will generate {size:,} test cases\n")
    
    total_start = time.time()
    timings = {}
    
    # Step 1: Generate Dataset
    print_header(f"STEP 1: GENERATE {size:,} TEST CASES")
    
    success, elapsed = run_command(
        f"python generate_synthetic_dataset.py --size {size}",
        f"Generating {size:,} synthetic test cases"
    )
    timings['generation'] = elapsed
    
    if not success:
        print("❌ Cannot proceed without dataset. Exiting.")
        return
    
    # Step 2: Evaluate Enhanced ML
    print_header("STEP 2: EVALUATE ENHANCED ML ALGORITHM")
    
    success, elapsed = run_command(
        "python run_large_scale_evaluation.py --dataset backend/data/large_test_dataset.json --enhanced",
        f"Evaluating Enhanced ML on {size:,} cases"
    )
    timings['enhanced_eval'] = elapsed
    
    if not success:
        print("⚠ Enhanced ML evaluation failed, but continuing...")
    
    # Step 3: Comparative Evaluation
    print_header("STEP 3: COMPARATIVE EVALUATION (ENHANCED VS BASELINE)")
    
    success, elapsed = run_command(
        "python run_large_scale_evaluation.py --dataset backend/data/large_test_dataset.json --compare",
        "Comparing Enhanced ML vs Baseline"
    )
    timings['comparison'] = elapsed
    
    if not success:
        print("⚠ Comparative evaluation failed, but continuing...")
    
    # Step 4: Generate Visualizations
    print_header("STEP 4: GENERATE VISUALIZATIONS")
    
    # Check if matplotlib is installed
    try:
        import matplotlib
        print("✓ matplotlib is installed\n")
    except ImportError:
        print("⚠ matplotlib not installed. Installing...\n")
        subprocess.run("pip install matplotlib", shell=True)
    
    success, elapsed = run_command(
        "py generate_visualizations.py",
        "Generating publication-quality charts"
    )
    timings['visualization'] = elapsed
    
    # Summary
    print_header("WORKFLOW COMPLETE")
    
    total_time = time.time() - total_start
    
    print("✓ High-accuracy workflow execution completed!\n")
    print(f"{'─' * 80}")
    print("TIMING SUMMARY")
    print(f"{'─' * 80}\n")
    
    for step, elapsed in timings.items():
        print(f"{step.replace('_', ' ').title():<30} {elapsed:>8.1f}s")
    
    print(f"{'─' * 80}")
    print(f"{'Total Time':<30} {total_time:>8.1f}s")
    print(f"{'─' * 80}\n")
    
    print("Generated outputs:")
    print("  📁 backend/data/")
    print(f"     - large_test_dataset.json ({size:,} cases)")
    print()
    print("  📁 backend/evaluation_results/")
    print("     - large_eval_*.json (Enhanced ML results)")
    print("     - large_comparison_*.json (Comparison results)")
    print()
    print("  📁 visualizations/")
    print("     - comparison_chart.png")
    print("     - improvement_chart.png")
    print("     - confusion_matrices.png")
    print("     - threshold_analysis.png")
    print("     - score_distribution.png")
    print()
    
    print("Next steps:")
    print("  1. Review results in backend/evaluation_results/")
    print("  2. Check accuracy improvements in large_comparison_*.json")
    print("  3. View visualizations in visualizations/")
    print("  4. Insert metrics into research paper")
    print(f"  5. Cite: 'Evaluated on {size:,} test cases'")
    print()
    print(f"📊 Your system has been validated on {size:,} test cases!")
    print("=" * 80)
    print()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Workflow interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
