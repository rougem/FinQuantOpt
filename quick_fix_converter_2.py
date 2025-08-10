#!/usr/bin/env python3
"""
Quick Fix LP Format Converter - Windows Compatible
Just fixes the ROOT issue so you can keep moving
"""

import re
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any

# HARDCODED FIX for Windows - replace with your actual path if needed
ROOT = r"C:\path\to\WISER_Optimization_VG"

class LPFormatConverter:
    """Convert standard LP format to VQE-compatible representation"""
    
    def __init__(self):
        self.objective_terms = {}
        self.constraints = []
        self.bounds = {}
        self.variables = set()

    def _normalize_var_name(self, var: str) -> str:
        """Convert variable names like w[0] into w_0 for CPLEX compatibility"""
        # Replace brackets with underscore notation
        return re.sub(r'\[([0-9]+)\]', r'_\1', var)

    def convert_file(self, input_file: str, output_file: str = None) -> str:
        """Main conversion function"""
        if output_file is None:
            # Create output in converted_problems directory
            input_path = Path(input_file)
            output_dir = Path("converted_problems")
            output_dir.mkdir(exist_ok=True)
            output_file = output_dir / f"{input_path.stem}_converted.lp"
        
        print(f"🔄 Converting {input_file} -> {output_file}")
        
        # Parse input file
        self._parse_lp_file(input_file)
        
        # Generate VQE-compatible format
        self._write_vqe_format(str(output_file))
        
        print(f"✅ Conversion complete: {len(self.constraints)} constraints, {len(self.variables)} variables")
        return str(output_file)
    
    def _parse_lp_file(self, filename: str):
        """Parse GUROBI .lp file format with proper constraint handling"""
        with open(filename, 'r') as f:
            content = f.read()
        
        # Clean up content
        content = re.sub(r'\\.*$', '', content, flags=re.MULTILINE)  # Remove comments
        content = re.sub(r'\s+', ' ', content)  # Normalize whitespace
        
        # Split into sections
        sections = self._split_sections(content)
        
        # Parse each section
        if 'objective' in sections:
            self.objective_terms = self._parse_objective(sections['objective'])
        
        if 'constraints' in sections:
            self.constraints = self._parse_constraints_fixed(sections['constraints'])
        
        if 'bounds' in sections:
            self.bounds = self._parse_bounds(sections['bounds'])
    
    # def _split_sections(self, content: str) -> Dict[str, str]:
    #     """Split LP content into sections"""
    #     sections = {}
        
    #     # Define section patterns
    #     patterns = {
    #         'objective': r'(minimize|maximize|min|max|obj)(.*?)(?=subject to|s\.t\.|constraints|bounds|end|\Z)',
    #         'constraints': r'(subject to|s\.t\.|constraints)(.*?)(?=bounds|end|\Z)',
    #         'bounds': r'bounds(.*?)(?=end|\Z)',
    #     }
        
    #     for section_name, pattern in patterns.items():
    #         match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
    #         if match:
    #             sections[section_name] = match.group(2).strip()
        
    #     return sections
    
    def _split_sections(self, content: str) -> Dict[str, str]:
        """Split LP content into sections"""
        sections = {}
        
        patterns = {
            'objective': r'(minimize|maximize|min|max|obj)(.*?)(?=subject to|s\.t\.|constraints|bounds|end|\Z)',
            'constraints': r'(subject to|s\.t\.|constraints)(.*?)(?=bounds|end|\Z)',
            'bounds': r'(bounds)(.*?)(?=end|\Z)',  # changed to always have two groups
        }
        
        for section_name, pattern in patterns.items():
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                # Get the last captured group that actually has content
                # text_part = next((g for g in match.groups()[1:] if g is not None), "")
                text_part = " ".join(g for g in match.groups()[1:] if g)
                sections[section_name] = text_part.strip()
        
        return sections
    
    def fix_scientific_notation_bug(tokens):
        fixed_tokens = []
        skip_next = False
        for i, tok in enumerate(tokens):
            if skip_next:
                skip_next = False
                continue

            # If we see a floating number followed by a single 'e', merge with next token
            if re.fullmatch(r"\d+\.\d+", tok) and i + 2 < len(tokens) and tokens[i+1].lower() == 'e':
                merged = tok + tokens[i+1] + tokens[i+2]  # merge number + 'e' + exponent
                fixed_tokens.append(merged)
                skip_next = True  # skip exponent token
                continue

            # If number followed by lone 'e' (no exponent), treat 'e' as a variable
            if re.fullmatch(r"\d+\.\d+", tok) and i + 1 < len(tokens) and tokens[i+1].lower() == 'e':
                # Here you can rename the 'e' variable to something like w_xxx or keep as is
                fixed_tokens.append(tok)
                fixed_tokens.append("w_e")  # give it a proper variable name
                skip_next = True
                continue

            fixed_tokens.append(tok)
        return fixed_tokens
    
    # def _parse_objective(self, obj_text: str) -> Dict[str, float]:
    #     """Parse objective function"""
    #     objective_terms = {}
        
    #     # Pattern for variable terms (handles portfolio_weight_X, etc.)
    #     pattern = r'([+-]?\s*\d*\.?\d*)\s*\*?\s*([a-zA-Z_][a-zA-Z0-9_\[\]]*(?:\^?\d*)?)'
        
    #     matches = re.finditer(pattern, obj_text)
        
    #     for match in matches:
    #         coeff_str, var = match.groups()
    #         coeff = self._parse_coefficient(coeff_str)
            
    #         if var:
    #             var = self._normalize_var_name(var.strip())
    #             objective_terms[var] = objective_terms.get(var, 0) + coeff
    #             self.variables.add(var)
        
    #     return objective_terms
    
    def _parse_objective(self, obj_text: str) -> Dict[str, float]:
        """Parse objective function with proper float exponent support"""
        objective_terms = {}
        
        # New regex pattern to correctly capture numbers with exponents and variables
        pattern = r'([+-]?\s*\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)[ ]*\*?[ ]*([a-zA-Z_][a-zA-Z0-9_\[\]]*)'
        
        matches = re.finditer(pattern, obj_text)
        
        for match in matches:
            coeff_str, var = match.groups()
            coeff = self._parse_coefficient(coeff_str)
            
            if var:
                var = self._normalize_var_name(var.strip())
                objective_terms[var] = objective_terms.get(var, 0) + coeff
                self.variables.add(var)
        
        return objective_terms

    
    def _parse_constraints_fixed(self, constraint_text: str) -> List[Dict[str, Any]]:
        """FIXED VERSION: Properly handle multi-line constraints"""
        constraints = []
        lines = constraint_text.strip().split('\n')
        
        current_constraint = ""
        constraint_name = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if this starts a new constraint (has colon and doesn't start with +/-)
            if ':' in line and not line.startswith(('+', '-')):
                # Process previous constraint
                if current_constraint and constraint_name:
                    constraint_dict = self._parse_single_constraint_fixed(constraint_name, current_constraint)
                    if constraint_dict:
                        constraints.append(constraint_dict)
                
                # Start new constraint
                name_part, expr_part = line.split(':', 1)
                constraint_name = name_part.strip()
                current_constraint = expr_part.strip()
            else:
                # Continuation line
                current_constraint += " " + line
        
        # Process final constraint
        if current_constraint and constraint_name:
            constraint_dict = self._parse_single_constraint_fixed(constraint_name, current_constraint)
            if constraint_dict:
                constraints.append(constraint_dict)
        
        return constraints
    
    def _parse_single_constraint_fixed(self, name: str, expr: str) -> Dict[str, Any]:
        """Parse a single constraint expression"""
        try:
            constraint_dict = {
                'name': name,
                'terms': {},
                'sense': '=',
                'rhs': 0.0
            }
            
            # Find constraint sense
            sense_patterns = [
                ('<=', r'(.+?)\s*<=\s*(.+)'),
                ('>=', r'(.+?)\s*>=\s*(.+)'),
                ('=', r'(.+?)\s*=\s*(.+)')
            ]
            
            lhs_expr = expr
            rhs_value = 0.0
            
            for sense, pattern in sense_patterns:
                match = re.search(pattern, expr)
                if match:
                    lhs_expr = match.group(1).strip()
                    rhs_str = match.group(2).strip()
                    constraint_dict['sense'] = sense
                    
                    try:
                        rhs_value = float(rhs_str)
                    except ValueError:
                        rhs_value = 0.0
                    
                    constraint_dict['rhs'] = rhs_value
                    break
            
            # Parse LHS terms
            terms = self._parse_linear_expression(lhs_expr)
            constraint_dict['terms'] = terms
            self.variables.update(terms.keys())
            
            return constraint_dict
            
        except Exception as e:
            print(f"⚠️ Error parsing constraint '{name}': {e}")
            return None
    
    def _parse_linear_expression(self, expr: str) -> Dict[str, float]:
        """Parse linear expression and extract variable coefficients"""
        terms = {}
        
        # Pattern for portfolio variables (allow brackets inside var names)
        pattern = r'([+-]?\s*\d*\.?\d*)\s*\*?\s*([a-zA-Z_][a-zA-Z0-9_\[\]]*)'
        
        for match in re.finditer(pattern, expr):
            coeff_str, var = match.groups()
            coeff = self._parse_coefficient(coeff_str)
            
            if var.strip():
                var = self._normalize_var_name(var.strip())
                terms[var] = terms.get(var, 0) + coeff
        
        return terms
    
    def _parse_coefficient(self, coeff_str: str) -> float:
        """Parse coefficient string"""
        coeff_str = coeff_str.replace(' ', '').strip()
        
        if not coeff_str or coeff_str == '+':
            return 1.0
        elif coeff_str == '-':
            return -1.0
        else:
            try:
                return float(coeff_str)
            except ValueError:
                return 1.0
    
    def _parse_bounds(self, bounds_text: str) -> Dict[str, Tuple[float, float]]:
        """Parse variable bounds (simplified)"""
        return {}  # Skip bounds for now to avoid complexity
    
    def _write_vqe_format(self, output_file: str):
        """Write VQE-compatible format"""
        with open(output_file, 'w') as f:
            # Write objective
            if self.objective_terms:
                f.write("minimize\n")
                f.write("obj: ")
                
                terms = []
                for var, coeff in self.objective_terms.items():
                    if coeff != 0:
                        if len(terms) == 0:
                            sign = '' if coeff >= 0 else '-'
                        else:
                            sign = ' + ' if coeff >= 0 else ' - '
                            coeff = abs(coeff)
                        
                        if coeff == 1:
                            terms.append(f"{sign}{var}")
                        else:
                            terms.append(f"{sign}{coeff} {var}")
                
                f.write("".join(terms))
                f.write("\n\n")
            
            # Write constraints (SINGLE LINES!)
            if self.constraints:
                f.write("subject to\n")
                
                for constraint in self.constraints:
                    name = constraint['name']
                    terms = constraint['terms']
                    sense = constraint['sense']
                    rhs = constraint['rhs']
                    
                    # Build constraint on ONE line
                    term_parts = []
                    for var, coeff in terms.items():
                        if coeff != 0:
                            if len(term_parts) == 0:
                                sign = '' if coeff >= 0 else '-'
                            else:
                                sign = ' + ' if coeff >= 0 else ' - '
                                coeff = abs(coeff)
                            
                            if coeff == 1:
                                term_parts.append(f"{sign}{var}")
                            else:
                                term_parts.append(f"{sign}{coeff} {var}")
                    
                    constraint_line = f"{name}: {''.join(term_parts)} {sense} {rhs}"
                    f.write(constraint_line + "\n")
                
                f.write("\n")
            
            # Write end
            f.write("end\n")


def main():
    """Quick command line interface"""
    if len(sys.argv) < 2:
        print("Usage: python lp_format_converter.py <input_file.lp>")
        return
    
    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"❌ Error: Input file '{input_file}' not found")
        return
    
    try:
        converter = LPFormatConverter()
        result_file = converter.convert_file(input_file)
        
        print(f"\n🎉 SUCCESS!")
        print(f"📁 Input: {input_file}")
        print(f"📁 Output: {result_file}")
        print(f"📊 Variables: {len(converter.variables)}")
        print(f"📋 Constraints: {len(converter.constraints)}")
        
        # Quick verification
        if os.path.exists(result_file):
            with open(result_file, 'r') as f:
                lines = f.readlines()
            print(f"📄 Output file has {len(lines)} lines")
            
            # Show sample
            print(f"\n🔍 First few lines of output:")
            for i, line in enumerate(lines[:5]):
                print(f"  {i+1}: {line.strip()}")
    
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
