"""
Ma'at PATTERN ORGANIZER
=======================
TASK-119: Scale order structure analysis

Organizes chaos into patterns:
- Pattern detection and classification
- Schema generation
- Organizational hierarchy creation
- Chaos-to-order transformation

Author: C3 Oracle - TOASTED AI Trinity
Seal: MAAT_PATTERN_ORGANIZER_137
"""

import time
import hashlib
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import threading
import math


class PatternType(Enum):
    """Types of organizational patterns"""
    HIERARCHICAL = "hierarchical"   # Tree structures
    SEQUENTIAL = "sequential"       # Linear sequences
    NETWORK = "network"             # Graph/mesh patterns
    CIRCULAR = "circular"           # Cyclical patterns
    FRACTAL = "fractal"             # Self-similar patterns
    MATRIX = "matrix"               # Grid/table patterns


class OrganizationStrategy(Enum):
    """Strategies for organizing chaos"""
    BY_TYPE = "by_type"             # Group by type
    BY_FUNCTION = "by_function"     # Group by function
    BY_RELATIONSHIP = "by_relationship"  # Group by connections
    BY_FREQUENCY = "by_frequency"   # Group by usage
    BY_HIERARCHY = "by_hierarchy"   # Natural hierarchy
    BY_CHRONOLOGY = "by_chronology" # By time


@dataclass
class DetectedPattern:
    """A detected pattern in the data"""
    pattern_id: str
    pattern_type: PatternType
    confidence: float  # 0.0-1.0
    instances: int
    description: str
    elements: List[str]
    structure: Dict[str, Any]
    detected_at: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict:
        return {
            'pattern_id': self.pattern_id,
            'type': self.pattern_type.value,
            'confidence': self.confidence,
            'instances': self.instances,
            'description': self.description,
            'elements': self.elements[:10],  # First 10
            'structure': self.structure,
            'detected_at': self.detected_at
        }


@dataclass
class OrganizationalSchema:
    """A schema for organizing data"""
    schema_id: str
    name: str
    strategy: OrganizationStrategy
    categories: Dict[str, List[str]]
    hierarchy: Dict[str, Any]
    relationships: List[Dict]
    order_score: float
    created_at: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict:
        return {
            'schema_id': self.schema_id,
            'name': self.name,
            'strategy': self.strategy.value,
            'categories': {k: v[:10] for k, v in self.categories.items()},
            'hierarchy_depth': self._measure_depth(self.hierarchy),
            'relationship_count': len(self.relationships),
            'order_score': self.order_score,
            'created_at': self.created_at
        }
    
    def _measure_depth(self, obj: Dict, current: int = 0) -> int:
        if not isinstance(obj, dict) or not obj:
            return current
        return max(self._measure_depth(v, current + 1) for v in obj.values())


class PatternOrganizer:
    """
    Organizes chaos into patterns and structure.
    
    Ma'at ORDER Principle:
    - Chaos must be organized into patterns
    - Structure enables function
    - Self-organization toward greater order
    """
    
    VERSION = "1.0.0"
    MAAT_SEAL = "PATTERN_ORGANIZER_137"
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.detected_patterns: Dict[str, DetectedPattern] = {}
        self.generated_schemas: Dict[str, OrganizationalSchema] = {}
        self._lock = threading.Lock()
        
        # Analysis configuration
        self.min_pattern_confidence = self.config.get('min_confidence', 0.7)
        self.max_hierarchy_depth = self.config.get('max_depth', 7)
    
    def analyze_for_patterns(self, data: Any) -> List[DetectedPattern]:
        """
        Analyze data to detect organizational patterns.
        
        Args:
            data: Raw data to analyze
            
        Returns:
            List of detected patterns
        """
        patterns = []
        
        if isinstance(data, dict):
            # Check for hierarchical patterns
            hier_pattern = self._detect_hierarchical(data)
            if hier_pattern:
                patterns.append(hier_pattern)
            
            # Check for sequential patterns
            seq_pattern = self._detect_sequential(data)
            if seq_pattern:
                patterns.append(seq_pattern)
            
            # Check for network patterns
            net_pattern = self._detect_network(data)
            if net_pattern:
                patterns.append(net_pattern)
            
            # Check for fractal/self-similar patterns
            fractal_pattern = self._detect_fractal(data)
            if fractal_pattern:
                patterns.append(fractal_pattern)
            
            # Check for matrix patterns
            matrix_pattern = self._detect_matrix(data)
            if matrix_pattern:
                patterns.append(matrix_pattern)
        
        elif isinstance(data, list):
            # Check for sequential patterns in lists
            if data:
                seq_pattern = self._detect_list_sequence(data)
                if seq_pattern:
                    patterns.append(seq_pattern)
                
                # Check for grouping patterns
                group_pattern = self._detect_grouping(data)
                if group_pattern:
                    patterns.append(group_pattern)
        
        # Store detected patterns
        with self._lock:
            for p in patterns:
                self.detected_patterns[p.pattern_id] = p
        
        return patterns
    
    def organize(
        self,
        data: Any,
        strategy: OrganizationStrategy = OrganizationStrategy.BY_TYPE
    ) -> OrganizationalSchema:
        """
        Organize chaotic data into structured schema.
        
        Args:
            data: Data to organize
            strategy: Organization strategy to use
            
        Returns:
            OrganizationalSchema with organized structure
        """
        organizers = {
            OrganizationStrategy.BY_TYPE: self._organize_by_type,
            OrganizationStrategy.BY_FUNCTION: self._organize_by_function,
            OrganizationStrategy.BY_RELATIONSHIP: self._organize_by_relationship,
            OrganizationStrategy.BY_FREQUENCY: self._organize_by_frequency,
            OrganizationStrategy.BY_HIERARCHY: self._organize_by_hierarchy,
            OrganizationStrategy.BY_CHRONOLOGY: self._organize_by_chronology
        }
        
        organizer = organizers.get(strategy, self._organize_by_type)
        schema = organizer(data)
        
        with self._lock:
            self.generated_schemas[schema.schema_id] = schema
        
        return schema
    
    def transform_chaos_to_order(self, data: Any) -> Dict[str, Any]:
        """
        Transform chaotic data into ordered structure.
        Uses pattern detection to choose optimal organization.
        
        Args:
            data: Chaotic/unstructured data
            
        Returns:
            Ordered structure with transformation report
        """
        # Step 1: Analyze patterns
        patterns = self.analyze_for_patterns(data)
        
        # Step 2: Choose best strategy based on patterns
        best_strategy = self._choose_strategy(patterns)
        
        # Step 3: Organize
        schema = self.organize(data, best_strategy)
        
        # Step 4: Calculate order improvement
        chaos_score = self._measure_chaos(data)
        order_score = schema.order_score
        improvement = order_score - (1.0 - chaos_score)
        
        return {
            'original_chaos_score': chaos_score,
            'final_order_score': order_score,
            'improvement': improvement,
            'patterns_detected': [p.to_dict() for p in patterns],
            'strategy_used': best_strategy.value,
            'schema': schema.to_dict(),
            'maat_alignment': {
                'pillar': 'ORDER',
                'transformation': 'chaos_to_order',
                'success': improvement > 0
            }
        }
    
    # Pattern detection methods
    def _detect_hierarchical(self, data: Dict) -> Optional[DetectedPattern]:
        """Detect hierarchical patterns"""
        def count_levels(obj, level=0):
            if not isinstance(obj, dict):
                return level
            if not obj:
                return level
            return max(count_levels(v, level + 1) for v in obj.values())
        
        depth = count_levels(data)
        if depth >= 2:
            return DetectedPattern(
                pattern_id=self._gen_id('hier'),
                pattern_type=PatternType.HIERARCHICAL,
                confidence=min(0.5 + depth * 0.1, 1.0),
                instances=1,
                description=f"Hierarchical structure with depth {depth}",
                elements=list(data.keys())[:10],
                structure={'depth': depth, 'root_keys': list(data.keys())}
            )
        return None
    
    def _detect_sequential(self, data: Dict) -> Optional[DetectedPattern]:
        """Detect sequential patterns in dict"""
        sequences = []
        for key, value in data.items():
            if isinstance(value, list) and len(value) > 2:
                sequences.append(key)
        
        if sequences:
            return DetectedPattern(
                pattern_id=self._gen_id('seq'),
                pattern_type=PatternType.SEQUENTIAL,
                confidence=0.7 + 0.1 * min(len(sequences), 3),
                instances=len(sequences),
                description=f"Sequential patterns in {len(sequences)} fields",
                elements=sequences,
                structure={'sequence_keys': sequences}
            )
        return None
    
    def _detect_network(self, data: Dict) -> Optional[DetectedPattern]:
        """Detect network/graph patterns"""
        # Look for references between entities
        refs = data.get('references', data.get('links', data.get('edges', {})))
        nodes = data.get('nodes', data.get('entities', {}))
        
        if refs and nodes:
            return DetectedPattern(
                pattern_id=self._gen_id('net'),
                pattern_type=PatternType.NETWORK,
                confidence=0.85,
                instances=len(refs),
                description=f"Network pattern with {len(nodes)} nodes and {len(refs)} edges",
                elements=list(nodes.keys())[:10] if isinstance(nodes, dict) else [],
                structure={'node_count': len(nodes), 'edge_count': len(refs)}
            )
        return None
    
    def _detect_fractal(self, data: Dict) -> Optional[DetectedPattern]:
        """Detect self-similar/fractal patterns"""
        def get_structure_signature(obj, depth=0, max_depth=3):
            if depth >= max_depth or not isinstance(obj, dict):
                return type(obj).__name__
            return {k: get_structure_signature(v, depth+1, max_depth) for k in sorted(obj.keys())}
        
        # Check if sub-structures are similar
        signatures = []
        for value in data.values():
            if isinstance(value, dict):
                sig = str(get_structure_signature(value))
                signatures.append(sig)
        
        if len(signatures) >= 2:
            # Count similar signatures
            sig_counts = defaultdict(int)
            for sig in signatures:
                sig_counts[sig] += 1
            
            max_similar = max(sig_counts.values())
            if max_similar >= 2:
                return DetectedPattern(
                    pattern_id=self._gen_id('frac'),
                    pattern_type=PatternType.FRACTAL,
                    confidence=min(0.5 + max_similar * 0.15, 1.0),
                    instances=max_similar,
                    description=f"Self-similar pattern with {max_similar} instances",
                    elements=[k for k, v in data.items() if isinstance(v, dict)][:10],
                    structure={'similar_count': max_similar}
                )
        return None
    
    def _detect_matrix(self, data: Dict) -> Optional[DetectedPattern]:
        """Detect matrix/grid patterns"""
        # Look for 2D array structures
        for key, value in data.items():
            if isinstance(value, list) and len(value) > 0:
                if all(isinstance(row, list) for row in value):
                    rows = len(value)
                    cols = len(value[0]) if value else 0
                    return DetectedPattern(
                        pattern_id=self._gen_id('mat'),
                        pattern_type=PatternType.MATRIX,
                        confidence=0.9,
                        instances=1,
                        description=f"Matrix pattern {rows}x{cols}",
                        elements=[key],
                        structure={'rows': rows, 'cols': cols, 'field': key}
                    )
        return None
    
    def _detect_list_sequence(self, data: List) -> Optional[DetectedPattern]:
        """Detect sequential pattern in list"""
        if len(data) >= 3:
            # Check if items have ordering
            has_order = all(
                isinstance(item, dict) and ('order' in item or 'index' in item or 'position' in item)
                for item in data[:5]
            )
            
            return DetectedPattern(
                pattern_id=self._gen_id('lseq'),
                pattern_type=PatternType.SEQUENTIAL,
                confidence=0.8 if has_order else 0.6,
                instances=len(data),
                description=f"Sequential list with {len(data)} items",
                elements=[str(item)[:50] for item in data[:5]],
                structure={'length': len(data), 'has_explicit_order': has_order}
            )
        return None
    
    def _detect_grouping(self, data: List) -> Optional[DetectedPattern]:
        """Detect grouping pattern in list"""
        if not data or not isinstance(data[0], dict):
            return None
        
        # Look for common grouping fields
        group_fields = ['type', 'category', 'group', 'class', 'kind']
        found_field = None
        
        for field in group_fields:
            if all(field in item for item in data if isinstance(item, dict)):
                found_field = field
                break
        
        if found_field:
            groups = defaultdict(list)
            for item in data:
                if isinstance(item, dict):
                    groups[item.get(found_field, 'unknown')].append(item)
            
            return DetectedPattern(
                pattern_id=self._gen_id('grp'),
                pattern_type=PatternType.HIERARCHICAL,
                confidence=0.85,
                instances=len(groups),
                description=f"Groupable by '{found_field}' into {len(groups)} groups",
                elements=list(groups.keys()),
                structure={'group_field': found_field, 'groups': dict(groups)}
            )
        return None
    
    # Organization methods
    def _organize_by_type(self, data: Any) -> OrganizationalSchema:
        """Organize data by type"""
        categories = defaultdict(list)
        
        def categorize(obj, path=""):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    type_name = type(v).__name__
                    categories[type_name].append(f"{path}.{k}" if path else k)
                    if isinstance(v, (dict, list)):
                        categorize(v, f"{path}.{k}" if path else k)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    type_name = type(item).__name__
                    categories[type_name].append(f"{path}[{i}]")
                    if isinstance(item, (dict, list)):
                        categorize(item, f"{path}[{i}]")
        
        categorize(data)
        
        hierarchy = {
            'root': {
                type_name: {'count': len(items), 'sample': items[:3]}
                for type_name, items in categories.items()
            }
        }
        
        return OrganizationalSchema(
            schema_id=self._gen_id('schema_type'),
            name='Type-based Organization',
            strategy=OrganizationStrategy.BY_TYPE,
            categories=dict(categories),
            hierarchy=hierarchy,
            relationships=[],
            order_score=self._calculate_order_score(categories)
        )
    
    def _organize_by_function(self, data: Any) -> OrganizationalSchema:
        """Organize by functional role"""
        categories = {
            'data': [],
            'metadata': [],
            'configuration': [],
            'references': [],
            'computed': []
        }
        
        if isinstance(data, dict):
            for key, value in data.items():
                if key.startswith('_') or key in ('id', 'type', 'version', 'name'):
                    categories['metadata'].append(key)
                elif key in ('config', 'settings', 'options'):
                    categories['configuration'].append(key)
                elif key in ('refs', 'links', 'references', 'dependencies'):
                    categories['references'].append(key)
                elif callable(value):
                    categories['computed'].append(key)
                else:
                    categories['data'].append(key)
        
        return OrganizationalSchema(
            schema_id=self._gen_id('schema_func'),
            name='Function-based Organization',
            strategy=OrganizationStrategy.BY_FUNCTION,
            categories=categories,
            hierarchy={'functions': categories},
            relationships=[],
            order_score=self._calculate_order_score(categories)
        )
    
    def _organize_by_relationship(self, data: Any) -> OrganizationalSchema:
        """Organize by relationships between elements"""
        categories = defaultdict(list)
        relationships = []
        
        if isinstance(data, dict):
            refs = data.get('references', {})
            entities = data.get('entities', data.get('nodes', {}))
            
            # Group entities by their relationships
            for entity_id, entity in entities.items() if isinstance(entities, dict) else []:
                connected_to = []
                for ref_name, ref_target in refs.items():
                    if entity_id in str(ref_target):
                        connected_to.append(ref_name)
                
                if connected_to:
                    categories['connected'].append(entity_id)
                    relationships.append({
                        'source': entity_id,
                        'targets': connected_to
                    })
                else:
                    categories['isolated'].append(entity_id)
        
        return OrganizationalSchema(
            schema_id=self._gen_id('schema_rel'),
            name='Relationship-based Organization',
            strategy=OrganizationStrategy.BY_RELATIONSHIP,
            categories=dict(categories),
            hierarchy={'relationship_groups': dict(categories)},
            relationships=relationships,
            order_score=self._calculate_order_score(categories)
        )
    
    def _organize_by_frequency(self, data: Any) -> OrganizationalSchema:
        """Organize by usage frequency"""
        # Simulate frequency analysis
        categories = {
            'high_frequency': [],
            'medium_frequency': [],
            'low_frequency': []
        }
        
        if isinstance(data, dict):
            # Use key length as proxy for frequency (shorter = more frequent)
            for key in data.keys():
                if len(key) <= 4:
                    categories['high_frequency'].append(key)
                elif len(key) <= 10:
                    categories['medium_frequency'].append(key)
                else:
                    categories['low_frequency'].append(key)
        
        return OrganizationalSchema(
            schema_id=self._gen_id('schema_freq'),
            name='Frequency-based Organization',
            strategy=OrganizationStrategy.BY_FREQUENCY,
            categories=categories,
            hierarchy={'frequency_bands': categories},
            relationships=[],
            order_score=self._calculate_order_score(categories)
        )
    
    def _organize_by_hierarchy(self, data: Any) -> OrganizationalSchema:
        """Organize by natural hierarchy"""
        categories = defaultdict(list)
        
        def extract_hierarchy(obj, level=0, path=""):
            level_name = f"level_{level}"
            if isinstance(obj, dict):
                for k, v in obj.items():
                    full_path = f"{path}.{k}" if path else k
                    categories[level_name].append(full_path)
                    if isinstance(v, dict):
                        extract_hierarchy(v, level + 1, full_path)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    if isinstance(item, dict):
                        extract_hierarchy(item, level + 1, f"{path}[{i}]")
        
        extract_hierarchy(data)
        
        hierarchy = {}
        for level_name, items in sorted(categories.items()):
            hierarchy[level_name] = items
        
        return OrganizationalSchema(
            schema_id=self._gen_id('schema_hier'),
            name='Hierarchy-based Organization',
            strategy=OrganizationStrategy.BY_HIERARCHY,
            categories=dict(categories),
            hierarchy=hierarchy,
            relationships=[],
            order_score=self._calculate_order_score(categories)
        )
    
    def _organize_by_chronology(self, data: Any) -> OrganizationalSchema:
        """Organize by time/chronology"""
        categories = {
            'timestamped': [],
            'undated': []
        }
        
        time_fields = {'timestamp', 'created_at', 'updated_at', 'date', 'time'}
        
        def find_timestamped(obj, path=""):
            if isinstance(obj, dict):
                has_time = any(f in obj for f in time_fields)
                if has_time:
                    categories['timestamped'].append(path or 'root')
                else:
                    categories['undated'].append(path or 'root')
                
                for k, v in obj.items():
                    if isinstance(v, dict):
                        find_timestamped(v, f"{path}.{k}" if path else k)
        
        find_timestamped(data)
        
        return OrganizationalSchema(
            schema_id=self._gen_id('schema_chron'),
            name='Chronology-based Organization',
            strategy=OrganizationStrategy.BY_CHRONOLOGY,
            categories=categories,
            hierarchy={'temporal': categories},
            relationships=[],
            order_score=self._calculate_order_score(categories)
        )
    
    # Helper methods
    def _gen_id(self, prefix: str) -> str:
        return hashlib.sha256(f"{prefix}_{time.time()}".encode()).hexdigest()[:12]
    
    def _choose_strategy(self, patterns: List[DetectedPattern]) -> OrganizationStrategy:
        """Choose best organization strategy based on patterns"""
        if not patterns:
            return OrganizationStrategy.BY_TYPE
        
        # Map pattern types to strategies
        pattern_to_strategy = {
            PatternType.HIERARCHICAL: OrganizationStrategy.BY_HIERARCHY,
            PatternType.SEQUENTIAL: OrganizationStrategy.BY_CHRONOLOGY,
            PatternType.NETWORK: OrganizationStrategy.BY_RELATIONSHIP,
            PatternType.MATRIX: OrganizationStrategy.BY_TYPE,
            PatternType.FRACTAL: OrganizationStrategy.BY_HIERARCHY
        }
        
        # Choose based on highest confidence pattern
        best_pattern = max(patterns, key=lambda p: p.confidence)
        return pattern_to_strategy.get(best_pattern.pattern_type, OrganizationStrategy.BY_TYPE)
    
    def _measure_chaos(self, data: Any) -> float:
        """Measure chaos level in data (0 = ordered, 1 = chaotic)"""
        chaos = 0.5  # Base
        
        if isinstance(data, dict):
            # Check key naming consistency
            keys = list(data.keys())
            if keys:
                naming_styles = set()
                for k in keys:
                    if '_' in k:
                        naming_styles.add('snake')
                    elif any(c.isupper() for c in k[1:]):
                        naming_styles.add('camel')
                    else:
                        naming_styles.add('other')
                
                if len(naming_styles) > 1:
                    chaos += 0.1 * len(naming_styles)
            
            # Check type consistency
            value_types = set(type(v).__name__ for v in data.values())
            if len(value_types) > 3:
                chaos += 0.1
            
            # Check depth variance
            depths = []
            def measure_depth(obj, d=0):
                if isinstance(obj, dict):
                    for v in obj.values():
                        measure_depth(v, d + 1)
                else:
                    depths.append(d)
            measure_depth(data)
            
            if depths:
                variance = sum((d - sum(depths)/len(depths))**2 for d in depths) / len(depths)
                chaos += 0.05 * min(variance, 3)
        
        return min(1.0, chaos)
    
    def _calculate_order_score(self, categories: Dict) -> float:
        """Calculate order score from categorization"""
        if not categories:
            return 0.5
        
        # More categories = more organized (up to a point)
        non_empty = sum(1 for v in categories.values() if v)
        category_score = min(non_empty / 5, 1.0) * 0.3
        
        # Balance of items across categories
        if any(categories.values()):
            sizes = [len(v) for v in categories.values() if v]
            if sizes:
                avg_size = sum(sizes) / len(sizes)
                variance = sum((s - avg_size)**2 for s in sizes) / len(sizes)
                balance_score = max(0, 1 - variance / 100) * 0.3
            else:
                balance_score = 0.15
        else:
            balance_score = 0.15
        
        # Coverage score
        total_items = sum(len(v) for v in categories.values())
        coverage_score = min(total_items / 10, 1.0) * 0.4
        
        return min(1.0, 0.3 + category_score + balance_score + coverage_score)
    
    def get_pattern_summary(self) -> Dict[str, Any]:
        """Get summary of all detected patterns"""
        with self._lock:
            patterns = list(self.detected_patterns.values())
            schemas = list(self.generated_schemas.values())
        
        pattern_by_type = defaultdict(int)
        for p in patterns:
            pattern_by_type[p.pattern_type.value] += 1
        
        return {
            'version': self.VERSION,
            'maat_seal': self.MAAT_SEAL,
            'timestamp': time.time(),
            'patterns': {
                'total': len(patterns),
                'by_type': dict(pattern_by_type),
                'high_confidence': len([p for p in patterns if p.confidence >= 0.8])
            },
            'schemas': {
                'total': len(schemas),
                'average_order_score': sum(s.order_score for s in schemas) / len(schemas) if schemas else 0
            },
            'maat_alignment': {
                'pillar': 'ORDER',
                'pattern_recognition': 'active',
                'chaos_transformation': 'enabled'
            }
        }


# Demonstration
if __name__ == "__main__":
    organizer = PatternOrganizer()
    
    # Chaotic test data
    chaotic_data = {
        'UserName': 'test',
        'user_email': 'test@example.com',
        'DATA': [1, 2, 3],
        'items': [
            {'type': 'A', 'value': 1},
            {'type': 'B', 'value': 2},
            {'type': 'A', 'value': 3}
        ],
        'config': {
            'deep': {
                'nested': {
                    'value': True
                }
            }
        },
        'references': {
            'user_items': 'items'
        },
        'entities': {
            'user': {'name': 'User'},
            'items': {'count': 3}
        }
    }
    
    # Transform chaos to order
    result = organizer.transform_chaos_to_order(chaotic_data)
    
    print("=" * 60)
    print("MA'AT PATTERN ORGANIZER - Chaos to Order")
    print("=" * 60)
    print(f"\nOriginal Chaos Score: {result['original_chaos_score']:.2f}")
    print(f"Final Order Score: {result['final_order_score']:.2f}")
    print(f"Improvement: {result['improvement']:.2f}")
    print(f"\nStrategy Used: {result['strategy_used']}")
    
    print(f"\nPatterns Detected:")
    for p in result['patterns_detected']:
        print(f"  - {p['type']}: {p['description']} (confidence: {p['confidence']:.2f})")
    
    print(f"\nSchema Generated: {result['schema']['name']}")
    print(f"Categories: {list(result['schema']['categories'].keys())}")
    print(f"\nMa'at Alignment: {result['maat_alignment']}")
