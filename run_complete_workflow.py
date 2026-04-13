"""
Complete Research Workflow
Run all evaluations and generate publication-ready results
"""

import sys
import os
import subprocess
from datetime import datetime

def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(title.center(80))
    print("=" * 80 + "\n")

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"📌 {description}")
    # Use 'py' for Windows compatibility
    command = command.replace('python ', 'py ')
    print(f"   Command: {command}")
    print()

    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=False, text=True)
        print(f"✓ {description} completed successfully\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed")
        print(f"   Error: {e}\n")
        return False

def main():
    """Run complete research workflow"""
    
    print_header("COMPLETE RESEARCH WORKFLOW")
    print("EmpowerTech Solutions - AI Resume Screening System")
    print(f"Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    print("This script will run:")
    print("  1. Basic evaluation test")
    print("  2. Comparative evaluation (ML vs Baseline)")
    print("  3. Cross-validation (5-fold)")
    print("  4. Visualization generation")
    print()
    
    input("Press Enter to continue...")
    
    # Step 1: Basic Evaluation
    print_header("STEP 1: BASIC EVALUATION TEST")
    success = run_command(
        "python run_evaluation.py",
        "Running basic evaluation across multiple thresholds"
    )
    
    if not success:
        print("⚠ Warning: Basic evaluation failed. Continuing anyway...")
    
    # Step 2: Comparative Evaluation
    print_header("STEP 2: COMPARATIVE EVALUATION")
    success = run_command(
        "python run_comparative_evaluation.py",
        "Comparing ML-based vs Baseline algorithms"
    )
    
    if not success:
        print("❌ Comparative evaluation failed. Stopping workflow.")
        return
    
    # Step 3: Cross-Validation
    print_header("STEP 3: CROSS-VALIDATION")
    success = run_command(
        "python run_cross_validation.py --k 5 --threshold 0.5",
        "Running 5-fold cross-validation"
    )
    
    if not success:
        print("⚠ Warning: Cross-validation failed. Continuing anyway...")
    
    # Step 4: Generate Visualizations
    print_header("STEP 4: GENERATE VISUALIZATIONS")
    
    # Check if matplotlib is installed
    try:
        import matplotlib
        matplotlib_installed = True
    except ImportError:
        matplotlib_installed = False
    
    if not matplotlib_installed:
        print("⚠ Matplotlib not installed. Installing...")
        run_command("pip install matplotlib", "Installing matplotlib")
    
    success = run_command(
        "python generate_visualizations.py",
        "Generating charts and graphs for research paper"
    )
    
    if not success:
        print("⚠ Warning: Visualization generation failed.")
    
    # Summary
    print_header("WORKFLOW COMPLETE")
    
    print("✓ Research workflow execution completed!")
    print()
    print("Generated outputs:")
    print("  📁 backend/evaluation_results/")
    print("     - threshold_*.json (Multiple threshold results)")
    print("     - comparison_*.json (ML vs Baseline comparison)")
    print("     - cross_validation_*.json (Cross-validation results)")
    print()
    print("  📁 visualizations/")
    print("     - comparison_chart.png")
    print("     - improvement_chart.png")
    print("     - confusion_matrices.png")
    print("     - threshold_analysis.png")
    print("     - score_distribution.png")
    print()
    print("Next steps:")
    print("  1. Review all results in backend/evaluation_results/")
    print("  2. Check generated visualizations in visualizations/")
    print("  3. Open docs/RESEARCH_PAPER_TEMPLATE.md")
    print("  4. Insert your metrics and results")
    print("  5. Add the generated charts to your paper")
    print()
    print("📄 Your research is now publication-ready!")
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
