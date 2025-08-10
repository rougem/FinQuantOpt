#!/usr/bin/env python3
"""
Standalone VQE Portfolio Optimization Monitor
Run this script to automatically monitor your quantum optimization progress.

Usage:
    python standalone_monitor.py
    
The script will auto-detect your data path and experiment, or you can modify
the configuration section below.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import pickle as pkl
from pathlib import Path
import time
import sys
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class VQEPortfolioMonitor:
    def __init__(self, data_path, experiment_id='test'):
        """
        Monitor VQE portfolio optimization in real-time
        
        Args:
            data_path: Path to the data directory
            experiment_id: The experiment ID to monitor
        """
        self.data_path = Path(data_path)
        self.experiment_id = experiment_id
        self.fig = None
        self.axes = None
        
    def setup_plots(self):
        """Setup the monitoring dashboard"""
        self.fig, self.axes = plt.subplots(2, 3, figsize=(18, 12))
        self.fig.suptitle(f'VQE Portfolio Optimization Monitor: {self.experiment_id}', fontsize=16)
        
        # Configure subplots
        titles = [
            'Objective Function Convergence',
            'Parameter Updates (θ)',
            'Solution Quality vs Classical',
            'Iteration Performance',
            'Parameter Distribution',
            'Constraint Violations'
        ]
        
        for i, ax in enumerate(self.axes.flat):
            ax.set_title(titles[i])
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return self.fig, self.axes
    
    def load_iteration_data(self, iter_num):
        """Load data from a specific iteration pickle file"""
        iter_file = self.data_path / f'1/31bonds/{self.experiment_id}_{iter_num}.pkl'
        if iter_file.exists():
            try:
                with open(iter_file, 'rb') as f:
                    return pkl.load(f)
            except Exception as e:
                print(f"Error loading iteration data: {e}")
                return None
        return None
    
    def load_experiment_data(self):
        """Load the main experiment results"""
        # Try different possible locations for the experiment file
        possible_paths = [
            self.data_path / f'1/31bonds/{self.experiment_id}/exp0.pkl',
            self.data_path / f'31bonds/{self.experiment_id}/exp0.pkl',
            self.data_path / f'{self.experiment_id}/exp0.pkl',
        ]
        
        for exp_file in possible_paths:
            if exp_file.exists():
                try:
                    print(f"📂 Loading data from: {exp_file}")
                    with open(exp_file, 'rb') as f:
                        data = pkl.load(f)
                    
                    # Debug: Check what we actually loaded
                    if data is None:
                        print("⚠️  Loaded data is None - file might be incomplete")
                        continue
                    elif isinstance(data, dict):
                        print(f"✅ Loaded dictionary with {len(data)} keys")
                        if len(data) == 0:
                            print("⚠️  Dictionary is empty - experiment might still be running")
                            continue
                        return data
                    else:
                        print(f"⚠️  Loaded data type: {type(data)} - expected dictionary")
                        continue
                        
                except Exception as e:
                    print(f"❌ Error loading from {exp_file}: {e}")
                    continue
        
        # If no files found, show what we're looking for
        print("🔍 No valid experiment data found. Searched in:")
        for path in possible_paths:
            status = "EXISTS" if path.exists() else "NOT FOUND"
            print(f"   - {path} ({status})")
        return None
    
    def plot_convergence(self, exp_data):
        """Plot objective function convergence"""
        ax = self.axes[0, 0]
        ax.clear()
        ax.set_title('Objective Function Convergence')
        
        if exp_data and 'step3_monitor_iter_best_fx' in exp_data:
            best_fx = exp_data['step3_monitor_iter_best_fx']
            
            # Debug: Check if best_fx is None or empty
            if best_fx is None:
                ax.text(0.5, 0.5, 'No convergence data yet\n(best_fx is None)', 
                       transform=ax.transAxes, ha='center', va='center')
                return
            elif len(best_fx) == 0:
                ax.text(0.5, 0.5, 'No convergence data yet\n(best_fx is empty)', 
                       transform=ax.transAxes, ha='center', va='center')
                return
            
            iterations = range(len(best_fx))
            
            ax.plot(iterations, best_fx, 'b-', linewidth=2, label='Best Objective')
            
            refvalue = exp_data.get('refvalue')
            if refvalue is not None:
                ax.axhline(y=refvalue, color='r', linestyle='--', 
                          label=f'Classical Solution: {refvalue:.4f}')
            
            ax.set_xlabel('Iteration')
            ax.set_ylabel('Objective Value')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # Add improvement indicators
            if len(best_fx) > 1:
                improvements = [i for i in range(1, len(best_fx)) if best_fx[i] < best_fx[i-1]]
                if improvements:
                    ax.scatter([improvements], [best_fx[i] for i in improvements], 
                             color='green', s=50, zorder=5, label='Improvements')
        else:
            ax.text(0.5, 0.5, 'Waiting for convergence data...\nstep3_monitor_iter_best_fx not found', 
                   transform=ax.transAxes, ha='center', va='center')
    
    def plot_parameter_updates(self, exp_data):
        """Plot parameter update magnitudes"""
        ax = self.axes[0, 1]
        ax.clear()
        ax.set_title('Parameter Updates (θ)')
        
        if exp_data and 'step3_monitor_iter_thetas' in exp_data:
            thetas = exp_data['step3_monitor_iter_thetas']
            
            # Debug: Check if thetas is None or empty
            if thetas is None:
                ax.text(0.5, 0.5, 'No parameter data yet\n(thetas is None)', 
                       transform=ax.transAxes, ha='center', va='center')
                return
            elif len(thetas) <= 1:
                ax.text(0.5, 0.5, 'Need more iterations\nfor parameter tracking', 
                       transform=ax.transAxes, ha='center', va='center')
                return
            
            # Calculate parameter changes between iterations
            param_changes = []
            for i in range(1, len(thetas)):
                if thetas[i] is not None and thetas[i-1] is not None:
                    change = np.linalg.norm(np.array(thetas[i]) - np.array(thetas[i-1]))
                    param_changes.append(change)
            
            if param_changes:
                iterations = range(1, len(param_changes) + 1)
                ax.plot(iterations, param_changes, 'g-', linewidth=2, label='Parameter Change Magnitude')
                ax.set_xlabel('Iteration')
                ax.set_ylabel('||Δθ||')
                ax.legend()
                ax.set_yscale('log')
            else:
                ax.text(0.5, 0.5, 'No valid parameter changes found', 
                       transform=ax.transAxes, ha='center', va='center')
        else:
            ax.text(0.5, 0.5, 'Waiting for parameter data...\nstep3_monitor_iter_thetas not found', 
                   transform=ax.transAxes, ha='center', va='center')
    
    def plot_solution_quality(self, exp_data):
        """Plot solution quality metrics"""
        ax = self.axes[0, 2]
        ax.clear()
        ax.set_title('Solution Quality vs Classical')
        
        if exp_data:
            classical_val = exp_data.get('refvalue', 0)
            quantum_val = exp_data.get('step3_result_best_fx', 0)
            
            if classical_val != 0:
                rel_gap = (quantum_val - classical_val) / abs(classical_val) * 100
                
                categories = ['Classical\nSolution', 'Quantum\nSolution']
                values = [classical_val, quantum_val]
                colors = ['red', 'blue']
                
                bars = ax.bar(categories, values, color=colors, alpha=0.7)
                ax.set_ylabel('Objective Value')
                
                # Add value labels on bars
                for bar, val in zip(bars, values):
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{val:.4f}', ha='center', va='bottom')
                
                # Add gap information
                ax.text(0.5, 0.95, f'Relative Gap: {rel_gap:.2f}%', 
                       transform=ax.transAxes, ha='center', va='top',
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    def plot_iteration_performance(self, exp_data):
        """Plot iteration-wise performance metrics"""
        ax = self.axes[1, 0]
        ax.clear()
        ax.set_title('Iteration Performance')
        
        if exp_data and 'step3_iter_fx_evals' in exp_data:
            fx_evals = exp_data['step3_iter_fx_evals']
            iterations = range(len(fx_evals))
            
            ax.bar(iterations, fx_evals, alpha=0.7, color='orange', label='Function Evaluations')
            ax.set_xlabel('Iteration')
            ax.set_ylabel('Function Evaluations')
            ax.legend()
    
    def plot_parameter_distribution(self, exp_data):
        """Plot current parameter distribution"""
        ax = self.axes[1, 1]
        ax.clear()
        ax.set_title('Parameter Distribution')
        
        if exp_data and 'step3_monitor_iter_thetas' in exp_data:
            thetas = exp_data['step3_monitor_iter_thetas']
            
            if thetas is None or len(thetas) == 0:
                ax.text(0.5, 0.5, 'No parameter data available', 
                       transform=ax.transAxes, ha='center', va='center')
                return
            
            current_theta = thetas[-1]
            if current_theta is None:
                ax.text(0.5, 0.5, 'Latest parameters are None', 
                       transform=ax.transAxes, ha='center', va='center')
                return
            
            ax.hist(current_theta, bins=20, alpha=0.7, color='purple', edgecolor='black')
            ax.set_xlabel('Parameter Value')
            ax.set_ylabel('Frequency')
            ax.axvline(np.mean(current_theta), color='red', linestyle='--', 
                      label=f'Mean: {np.mean(current_theta):.3f}')
            ax.legend()
        else:
            ax.text(0.5, 0.5, 'Waiting for parameter data...', 
                   transform=ax.transAxes, ha='center', va='center')
    
    def plot_constraint_info(self, exp_data):
        """Plot constraint-related information"""
        ax = self.axes[1, 2]
        ax.clear()
        ax.set_title('Optimization Info')
        
        if exp_data:
            runtime = exp_data.get('step3_time', 0)
            if runtime:
                runtime_str = f"{runtime:.2f}s"
            else:
                runtime_str = "Running..."
                
            info_text = f"""
Experiment: {exp_data.get('experiment_id', 'N/A')}
Ansatz: {exp_data.get('ansatz', 'N/A')}
Device: {exp_data.get('device', 'N/A')}
Alpha (CVaR): {exp_data.get('alpha', 'N/A')}
Shots: {exp_data.get('shots', 'N/A')}
Runtime: {runtime_str}
Status: {exp_data.get('step3_result_message', 'Running...')}
Function Evals: {exp_data.get('step3_fx_evals', 'N/A')}
            """
            
            ax.text(0.05, 0.95, info_text, transform=ax.transAxes, 
                   verticalalignment='top', fontfamily='monospace',
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
    
    def debug_data(self, exp_data):
        """Debug function to see what's in the experiment data"""
        print("🔍 DEBUG: Examining experiment data...")
        print(f"Data type: {type(exp_data)}")
        
        if isinstance(exp_data, dict):
            print(f"Dictionary keys ({len(exp_data)}):")
            for key in sorted(exp_data.keys()):
                value = exp_data[key]
                if value is None:
                    print(f"  {key}: None")
                elif isinstance(value, list):
                    print(f"  {key}: list with {len(value)} items")
                    if len(value) > 0 and value[0] is None:
                        print(f"    - First item is None")
                else:
                    print(f"  {key}: {type(value)} = {value}")
        print("🔍 DEBUG: End of data examination")
    
    def update_plots(self):
        """Update all plots with current data"""
        exp_data = self.load_experiment_data()
        
        if exp_data:
            # Add debug info
            self.debug_data(exp_data)
            
            try:
                self.plot_convergence(exp_data)
            except Exception as e:
                print(f"❌ Error in plot_convergence: {e}")
                
            try:
                self.plot_parameter_updates(exp_data)
            except Exception as e:
                print(f"❌ Error in plot_parameter_updates: {e}")
                
            try:
                self.plot_solution_quality(exp_data)
            except Exception as e:
                print(f"❌ Error in plot_solution_quality: {e}")
                
            try:
                self.plot_iteration_performance(exp_data)
            except Exception as e:
                print(f"❌ Error in plot_iteration_performance: {e}")
                
            try:
                self.plot_parameter_distribution(exp_data)
            except Exception as e:
                print(f"❌ Error in plot_parameter_distribution: {e}")
                
            try:
                self.plot_constraint_info(exp_data)
            except Exception as e:
                print(f"❌ Error in plot_constraint_info: {e}")
        else:
            # Show waiting message if no data yet
            self.axes[1, 2].clear()
            self.axes[1, 2].text(0.5, 0.5, 'Waiting for experiment data...\nMake sure VQE is running!', 
                               transform=self.axes[1, 2].transAxes, ha='center', va='center',
                               fontsize=14, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
            self.axes[1, 2].set_xlim(0, 1)
            self.axes[1, 2].set_ylim(0, 1)
            self.axes[1, 2].axis('off')
        
        plt.tight_layout()
        plt.draw()
    
    def monitor_realtime(self, update_interval=5, max_updates=100):
        """
        Monitor the optimization in real-time
        
        Args:
            update_interval: Seconds between updates
            max_updates: Maximum number of updates before stopping
        """
        self.setup_plots()
        plt.ion()  # Turn on interactive mode
        
        print(f"🚀 VQE Portfolio Optimization Monitor Started")
        print(f"📁 Data path: {self.data_path}")
        print(f"🔬 Experiment ID: {self.experiment_id}")
        print(f"⏱️  Update interval: {update_interval} seconds")
        print("❌ Close the plot window to stop monitoring.")
        print("="*60)
        
        update_count = 0
        
        try:
            while update_count < max_updates:
                self.update_plots()
                plt.pause(update_interval)
                update_count += 1
                
                # Check if window is still open
                if not plt.get_fignums():
                    break
                    
                timestamp = datetime.now().strftime('%H:%M:%S')
                print(f"📊 Update {update_count:3d}/{max_updates} - {timestamp}")
                
        except KeyboardInterrupt:
            print("\n⛔ Monitoring stopped by user (Ctrl+C).")
        
        plt.ioff()  # Turn off interactive mode
        plt.show()
    
    def generate_final_report(self, save_path=None):
        """Generate a final analysis report"""
        exp_data = self.load_experiment_data()
        
        if not exp_data:
            print("❌ No valid experiment data found!")
            return
        
        # Check if experiment is still running (empty or incomplete data)
        if isinstance(exp_data, dict) and len(exp_data) == 0:
            print("⏳ Experiment file exists but is empty - optimization might still be running.")
            print("Try running real-time monitoring instead.")
            return
        
        # Update plots one final time
        try:
            self.update_plots()
        except Exception as e:
            print(f"❌ Error updating plots: {e}")
            print("This might happen if the experiment is still running.")
            return
        
        # Print summary
        print("\n" + "="*60)
        print("📈 VQE Portfolio Optimization Final Report")
        print("="*60)
        print(f"🔬 Experiment ID: {exp_data.get('experiment_id', 'N/A')}")
        print(f"🎯 Classical Solution: {exp_data.get('refvalue', 'N/A')}")
        print(f"⚛️  Quantum Solution: {exp_data.get('step3_result_best_fx', 'N/A')}")
        
        if exp_data.get('refvalue') and exp_data.get('step3_result_best_fx'):
            gap = (exp_data['step3_result_best_fx'] - exp_data['refvalue']) / abs(exp_data['refvalue']) * 100
            if gap < 0:
                print(f"✅ Relative Gap: {gap:.2f}% (Quantum BETTER!)")
            else:
                print(f"📊 Relative Gap: {gap:.2f}%")
        
        runtime = exp_data.get('step3_time', 0)
        if runtime:
            print(f"⏱️  Runtime: {runtime:.2f} seconds")
        else:
            print("⏱️  Runtime: Still running...")
            
        print(f"🔄 Function Evaluations: {exp_data.get('step3_fx_evals', 'N/A')}")
        print(f"✅ Optimization Status: {exp_data.get('step3_result_message', 'N/A')}")
        print("="*60)
        
        if save_path:
            try:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                print(f"💾 Report saved to: {save_path}")
            except Exception as e:
                print(f"⚠️  Could not save report: {e}")


def auto_detect_paths():
    """Try to automatically detect the data path and current experiment"""
    # Try to find the project root
    current_dir = Path.cwd()
    possible_roots = [current_dir, current_dir.parent, current_dir / 'WISER_Optimization_VG']
    
    data_path = None
    for root in possible_roots:
        test_data_path = root / 'data'
        if test_data_path.exists():
            data_path = test_data_path
            break
    
    if not data_path:
        # Fallback - ask user or use default
        print("⚠️  Could not auto-detect data path. Using current directory.")
        data_path = current_dir / 'data'
    
    return str(data_path)


def main():
    """Main execution function"""
    print("🎯 VQE Portfolio Optimization Standalone Monitor")
    print("="*60)
    
    # CONFIGURATION SECTION - MODIFY THESE IF NEEDED
    # ================================================
    
    # Option 1: Auto-detect (recommended)
    DATA_PATH = auto_detect_paths()
    EXPERIMENT_ID = 'test'  # Change this to match your experiment
    
    # Option 2: Manual configuration (uncomment and modify if auto-detect fails)
    # DATA_PATH = "C:/path/to/WISER_Optimization_VG/data"
    # EXPERIMENT_ID = 'test'
    
    # Monitoring settings
    UPDATE_INTERVAL = 10  # seconds between updates
    MAX_UPDATES = 100     # maximum updates before auto-stop
    
    # ================================================
    
    print(f"📁 Using data path: {DATA_PATH}")
    print(f"🔬 Monitoring experiment: {EXPERIMENT_ID}")
    
    # Verify data path exists
    if not Path(DATA_PATH).exists():
        print(f"❌ Data path does not exist: {DATA_PATH}")
        print("Please check the configuration section and update DATA_PATH")
        return
    
    # Create monitor
    monitor = VQEPortfolioMonitor(DATA_PATH, experiment_id=EXPERIMENT_ID)
    
    # Check if we should do real-time monitoring or final report
    possible_exp_files = [
        Path(DATA_PATH) / f'1/31bonds/{EXPERIMENT_ID}/exp0.pkl',
        Path(DATA_PATH) / f'31bonds/{EXPERIMENT_ID}/exp0.pkl', 
        Path(DATA_PATH) / f'{EXPERIMENT_ID}/exp0.pkl',
    ]
    
    exp_file_found = None
    for exp_file in possible_exp_files:
        if exp_file.exists():
            exp_file_found = exp_file
            break
    
    if exp_file_found:
        print(f"📊 Experiment data found at: {exp_file_found}")
        print("Generating final report...")
        monitor.generate_final_report(save_path="vqe_portfolio_report.png")
        
        user_input = input("\nWould you like to start real-time monitoring anyway? (y/n): ")
        if user_input.lower().startswith('y'):
            monitor.monitor_realtime(update_interval=UPDATE_INTERVAL, max_updates=MAX_UPDATES)
    else:
        print("⏳ No experiment data found yet. Searched in:")
        for path in possible_exp_files:
            print(f"   - {path}")
        print("\nStarting real-time monitoring...")
        print("Make sure your VQE optimization is running in another terminal!")
        time.sleep(2)  # Give user time to read
        monitor.monitor_realtime(update_interval=UPDATE_INTERVAL, max_updates=MAX_UPDATES)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please check the configuration section and ensure your paths are correct.")
        input("Press Enter to exit...")
