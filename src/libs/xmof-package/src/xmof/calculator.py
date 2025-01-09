from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import networkx as nx
from sympy import sympify, pi, E
from cachetools import TTLCache
import hashlib

@dataclass
class Formula:
    """Class to represent a formula with metadata"""
    name: str
    description: str
    expression: str
    units: str = None
    rounding: Optional[int] = None
    parsed_expression: Any = None

class IndustrialCalculator:
    def __init__(self, default_rounding: Optional[int] = None, cache_ttl: int = 3600):
        self.dependency_graph = nx.DiGraph()
        self.formulas = {}
        self.inputs = {}
        self.default_rounding = default_rounding
        # Initialize cache with TTL (time-to-live) in seconds
        self.graph_cache = TTLCache(maxsize=100, ttl=cache_ttl)
        
    def _get_cache_key(self, formulas: Dict[str, Any]) -> str:
        """Generate a cache key from formulas dictionary"""
        # Create a stable string representation of the calculations
        calc_str = ";".join(sorted(
            f"{name}:{formula.get('expression', '')}" 
            for name, formula in formulas.items()
        ))
        return hashlib.md5(calc_str.encode()).hexdigest()

    def _build_dependency_graph(self, formulas_data: Dict[str, Any]) -> nx.DiGraph:
        """Build and cache directed graph of calculation dependencies"""
        cache_key = self._get_cache_key(formulas_data)
        
        # Check cache first
        if cache_key in self.graph_cache:
            return self.graph_cache[cache_key]
            
        # Build new graph if not in cache
        graph = nx.DiGraph()
        
        # Add all calculations as nodes
        for calc_name in self.formulas:
            graph.add_node(calc_name)
        
        # Add edges for dependencies
        for calc_name, formula in self.formulas.items():
            deps = {str(symbol) for symbol in formula.parsed_expression.free_symbols}
            for dep in deps:
                if dep in self.formulas:
                    graph.add_edge(dep, calc_name)
        
        if not nx.is_directed_acyclic_graph(graph):
            raise ValueError("Circular dependencies detected in calculations")
        
        # Store in cache
        self.graph_cache[cache_key] = graph
        return graph
        
    def parse_config(self, config: dict) -> None:
        """Parse configuration containing expressions and values"""
        try:
            self.inputs = config.get("input_values", {})
            formulas_data = config.get("calculations", {})
            
            if "default_rounding" in config:
                self.default_rounding = config["default_rounding"]
            
            # Add mathematical constants
            self.inputs.update({
                'pi': float(pi),
                'e': float(E)
            })
            
            # Process each formula definition
            new_formulas = {}
            for calc_name, formula_def in formulas_data.items():
                parsed_expr = sympify(formula_def["expression"])
                new_formulas[calc_name] = Formula(
                    name=formula_def.get("name", calc_name),
                    description=formula_def.get("description", ""),
                    expression=formula_def["expression"],
                    units=formula_def.get("units"),
                    rounding=formula_def.get("rounding", self.default_rounding),
                    parsed_expression=parsed_expr
                )
            
            # Update formulas
            self.formulas = new_formulas
            
            # Get dependency graph (will use cache if available)
            self.dependency_graph = self._build_dependency_graph(formulas_data)
                
        except Exception as e:
            raise ValueError(f"Error parsing configuration: {str(e)}")
    
    def _round_value(self, value: float, rounding: Optional[int]) -> float:
        if rounding is not None:
            return round(value, rounding)
        return value
    
    def evaluate(self) -> Dict[str, Any]:
        """Evaluate all expressions in the correct order"""
        if not self.formulas:
            raise ValueError("No calculations defined")
        
        calculation_order = list(nx.topological_sort(self.dependency_graph))
        results = {}
        errors = {}
        values = dict(self.inputs)
        cache_info = {
            "cache_size": len(self.graph_cache),
            "cache_maxsize": self.graph_cache.maxsize,
            "cache_currsize": len(self.graph_cache)
        }
        
        for calc_name in calculation_order:
            try:
                formula = self.formulas[calc_name]
                result = float(formula.parsed_expression.evalf(subs=values))
                result = self._round_value(result, formula.rounding)
                results[calc_name] = result
                values[calc_name] = result
            except Exception as e:
                errors[calc_name] = str(e)
        
        return {
            "results": results,
            "errors": errors if errors else None,
            "calculation_order": calculation_order,
            "cache_info": cache_info
        }