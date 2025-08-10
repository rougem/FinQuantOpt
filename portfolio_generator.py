#!/usr/bin/env python3
"""
Portfolio Optimization Problem Generator for Vanguard Challenge

This module creates realistic portfolio optimization problems in GUROBI format
that can be solved by the VQE quantum optimization framework.

Focus areas:
1. Asset allocation with risk constraints
2. Sector diversification limits  
3. ESG/sustainability constraints
4. Transaction cost minimization
5. Index tracking problems
"""

import numpy as np
import pandas as pd
import gurobipy as gp
from gurobipy import GRB
from pathlib import Path
import random
from datetime import datetime, timedelta

class PortfolioGenerator:
    """Generate realistic portfolio optimization problems for VQE testing"""
    
    def __init__(self, random_seed=42):
        """Initialize with reproducible random seed"""
        np.random.seed(random_seed)
        random.seed(random_seed)
        
    def generate_realistic_returns(self, n_assets, market_regime='normal'):
        """Generate realistic expected returns based on market regime"""
        
        if market_regime == 'bull':
            # Bull market: higher returns, lower volatility
            base_returns = np.random.normal(0.12, 0.05, n_assets)  # 12% average
            volatilities = np.random.uniform(0.15, 0.25, n_assets)  # 15-25% vol
            
        elif market_regime == 'bear':
            # Bear market: lower/negative returns, higher volatility  
            base_returns = np.random.normal(-0.05, 0.08, n_assets)  # -5% average
            volatilities = np.random.uniform(0.25, 0.40, n_assets)  # 25-40% vol
            
        elif market_regime == 'crisis':
            # Crisis: very negative returns, extreme volatility
            base_returns = np.random.normal(-0.20, 0.15, n_assets)  # -20% average
            volatilities = np.random.uniform(0.40, 0.80, n_assets)  # 40-80% vol
            
        else:  # normal market
            base_returns = np.random.normal(0.08, 0.06, n_assets)   # 8% average
            volatilities = np.random.uniform(0.18, 0.30, n_assets)  # 18-30% vol
            
        return base_returns, volatilities
    
    def generate_sector_structure(self, n_assets):
        """Create realistic sector allocation"""
        
        # Define major sectors with typical market caps
        sectors = {
            'Technology': 0.25,      # 25% of market
            'Healthcare': 0.15,      # 15% of market  
            'Financials': 0.12,      # 12% of market
            'Consumer': 0.12,        # 12% of market
            'Industrials': 0.10,     # 10% of market
            'Energy': 0.08,          # 8% of market
            'Materials': 0.06,       # 6% of market
            'Utilities': 0.05,       # 5% of market
            'Real Estate': 0.04,     # 4% of market
            'Telecom': 0.03,         # 3% of market
        }
        
        # Assign assets to sectors based on market cap weights
        sector_assignments = []
        sector_names = list(sectors.keys())
        sector_weights = list(sectors.values())
        
        for i in range(n_assets):
            sector = np.random.choice(sector_names, p=sector_weights)
            sector_assignments.append(sector)
            
        return sector_assignments, sectors
    
    def generate_covariance_matrix(self, returns, volatilities, sector_assignments):
        """Generate realistic covariance matrix with sector correlations"""
        
        n_assets = len(returns)
        
        # Base correlation matrix
        correlation_matrix = np.eye(n_assets)
        
        # Add sector correlations (assets in same sector are more correlated)
        for i in range(n_assets):
            for j in range(i+1, n_assets):
                if sector_assignments[i] == sector_assignments[j]:
                    # Same sector: higher correlation (0.3-0.7)
                    corr = np.random.uniform(0.3, 0.7)
                else:
                    # Different sectors: lower correlation (0.0-0.3)
                    corr = np.random.uniform(0.0, 0.3)
                
                correlation_matrix[i, j] = corr
                correlation_matrix[j, i] = corr
        
        # Convert to covariance matrix
        vol_matrix = np.outer(volatilities, volatilities)
        covariance_matrix = correlation_matrix * vol_matrix
        
        # Ensure positive semi-definite
        eigenvals, eigenvecs = np.linalg.eigh(covariance_matrix)
        eigenvals = np.maximum(eigenvals, 0.0001)  # Regularize small eigenvalues
        covariance_matrix = eigenvecs @ np.diag(eigenvals) @ eigenvecs.T
        
        return covariance_matrix
    
    def create_mean_variance_problem(self, n_assets=31, risk_aversion=1.0, 
                                   market_regime='normal', max_sector_weight=0.3):
        """
        Create mean-variance portfolio optimization problem
        
        minimize: λ * w^T Σ w - μ^T w  (risk - return tradeoff)
        subject to: 
        - sum(w) = 1 (budget constraint)
        - sector weights <= max_sector_weight
        - w >= 0 (long-only)
        """
        
        # Generate market data
        expected_returns, volatilities = self.generate_realistic_returns(n_assets, market_regime)
        sector_assignments, sector_info = self.generate_sector_structure(n_assets)
        covariance_matrix = self.generate_covariance_matrix(expected_returns, volatilities, sector_assignments)
        
        # Create GUROBI model
        model = gp.Model(f"mean_variance_{n_assets}assets_{market_regime}")
        model.setParam('OutputFlag', 0)  # Silent mode
        
        # Decision variables: portfolio weights
        weights = model.addVars(n_assets, name="w", lb=0.0, ub=1.0)
        
        # Objective: minimize risk - return tradeoff
        portfolio_variance = gp.quicksum(
            weights[i] * weights[j] * covariance_matrix[i, j] 
            for i in range(n_assets) for j in range(n_assets)
        )
        
        portfolio_return = gp.quicksum(
            expected_returns[i] * weights[i] for i in range(n_assets)
        )
        
        # Set objective: λ * risk - return (minimize risk, maximize return)
        model.setObjective(risk_aversion * portfolio_variance - portfolio_return, GRB.MINIMIZE)
        
        # Budget constraint: weights sum to 1
        model.addConstr(gp.quicksum(weights[i] for i in range(n_assets)) == 1.0, "budget")
        
        # Sector constraints: max allocation per sector
        unique_sectors = list(set(sector_assignments))
        for sector in unique_sectors:
            sector_assets = [i for i, s in enumerate(sector_assignments) if s == sector]
            if len(sector_assets) > 1:  # Only add constraint if sector has multiple assets
                sector_weight = gp.quicksum(weights[i] for i in sector_assets)
                model.addConstr(sector_weight <= max_sector_weight, f"sector_{sector}")
        
        return model, {
            'expected_returns': expected_returns,
            'covariance_matrix': covariance_matrix, 
            'sector_assignments': sector_assignments,
            'market_regime': market_regime
        }
    
    def create_risk_parity_problem(self, n_assets=31, market_regime='normal'):
        """
        Create risk parity optimization problem
        
        Goal: Each asset contributes equally to portfolio risk
        This is more complex for quantum optimization but very realistic
        """
        
        # Generate market data  
        expected_returns, volatilities = self.generate_realistic_returns(n_assets, market_regime)
        sector_assignments, sector_info = self.generate_sector_structure(n_assets)
        covariance_matrix = self.generate_covariance_matrix(expected_returns, volatilities, sector_assignments)
        
        # Create GUROBI model
        model = gp.Model(f"risk_parity_{n_assets}assets_{market_regime}")
        model.setParam('OutputFlag', 0)
        
        # Decision variables
        weights = model.addVars(n_assets, name="w", lb=0.0, ub=1.0)
        
        # For simplicity, use naive risk parity: equal weights
        # In practice, this would be more complex
        target_weight = 1.0 / n_assets
        
        # Minimize deviations from equal weights  
        deviations = model.addVars(n_assets, name="dev", lb=0.0)
        
        for i in range(n_assets):
            model.addConstr(deviations[i] >= weights[i] - target_weight)
            model.addConstr(deviations[i] >= target_weight - weights[i])
        
        model.setObjective(gp.quicksum(deviations), GRB.MINIMIZE)
        
        # Budget constraint
        model.addConstr(gp.quicksum(weights) == 1.0, "budget")
        
        return model, {
            'expected_returns': expected_returns,
            'covariance_matrix': covariance_matrix,
            'sector_assignments': sector_assignments,
            'target_weight': target_weight
        }
    
    def create_index_tracking_problem(self, n_assets=31, tracking_error_limit=0.02):
        """
        Create index tracking problem
        
        minimize: tracking error vs benchmark
        subject to: various practical constraints
        """
        
        # Generate market data
        expected_returns, volatilities = self.generate_realistic_returns(n_assets, 'normal')
        sector_assignments, sector_info = self.generate_sector_structure(n_assets)
        covariance_matrix = self.generate_covariance_matrix(expected_returns, volatilities, sector_assignments)
        
        # Create benchmark (market cap weighted)
        market_caps = np.random.lognormal(10, 1, n_assets)  # Realistic market cap distribution
        benchmark_weights = market_caps / np.sum(market_caps)
        
        # Create GUROBI model
        model = gp.Model(f"index_tracking_{n_assets}assets")
        model.setParam('OutputFlag', 0)
        
        # Decision variables
        weights = model.addVars(n_assets, name="w", lb=0.0, ub=1.0)
        
        # Minimize tracking error (simplified as sum of squared deviations)
        tracking_error = gp.quicksum(
            (weights[i] - benchmark_weights[i]) ** 2 for i in range(n_assets)
        )
        
        model.setObjective(tracking_error, GRB.MINIMIZE)
        
        # Budget constraint
        model.addConstr(gp.quicksum(weights) == 1.0, "budget")
        
        # Individual position limits (can't deviate too much from benchmark)
        for i in range(n_assets):
            model.addConstr(weights[i] <= benchmark_weights[i] + 0.05, f"max_dev_{i}")
            model.addConstr(weights[i] >= max(0, benchmark_weights[i] - 0.05), f"min_dev_{i}")
        
        return model, {
            'benchmark_weights': benchmark_weights,
            'expected_returns': expected_returns,
            'covariance_matrix': covariance_matrix,
            'sector_assignments': sector_assignments
        }
    
    def create_esg_constrained_problem(self, n_assets=31, min_esg_score=7.0, max_carbon=100):
        """
        Create ESG-constrained portfolio optimization
        
        Modern portfolio theory + ESG constraints
        Very relevant for current institutional investing
        """
        
        # Generate market data
        expected_returns, volatilities = self.generate_realistic_returns(n_assets, 'normal')
        sector_assignments, sector_info = self.generate_sector_structure(n_assets)
        covariance_matrix = self.generate_covariance_matrix(expected_returns, volatilities, sector_assignments)
        
        # Generate ESG scores (0-10 scale)
        esg_scores = np.random.uniform(3, 10, n_assets)
        
        # Generate carbon intensity (higher for energy/materials)
        carbon_intensity = np.zeros(n_assets)
        for i, sector in enumerate(sector_assignments):
            if sector in ['Energy', 'Materials', 'Industrials']:
                carbon_intensity[i] = np.random.uniform(50, 200)  # High carbon
            elif sector in ['Technology', 'Healthcare', 'Financials']:
                carbon_intensity[i] = np.random.uniform(5, 30)    # Low carbon
            else:
                carbon_intensity[i] = np.random.uniform(20, 80)   # Medium carbon
        
        # Create GUROBI model
        model = gp.Model(f"esg_constrained_{n_assets}assets")
        model.setParam('OutputFlag', 0)
        
        # Decision variables
        weights = model.addVars(n_assets, name="w", lb=0.0, ub=1.0)
        
        # Objective: minimize risk (simplified)
        portfolio_variance = gp.quicksum(
            weights[i] * weights[j] * covariance_matrix[i, j]
            for i in range(n_assets) for j in range(n_assets)
        )
        
        model.setObjective(portfolio_variance, GRB.MINIMIZE)
        
        # Budget constraint
        model.addConstr(gp.quicksum(weights) == 1.0, "budget")
        
        # ESG constraint: portfolio ESG score >= threshold
        portfolio_esg = gp.quicksum(esg_scores[i] * weights[i] for i in range(n_assets))
        model.addConstr(portfolio_esg >= min_esg_score, "min_esg")
        
        # Carbon constraint: portfolio carbon intensity <= limit
        portfolio_carbon = gp.quicksum(carbon_intensity[i] * weights[i] for i in range(n_assets))
        model.addConstr(portfolio_carbon <= max_carbon, "max_carbon")
        
        return model, {
            'expected_returns': expected_returns,
            'covariance_matrix': covariance_matrix,
            'sector_assignments': sector_assignments,
            'esg_scores': esg_scores,
            'carbon_intensity': carbon_intensity
        }

def create_vanguard_test_suite(output_dir="vanguard_problems"):
    """
    Create a comprehensive test suite for the Vanguard challenge
    
    This generates multiple realistic portfolio problems that demonstrate:
    1. Different problem types (mean-variance, risk parity, tracking, ESG)
    2. Different sizes (31, 109, 155 assets) 
    3. Different market conditions (bull, bear, normal, crisis)
    4. Increasing constraint complexity
    """
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    generator = PortfolioGenerator()
    problems_created = []
    
    print("🏗️  Creating Vanguard Portfolio Optimization Test Suite...")
    print("="*60)
    
    # Problem configurations for comprehensive testing
    configurations = [
        {'type': 'mean_variance', 'n_assets': 31, 'market': 'normal', 'risk_aversion': 1.0},
        {'type': 'mean_variance', 'n_assets': 31, 'market': 'bull', 'risk_aversion': 0.5},
        {'type': 'mean_variance', 'n_assets': 31, 'market': 'bear', 'risk_aversion': 2.0},
        {'type': 'index_tracking', 'n_assets': 31, 'tracking_error': 0.02},
        {'type': 'esg_constrained', 'n_assets': 31, 'min_esg': 7.0, 'max_carbon': 80},
        {'type': 'mean_variance', 'n_assets': 109, 'market': 'normal', 'risk_aversion': 1.0},
        {'type': 'index_tracking', 'n_assets': 109, 'tracking_error': 0.015},
        {'type': 'mean_variance', 'n_assets': 155, 'market': 'normal', 'risk_aversion': 1.0},
    ]
    
    import re
    
    for i, config in enumerate(configurations):
        print(f"\n📊 Creating Problem {i+1}/{len(configurations)}: {config['type']} ({config['n_assets']} assets)")
        
        try:
            if config['type'] == 'mean_variance':
                model, metadata = generator.create_mean_variance_problem(
                    n_assets=config['n_assets'],
                    risk_aversion=config['risk_aversion'],
                    market_regime=config['market']
                )
                problem_name = f"mean_variance_{config['n_assets']}assets_{config['market']}_risk{config['risk_aversion']}"
                
            elif config['type'] == 'index_tracking':
                model, metadata = generator.create_index_tracking_problem(
                    n_assets=config['n_assets'],
                    tracking_error_limit=config['tracking_error']
                )
                problem_name = f"index_tracking_{config['n_assets']}assets_te{config['tracking_error']}"
                
            elif config['type'] == 'esg_constrained':
                model, metadata = generator.create_esg_constrained_problem(
                    n_assets=config['n_assets'],
                    min_esg_score=config['min_esg'],
                    max_carbon=config['max_carbon']
                )
                problem_name = f"esg_constrained_{config['n_assets']}assets_esg{config['min_esg']}"
                
            elif config['type'] == 'risk_parity':
                model, metadata = generator.create_risk_parity_problem(
                    n_assets=config['n_assets'],
                    market_regime=config.get('market', 'normal')
                )
                problem_name = f"risk_parity_{config['n_assets']}assets"
            
            # Solve classically with GUROBI
            model.optimize()
            
            if model.status == GRB.OPTIMAL:
                classical_objective = model.objVal
                classical_solution = [var.x for var in model.getVars() if var.varName.startswith('w')]
                
                print(f"   ✅ Classical solution found: objective = {classical_objective:.6f}")
                
                # Save LP file for quantum optimization
                lp_filename = output_path / f"{problem_name}.lp"
                model.write(str(lp_filename))  # IMPORTANT: Write LP file here
                
                # Post-process LP file to fix multi-line constraints and trailing commas
                
                with open(str(lp_filename), 'r') as f:
                    lines = f.readlines()

                fixed_lines = []
                i = 0
                while i < len(lines):
                    line = lines[i].rstrip('\n').strip()

                    if ':' in line and not re.search(r'(<=|>=|=)\s*[-+]?\d*\.?\d+(e[-+]?\d+)?$', line):
                        # Start of multiline constraint — merge all continuation lines
                        merged_line = line
                        i += 1
                        while i < len(lines):
                            next_line = lines[i].rstrip('\n').strip()
                            # Break if next line looks like start of new constraint or section
                            if next_line == '' or (':' in next_line and not next_line.startswith(('+', '-'))):
                                break
                            merged_line += ' ' + next_line
                            i += 1
                            # Stop merging if line ends with <=, >= or = with number
                            if re.search(r'(<=|>=|=)\s*[-+]?\d*\.?\d+(e[-+]?\d+)?$', merged_line):
                                break
                        # Remove *all* commas inside the constraint line (LP format does not support commas in constraints)
                        merged_line = merged_line.replace(',', '')
                        fixed_lines.append(merged_line)
                    else:
                        # Remove trailing commas just in case
                        line = line.rstrip(',')
                        fixed_lines.append(line)
                        i += 1

                with open(str(lp_filename), 'w') as f:
                    for fixed_line in fixed_lines:
                        f.write(fixed_line + '\n')
                
                # Save metadata for analysis
                metadata.update({
                    'problem_name': problem_name,
                    'classical_objective': classical_objective,
                    'classical_solution': classical_solution,
                    'problem_type': config['type'],
                    'n_assets': config['n_assets']
                })
                
                metadata_filename = output_path / f"{problem_name}_metadata.pkl"
                import pickle
                with open(metadata_filename, 'wb') as f:
                    pickle.dump(metadata, f)
                
                problems_created.append({
                    'name': problem_name,
                    'lp_file': str(lp_filename),
                    'metadata_file': str(metadata_filename),
                    'classical_objective': classical_objective,
                    'n_assets': config['n_assets'],
                    'type': config['type']
                })
                
            else:
                print(f"   ❌ Failed to solve classically (status: {model.status})")
                
        except Exception as e:
            print(f"   ❌ Error creating problem: {e}")
            continue
    
    # Write summary report
    summary_file = output_path / "problem_suite_summary.txt"
    with open(summary_file, 'w') as f:
        f.write("Vanguard Portfolio Optimization Test Suite\n")
        f.write("="*50 + "\n\n")
        f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total problems: {len(problems_created)}\n\n")
        
        for problem in problems_created:
            f.write(f"Problem: {problem['name']}\n")
            f.write(f"  Type: {problem['type']}\n")
            f.write(f"  Assets: {problem['n_assets']}\n")
            f.write(f"  Classical objective: {problem['classical_objective']:.6f}\n")
            f.write(f"  LP file: {problem['lp_file']}\n\n")
    
    print(f"\n🎉 Created {len(problems_created)} portfolio optimization problems!")
    print(f"📁 Files saved to: {output_path.absolute()}")
    print(f"📋 Summary: {summary_file}")
    print("\n🚀 Ready for quantum optimization testing!")
    
    return problems_created

if __name__ == "__main__":
    # Create the comprehensive test suite
    problems = create_vanguard_test_suite()
    
    print("\n" + "="*60)
    print("NEXT STEPS:")
    print("="*60)
    print("1. Run quantum optimization on these problems using the VQE framework")
    print("2. Compare quantum vs classical results") 
    print("3. Analyze scalability (31 → 109 → 155 assets)")
    print("4. Focus on problems where quantum shows advantage")
    print("5. Present results showing domain expertise + quantum optimization")
