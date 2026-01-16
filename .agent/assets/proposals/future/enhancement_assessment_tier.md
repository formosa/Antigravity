# Implementation Plan: Assessment Layer Framework for Sphinx-Needs Documentation Systems

**Document Classification:** Research Knowledge Asset  
**Target System:** Sphinx + Sphinx-Needs + PlantUML + Graphviz  
**Implementation Complexity:** Enterprise-Grade, Production-Ready  
**Estimated Development Effort:** 320-400 hours (2-3 engineer-months)  

---

## Executive Summary

This implementation plan defines a comprehensive framework for injecting **metadata enrichment layers** between hierarchical documentation strata in Sphinx-based technical documentation systems. The framework enables automated classification of architectural elements according to established taxonomies (Design Patterns, Process Flow Models, etc.), programmatic validation of implementation adherence, and visual verification through diagram comparison.

**Core Capabilities Delivered:**
1. LLM-powered classification of documentation tags into design pattern roles
2. Jinja2-templated PlantUML diagram generation from enriched metadata
3. Graphviz-based visualization of tag dependency graphs and traceability matrices
4. Build-time validation comparing declared patterns against implementation blueprints
5. Programmatic assessment reporting with violation detection

---

## Phase 1: Foundation Architecture (80 hours)

### 1.1 Sphinx-Needs Schema Extension

**Objective:** Define custom need types and metadata fields to support assessment layer functionality.

#### 1.1.1 Custom Need Type Definitions

**File:** `conf.py` (Sphinx configuration)

```python
# Assessment Layer Need Types
needs_types = [
    # Existing types (preserved)
    dict(directive="req", title="Requirement", prefix="REQ_", color="#BFD8D2", style="node"),
    dict(directive="spec", title="Specification", prefix="SPEC_", color="#FEDCD2", style="node"),
    dict(directive="impl", title="Implementation", prefix="IMPL_", color="#DF744A", style="node"),
    
    # NEW: Assessment Layer Types
    dict(
        directive="pattern",
        title="Design Pattern",
        prefix="PAT_",
        color="#9B59B6",
        style="node",
        description="Architectural pattern classification and mapping"
    ),
    dict(
        directive="flow",
        title="Process Flow",
        prefix="FLOW_",
        color="#3498DB",
        style="node",
        description="Behavioral flow topology and sequencing"
    ),
    dict(
        directive="assess",
        title="Assessment Directive",
        prefix="ASSESS_",
        color="#E74C3C",
        style="node",
        description="LLM-powered classification trigger"
    ),
    dict(
        directive="validation",
        title="Validation Result",
        prefix="VAL_",
        color="#F39C12",
        style="node",
        description="Pattern adherence validation output"
    )
]
```

#### 1.1.2 Extended Metadata Fields

```python
# Custom fields for pattern assessment
needs_extra_options = [
    # Pattern Classification Fields
    "pattern_family",        # GoF | POSA | EIP | Custom
    "pattern_name",          # Observer | Singleton | Strategy | etc.
    "pattern_category",      # Creational | Structural | Behavioral
    "pattern_role",          # SUBJECT | OBSERVER | CONTEXT | STRATEGY | etc.
    "pattern_confidence",    # 0.0-1.0 (LLM classification confidence score)
    "pattern_rationale",     # Free text justification from LLM
    
    # Flow Classification Fields
    "flow_type",             # Sequential | Parallel | Conditional | Event-Driven
    "flow_error_handling",   # Fail-Fast | Retry | Circuit-Breaker | Compensating
    "flow_concurrency",      # Synchronous | Asynchronous | Reactive
    
    # Assessment Metadata
    "assessed_by",           # LLM model identifier (e.g., "gpt-4-turbo-2024-04-09")
    "assessment_timestamp",  # ISO 8601 timestamp
    "assessment_version",    # Semantic version for assessment rules
    
    # Validation Fields
    "validation_status",     # PASS | FAIL | WARNING | SKIPPED
    "violation_count",       # Integer count of detected violations
    "violation_details",     # JSON array of violation objects
    
    # Diagram Generation
    "diagram_template",      # Path to Jinja2 template file
    "diagram_type",          # plantuml | graphviz | combined
    "diagram_output_path",   # Relative path for generated diagram
    
    # Traceability Enhancement
    "applies_to_tags",       # Comma-separated list of tag IDs in scope
    "constrains_tags",       # Downstream tags that must respect this assessment
    "validated_against"      # Upstream tags used for validation
]

# Link type definitions for traceability
needs_extra_links = [
    {
        "option": "assessed_by",
        "incoming": "is assessed by",
        "outgoing": "assesses",
        "copy": False,
        "color": "#9B59B6"
    },
    {
        "option": "constrains",
        "incoming": "is constrained by",
        "outgoing": "constrains",
        "copy": False,
        "color": "#E74C3C"
    },
    {
        "option": "validates",
        "incoming": "is validated by",
        "outgoing": "validates",
        "copy": False,
        "color": "#F39C12"
    },
    {
        "option": "implements_pattern",
        "incoming": "pattern implemented by",
        "outgoing": "implements pattern",
        "copy": False,
        "color": "#3498DB"
    }
]
```

#### 1.1.3 Global Configuration Parameters

```python
# Assessment Layer Configuration
needs_assessment_config = {
    # LLM API Configuration
    "llm_provider": "openai",  # openai | anthropic | google | azure
    "llm_model": "gpt-4-turbo-2024-04-09",
    "llm_temperature": 0.1,  # Low temperature for deterministic classification
    "llm_max_tokens": 4096,
    "llm_timeout_seconds": 60,
    
    # Classification Schema Libraries
    "pattern_libraries": [
        "schemas/gof_patterns.yaml",
        "schemas/posa_patterns.yaml",
        "schemas/eip_patterns.yaml"
    ],
    "flow_taxonomies": [
        "schemas/flow_types.yaml",
        "schemas/concurrency_models.yaml"
    ],
    
    # Diagram Generation
    "plantuml_jar_path": "/usr/local/bin/plantuml.jar",
    "plantuml_output_format": "svg",  # svg | png | pdf
    "graphviz_engine": "dot",  # dot | neato | fdp | sfdp | circo
    "template_search_paths": [
        "_templates/plantuml",
        "_templates/graphviz"
    ],
    
    # Validation Rules
    "validation_strictness": "WARNING",  # ERROR | WARNING | INFO
    "fail_build_on_violations": False,
    "violation_report_path": "_build/validation_report.json",
    
    # Performance Optimization
    "enable_assessment_cache": True,
    "cache_ttl_hours": 168,  # 1 week
    "parallel_assessment_workers": 4,
    "batch_size_tags": 10
}
```

---

### 1.2 Pattern Classification Schema Library

**Objective:** Define machine-readable taxonomies for pattern recognition.

#### 1.2.1 GoF Patterns Schema

**File:** `schemas/gof_patterns.yaml`

```yaml
schema_metadata:
  name: "Gang of Four Design Patterns"
  version: "1.0.0"
  source: "Design Patterns: Elements of Reusable Object-Oriented Software (1994)"
  authority: "Gamma, Helm, Johnson, Vlissides"

categories:
  creational:
    description: "Patterns that deal with object creation mechanisms"
    patterns:
      - name: "Singleton"
        intent: "Ensure a class has only one instance and provide a global point of access to it"
        participants:
          - role: "SINGLETON"
            multiplicity: "1"
            responsibilities:
              - "Maintain single instance"
              - "Provide global access point"
        
      - name: "Factory Method"
        intent: "Define an interface for creating objects, but let subclasses decide which class to instantiate"
        participants:
          - role: "CREATOR"
            multiplicity: "1"
            responsibilities:
              - "Declare factory method"
          - role: "CONCRETE_CREATOR"
            multiplicity: "1..*"
            responsibilities:
              - "Override factory method to return ConcreteProduct"
          - role: "PRODUCT"
            multiplicity: "1"
            responsibilities:
              - "Define interface of objects the factory method creates"
          - role: "CONCRETE_PRODUCT"
            multiplicity: "1..*"
            responsibilities:
              - "Implement Product interface"
        
      - name: "Abstract Factory"
        intent: "Provide an interface for creating families of related or dependent objects"
        participants:
          - role: "ABSTRACT_FACTORY"
            multiplicity: "1"
          - role: "CONCRETE_FACTORY"
            multiplicity: "1..*"
          - role: "ABSTRACT_PRODUCT"
            multiplicity: "2..*"
          - role: "CONCRETE_PRODUCT"
            multiplicity: "2..*"

  structural:
    description: "Patterns that deal with object composition"
    patterns:
      - name: "Adapter"
        intent: "Convert the interface of a class into another interface clients expect"
        participants:
          - role: "TARGET"
            multiplicity: "1"
          - role: "ADAPTER"
            multiplicity: "1"
          - role: "ADAPTEE"
            multiplicity: "1"
          - role: "CLIENT"
            multiplicity: "1..*"
        
      - name: "Proxy"
        intent: "Provide a surrogate or placeholder for another object to control access to it"
        participants:
          - role: "SUBJECT"
            multiplicity: "1"
          - role: "REAL_SUBJECT"
            multiplicity: "1"
          - role: "PROXY"
            multiplicity: "1"

  behavioral:
    description: "Patterns that deal with object collaboration and responsibilities"
    patterns:
      - name: "Observer"
        intent: "Define a one-to-many dependency between objects so that when one object changes state, all its dependents are notified"
        participants:
          - role: "SUBJECT"
            multiplicity: "1"
            responsibilities:
              - "Attach observers"
              - "Detach observers"
              - "Notify observers"
          - role: "OBSERVER"
            multiplicity: "0..*"
            responsibilities:
              - "Update in response to subject state change"
          - role: "CONCRETE_SUBJECT"
            multiplicity: "1"
            responsibilities:
              - "Store state of interest"
              - "Send notification when state changes"
          - role: "CONCRETE_OBSERVER"
            multiplicity: "0..*"
            responsibilities:
              - "Maintain reference to ConcreteSubject"
              - "Implement update algorithm"
        constraints:
          - "SUBJECT must have attach() and notify() methods"
          - "OBSERVER must have update() method"
          - "ConcreteSubject state changes must trigger notify()"
        
      - name: "Strategy"
        intent: "Define a family of algorithms, encapsulate each one, and make them interchangeable"
        participants:
          - role: "CONTEXT"
            multiplicity: "1"
          - role: "STRATEGY"
            multiplicity: "1"
          - role: "CONCRETE_STRATEGY"
            multiplicity: "1..*"
        
      - name: "Command"
        intent: "Encapsulate a request as an object"
        participants:
          - role: "COMMAND"
            multiplicity: "1"
          - role: "CONCRETE_COMMAND"
            multiplicity: "1..*"
          - role: "INVOKER"
            multiplicity: "1"
          - role: "RECEIVER"
            multiplicity: "1"

# LLM Classification Prompts
classification_prompts:
  observer_detection: |
    Analyze the following architectural elements and determine if they implement the Observer pattern.
    
    Required Evidence:
    1. One element maintaining a list of dependents (SUBJECT role)
    2. One or more elements receiving notifications (OBSERVER role)
    3. Decoupled notification mechanism (observers don't know about each other)
    
    Respond with JSON:
    {
      "pattern_detected": true/false,
      "confidence": 0.0-1.0,
      "role_assignments": {
        "TAG_ID": "SUBJECT" | "OBSERVER" | "CONCRETE_SUBJECT" | "CONCRETE_OBSERVER",
        ...
      },
      "rationale": "Detailed explanation of classification decision"
    }
```

#### 1.2.2 Process Flow Taxonomy

**File:** `schemas/flow_types.yaml`

```yaml
schema_metadata:
  name: "Process Flow Classification Taxonomy"
  version: "1.0.0"
  source: "Enterprise Integration Patterns + Custom Extensions"

flow_topologies:
  sequential:
    description: "Linear execution path with deterministic ordering"
    characteristics:
      - "Single entry point"
      - "Single exit point"
      - "No branching or parallelism"
      - "Steps execute in strict order"
    error_handling_compatible:
      - "Fail-Fast"
      - "Retry with Backoff"
      - "Circuit Breaker"
    diagram_representation: "Activity Diagram (Linear)"
    
  parallel:
    description: "Multiple execution paths proceeding concurrently"
    characteristics:
      - "Fork-Join topology"
      - "Independent subtasks"
      - "Synchronization barrier at completion"
    error_handling_compatible:
      - "Partial Failure Tolerance"
      - "Compensating Transaction"
    diagram_representation: "Activity Diagram (Fork/Join)"
    
  conditional:
    description: "Execution path determined by runtime state evaluation"
    characteristics:
      - "Decision nodes (if/switch)"
      - "Multiple possible paths"
      - "Guard conditions"
    error_handling_compatible:
      - "Exception Handling"
      - "Fallback Strategy"
    diagram_representation: "Activity Diagram (Decision Nodes)"
    
  event_driven:
    description: "Execution triggered by asynchronous events"
    characteristics:
      - "Event producers and consumers"
      - "Message queues or event buses"
      - "Decoupled temporal coordination"
    error_handling_compatible:
      - "Dead Letter Queue"
      - "Idempotent Processing"
      - "Event Replay"
    diagram_representation: "Sequence Diagram + Event Flow"

concurrency_models:
  synchronous:
    description: "Caller blocks waiting for operation completion"
    characteristics:
      - "Request-response coupling"
      - "Deterministic timing"
      - "Simple error propagation"
    
  asynchronous:
    description: "Caller proceeds without waiting"
    characteristics:
      - "Callback or promise-based completion"
      - "Non-blocking execution"
      - "Complex error handling"
    
  reactive:
    description: "Data flow programming with backpressure"
    characteristics:
      - "Observable streams"
      - "Functional transformations"
      - "Backpressure propagation"
```

---

### 1.3 Sphinx Extension Development

**Objective:** Implement custom Sphinx directives and build hooks for assessment layer functionality.

#### 1.3.1 Extension Package Structure

```
extensions/
├── sphinx_assess/
│   ├── __init__.py
│   ├── directives/
│   │   ├── __init__.py
│   │   ├── assess_directive.py      # .. assess:: implementation
│   │   ├── pattern_directive.py     # .. pattern:: implementation
│   │   ├── flow_directive.py        # .. flow:: implementation
│   │   └── validation_directive.py  # .. validation:: implementation
│   ├── analyzers/
│   │   ├── __init__.py
│   │   ├── llm_classifier.py        # LLM API integration
│   │   ├── pattern_matcher.py       # Rule-based pattern detection
│   │   └── flow_analyzer.py         # Process flow topology analysis
│   ├── generators/
│   │   ├── __init__.py
│   │   ├── plantuml_generator.py    # Jinja2 → PlantUML rendering
│   │   ├── graphviz_generator.py    # Graphviz DOT generation
│   │   └── template_loader.py       # Template management
│   ├── validators/
│   │   ├── __init__.py
│   │   ├── pattern_validator.py     # Pattern adherence checking
│   │   ├── constraint_checker.py    # Structural constraint validation
│   │   └── diff_analyzer.py         # Ideal vs. actual comparison
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── needs_query.py           # Sphinx-Needs API wrappers
│   │   ├── cache_manager.py         # Assessment result caching
│   │   └── report_generator.py      # JSON/HTML report generation
│   └── schemas/
│       ├── __init__.py
│       └── schema_loader.py         # YAML schema parsing
└── tests/
    ├── test_directives.py
    ├── test_analyzers.py
    ├── test_generators.py
    └── test_validators.py
```

#### 1.3.2 Core Directive Implementation

**File:** `extensions/sphinx_assess/directives/assess_directive.py`

```python
"""
Assessment Directive Implementation
Triggers LLM-based classification of documentation tags.
"""

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx.util import logging
from typing import List, Dict, Any
import json
import yaml

from ..analyzers.llm_classifier import LLMClassifier
from ..utils.needs_query import get_needs_by_ids
from ..utils.cache_manager import AssessmentCache

logger = logging.getLogger(__name__)


class AssessDirective(Directive):
    """
    Custom Sphinx directive for triggering assessment layer analysis.
    
    Usage:
        .. assess:: PATTERN_CLASSIFICATION_ID
           :scope: SAD-1, SAD-2, SAD-3
           :classification_type: design_pattern
           :schema: gof_behavioral
           :output_enrichment: pattern_role, pattern_name, pattern_confidence
           :diagram_template: templates/observer_pattern.puml.jinja2
           :validation_level: WARNING
    """
    
    required_arguments = 1  # Assessment ID
    optional_arguments = 0
    final_argument_whitespace = False
    
    option_spec = {
        'scope': directives.unchanged_required,           # Comma-separated tag IDs
        'classification_type': directives.unchanged,      # design_pattern | process_flow
        'schema': directives.unchanged_required,          # Schema identifier
        'output_enrichment': directives.unchanged,        # Metadata fields to populate
        'diagram_template': directives.unchanged,         # Path to Jinja2 template
        'validation_level': directives.unchanged,         # ERROR | WARNING | INFO
        'cache_ttl_hours': directives.positive_int,       # Cache duration override
        'llm_model_override': directives.unchanged,       # Model override for this assessment
    }
    
    def run(self) -> List[nodes.Node]:
        """Execute assessment directive processing."""
        env = self.state.document.settings.env
        app = env.app
        
        # Extract directive parameters
        assessment_id = self.arguments[0]
        scope_tags = [tag.strip() for tag in self.options.get('scope', '').split(',')]
        classification_type = self.options.get('classification_type', 'design_pattern')
        schema_name = self.options['schema']
        
        # Retrieve target tags from Sphinx-Needs
        target_needs = get_needs_by_ids(env, scope_tags)
        
        if not target_needs:
            logger.warning(
                f"Assessment {assessment_id}: No valid tags found in scope {scope_tags}",
                location=(env.docname, self.lineno)
            )
            return []
        
        # Initialize LLM classifier
        classifier = LLMClassifier(
            app.config.needs_assessment_config,
            schema_name=schema_name,
            classification_type=classification_type
        )
        
        # Check cache
        cache = AssessmentCache(app.config.needs_assessment_config)
        cache_key = cache.generate_key(assessment_id, target_needs)
        
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.info(f"Assessment {assessment_id}: Using cached results")
            classification_results = cached_result
        else:
            # Perform LLM classification
            logger.info(f"Assessment {assessment_id}: Invoking LLM classifier for {len(target_needs)} tags")
            classification_results = classifier.classify(target_needs)
            
            # Cache results
            cache.set(
                cache_key,
                classification_results,
                ttl_hours=self.options.get('cache_ttl_hours', 168)
            )
        
        # Enrich Sphinx-Needs metadata
        self._enrich_needs_metadata(env, classification_results)
        
        # Generate assessment report node
        report_node = self._create_report_node(
            assessment_id,
            classification_results,
            target_needs
        )
        
        return [report_node]
    
    def _enrich_needs_metadata(
        self,
        env: Any,
        classification_results: Dict[str, Any]
    ) -> None:
        """
        Update Sphinx-Needs internal database with classification metadata.
        
        Parameters
        ----------
        env : sphinx.environment.BuildEnvironment
            Sphinx build environment containing needs data.
        classification_results : Dict[str, Any]
            LLM classification output mapping tag IDs to metadata.
        """
        needs_all_needs = env.needs_all_needs
        
        for tag_id, metadata in classification_results.items():
            if tag_id in needs_all_needs:
                need = needs_all_needs[tag_id]
                
                # Inject pattern metadata
                if 'pattern_name' in metadata:
                    need['pattern_name'] = metadata['pattern_name']
                if 'pattern_role' in metadata:
                    need['pattern_role'] = metadata['pattern_role']
                if 'pattern_confidence' in metadata:
                    need['pattern_confidence'] = metadata['pattern_confidence']
                if 'pattern_rationale' in metadata:
                    need['pattern_rationale'] = metadata['pattern_rationale']
                
                # Record assessment metadata
                need['assessed_by'] = metadata.get('model', 'unknown')
                need['assessment_timestamp'] = metadata.get('timestamp', '')
                
                logger.debug(
                    f"Enriched {tag_id} with pattern metadata: "
                    f"{metadata.get('pattern_name')} / {metadata.get('pattern_role')}"
                )
    
    def _create_report_node(
        self,
        assessment_id: str,
        classification_results: Dict[str, Any],
        target_needs: List[Dict[str, Any]]
    ) -> nodes.Node:
        """
        Create docutils node for assessment report visualization.
        
        Returns
        -------
        nodes.container
            Container node with assessment summary table and metadata.
        """
        # Create container node
        container = nodes.container()
        container['classes'].append('assessment-report')
        
        # Add title
        title = nodes.title(text=f"Assessment Report: {assessment_id}")
        container += title
        
        # Create summary table
        table = self._build_summary_table(classification_results, target_needs)
        container += table
        
        # Add metadata paragraph
        metadata_para = nodes.paragraph()
        metadata_para += nodes.Text(
            f"Classified {len(classification_results)} tags using "
            f"{classification_results.get('_meta', {}).get('model', 'unknown')} "
            f"at {classification_results.get('_meta', {}).get('timestamp', 'unknown')}"
        )
        container += metadata_para
        
        return container
    
    def _build_summary_table(
        self,
        results: Dict[str, Any],
        needs: List[Dict[str, Any]]
    ) -> nodes.table:
        """Build HTML table summarizing classification results."""
        # Implementation details for table generation
        # (Standard docutils table construction)
        pass


def setup(app):
    """Sphinx extension setup function."""
    app.add_directive('assess', AssessDirective)
    
    return {
        'version': '1.0.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
```

#### 1.3.3 LLM Classifier Implementation

**File:** `extensions/sphinx_assess/analyzers/llm_classifier.py`

```python
"""
LLM-based pattern classification engine.
Supports multiple providers (OpenAI, Anthropic, Google).
"""

import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import yaml

# Provider-specific imports
try:
    import openai
except ImportError:
    openai = None

try:
    import anthropic
except ImportError:
    anthropic = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None


logger = logging.getLogger(__name__)


class LLMClassifier:
    """
    Multi-provider LLM classification engine for architectural pattern detection.
    
    Parameters
    ----------
    config : Dict[str, Any]
        Assessment configuration from Sphinx conf.py.
    schema_name : str
        Pattern schema identifier (e.g., 'gof_behavioral').
    classification_type : str
        Type of classification ('design_pattern' | 'process_flow').
    
    Attributes
    ----------
    provider : str
        LLM provider identifier.
    model : str
        Model identifier for API calls.
    schema : Dict[str, Any]
        Loaded pattern schema definitions.
    """
    
    def __init__(
        self,
        config: Dict[str, Any],
        schema_name: str,
        classification_type: str = 'design_pattern'
    ):
        self.config = config
        self.schema_name = schema_name
        self.classification_type = classification_type
        
        # Initialize provider
        self.provider = config.get('llm_provider', 'openai')
        self.model = config.get('llm_model')
        self.temperature = config.get('llm_temperature', 0.1)
        self.max_tokens = config.get('llm_max_tokens', 4096)
        
        # Load classification schema
        self.schema = self._load_schema(schema_name)
        
        # Initialize API client
        self._init_client()
    
    def _load_schema(self, schema_name: str) -> Dict[str, Any]:
        """Load pattern schema from YAML library."""
        schema_map = {
            'gof_behavioral': 'schemas/gof_patterns.yaml',
            'gof_structural': 'schemas/gof_patterns.yaml',
            'gof_creational': 'schemas/gof_patterns.yaml',
            'flow_topologies': 'schemas/flow_types.yaml',
        }
        
        schema_path = schema_map.get(schema_name)
        if not schema_path:
            raise ValueError(f"Unknown schema: {schema_name}")
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            full_schema = yaml.safe_load(f)
        
        # Extract relevant category
        if 'gof' in schema_name:
            category = schema_name.split('_')[1]  # behavioral | structural | creational
            return full_schema['categories'][category]
        elif 'flow' in schema_name:
            return full_schema['flow_topologies']
        
        return full_schema
    
    def _init_client(self) -> None:
        """Initialize provider-specific API client."""
        if self.provider == 'openai':
            if openai is None:
                raise ImportError("OpenAI package not installed")
            self.client = openai.OpenAI()
        
        elif self.provider == 'anthropic':
            if anthropic is None:
                raise ImportError("Anthropic package not installed")
            self.client = anthropic.Anthropic()
        
        elif self.provider == 'google':
            if genai is None:
                raise ImportError("Google GenerativeAI package not installed")
            genai.configure()
            self.client = genai.GenerativeModel(self.model)
        
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def classify(self, needs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Classify a list of Sphinx-Needs tags into pattern roles.
        
        Parameters
        ----------
        needs : List[Dict[str, Any]]
            List of Sphinx-Needs objects to classify.
        
        Returns
        -------
        Dict[str, Any]
            Mapping of tag IDs to classification metadata:
            {
                "TAG_ID": {
                    "pattern_name": "Observer",
                    "pattern_role": "SUBJECT",
                    "pattern_confidence": 0.92,
                    "pattern_rationale": "Element maintains observer list..."
                },
                "_meta": {
                    "model": "gpt-4-turbo-2024-04-09",
                    "timestamp": "2024-01-15T14:32:00Z",
                    "schema": "gof_behavioral"
                }
            }
        """
        # Build classification prompt
        prompt = self._build_classification_prompt(needs)
        
        # Execute LLM API call
        if self.provider == 'openai':
            response = self._classify_openai(prompt)
        elif self.provider == 'anthropic':
            response = self._classify_anthropic(prompt)
        elif self.provider == 'google':
            response = self._classify_google(prompt)
        
        # Parse and validate response
        try:
            parsed = json.loads(response)
            validated = self._validate_classification_response(parsed, needs)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            logger.debug(f"Raw response: {response}")
            raise
        
        # Add metadata
        validated['_meta'] = {
            'model': self.model,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'schema': self.schema_name,
            'provider': self.provider
        }
        
        return validated
    
    def _build_classification_prompt(self, needs: List[Dict[str, Any]]) -> str:
        """
        Construct LLM prompt for pattern classification.
        
        Prompt Engineering Strategy
        ---------------------------
        1. Provide schema definitions (pattern intent, participants, constraints)
        2. Present target tags with full context (title, description, relationships)
        3. Request structured JSON output with confidence scores
        4. Include few-shot examples for calibration
        """
        # Extract pattern definitions from schema
        pattern_definitions = self._format_pattern_definitions()
        
        # Format target tags
        tag_descriptions = self._format_needs_for_prompt(needs)
        
        # Load classification prompt template from schema
        prompt_template = self.schema.get(
            'classification_prompts',
            {}
        ).get(f'{self.classification_type}_detection', '')
        
        # Construct full prompt
        prompt = f"""You are an expert software architect analyzing documentation tags to identify design patterns.

## Pattern Library
{pattern_definitions}

## Tags to Classify
```python
## Tags to Classify
{tag_descriptions}

## Task
Analyze the provided tags and classify them according to the pattern definitions above.

For each tag, determine:
1. Which pattern (if any) it participates in
2. What role it plays in that pattern
3. Your confidence level (0.0-1.0)
4. Justification for the classification

## Output Format
Respond with ONLY a valid JSON object (no markdown, no preamble):

{{
  "TAG_ID_1": {{
    "pattern_name": "Observer" | "Strategy" | "Singleton" | etc. | null,
    "pattern_role": "SUBJECT" | "OBSERVER" | "CONTEXT" | etc. | null,
    "pattern_confidence": 0.0-1.0,
    "pattern_rationale": "Detailed explanation of why this classification was made",
    "alternative_interpretations": [
      {{"pattern": "Alternative Pattern", "confidence": 0.0-1.0, "reason": "..."}}
    ]
  }},
  "TAG_ID_2": {{ ... }},
  ...
}}

## Classification Rules
- If a tag doesn't clearly fit any pattern, set pattern_name and pattern_role to null
- Confidence < 0.5 indicates uncertain classification (consider null instead)
- Provide specific evidence from tag descriptions in rationale
- Consider structural relationships (links between tags) as primary evidence
- If multiple patterns could apply, choose the one with highest confidence
- Document alternative interpretations for ambiguous cases

{prompt_template}
"""
        
        return prompt
    
    def _format_pattern_definitions(self) -> str:
        """Format schema pattern definitions for prompt inclusion."""
        definitions = []
        
        if self.classification_type == 'design_pattern':
            for pattern in self.schema.get('patterns', []):
                definition = f"""
### {pattern['name']}
**Intent:** {pattern['intent']}

**Participants:**
"""
                for participant in pattern.get('participants', []):
                    definition += f"- {participant['role']} (multiplicity: {participant['multiplicity']})\n"
                    if 'responsibilities' in participant:
                        for resp in participant['responsibilities']:
                            definition += f"  - {resp}\n"
                
                if 'constraints' in pattern:
                    definition += "\n**Constraints:**\n"
                    for constraint in pattern['constraints']:
                        definition += f"- {constraint}\n"
                
                definitions.append(definition)
        
        elif self.classification_type == 'process_flow':
            for flow_type, flow_def in self.schema.items():
                definition = f"""
### {flow_type.upper()}
**Description:** {flow_def['description']}

**Characteristics:**
"""
                for char in flow_def.get('characteristics', []):
                    definition += f"- {char}\n"
                
                definitions.append(definition)
        
        return "\n".join(definitions)
    
    def _format_needs_for_prompt(self, needs: List[Dict[str, Any]]) -> str:
        """Format Sphinx-Needs objects for LLM consumption."""
        formatted = []
        
        for need in needs:
            tag_info = f"""
**Tag ID:** {need['id']}
**Title:** {need.get('title', 'Untitled')}
**Type:** {need.get('type', 'unknown')}
**Description:**
{need.get('description', need.get('content', 'No description available'))}

**Relationships:**
"""
            # Include traceability links
            if need.get('links'):
                for link_type, linked_ids in need['links'].items():
                    if linked_ids:
                        tag_info += f"- {link_type}: {', '.join(linked_ids)}\n"
            
            # Include any existing metadata that might be relevant
            if need.get('docname'):
                tag_info += f"**Source Document:** {need['docname']}\n"
            
            formatted.append(tag_info)
        
        return "\n---\n".join(formatted)
    
    def _classify_openai(self, prompt: str) -> str:
        """Execute classification using OpenAI API."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert software architect specializing in design pattern recognition. You analyze documentation and provide precise, evidence-based pattern classifications in valid JSON format."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            response_format={"type": "json_object"}  # Enforce JSON output
        )
        
        return response.choices[0].message.content
    
    def _classify_anthropic(self, prompt: str) -> str:
        """Execute classification using Anthropic API."""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system="You are an expert software architect specializing in design pattern recognition. Respond only with valid JSON.",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        return response.content[0].text
    
    def _classify_google(self, prompt: str) -> str:
        """Execute classification using Google Gemini API."""
        response = self.client.generate_content(
            prompt,
            generation_config={
                "temperature": self.temperature,
                "max_output_tokens": self.max_tokens,
            }
        )
        
        return response.text
    
    def _validate_classification_response(
        self,
        parsed: Dict[str, Any],
        needs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Validate LLM classification response structure and content.
        
        Validation Rules
        ----------------
        1. Response must be a dictionary
        2. Each key must match a tag ID from input needs
        3. Each value must contain required fields
        4. Confidence scores must be 0.0-1.0
        5. Pattern names must exist in schema (if not null)
        6. Pattern roles must be valid for assigned pattern
        """
        validated = {}
        need_ids = {need['id'] for need in needs}
        
        for tag_id, classification in parsed.items():
            # Skip metadata keys
            if tag_id.startswith('_'):
                continue
            
            # Validate tag ID exists in input
            if tag_id not in need_ids:
                logger.warning(f"LLM returned classification for unknown tag: {tag_id}")
                continue
            
            # Validate required fields
            required_fields = ['pattern_name', 'pattern_role', 'pattern_confidence', 'pattern_rationale']
            if not all(field in classification for field in required_fields):
                logger.error(f"Missing required fields in classification for {tag_id}")
                continue
            
            # Validate confidence score
            confidence = classification['pattern_confidence']
            if not isinstance(confidence, (int, float)) or not 0.0 <= confidence <= 1.0:
                logger.warning(f"Invalid confidence score for {tag_id}: {confidence}")
                classification['pattern_confidence'] = 0.0
            
            # Validate pattern name against schema
            pattern_name = classification['pattern_name']
            if pattern_name is not None:
                valid_patterns = [p['name'] for p in self.schema.get('patterns', [])]
                if pattern_name not in valid_patterns:
                    logger.warning(
                        f"LLM assigned unknown pattern '{pattern_name}' to {tag_id}. "
                        f"Valid patterns: {valid_patterns}"
                    )
            
            # Validate pattern role
            pattern_role = classification['pattern_role']
            if pattern_role is not None and pattern_name is not None:
                pattern_def = next(
                    (p for p in self.schema.get('patterns', []) if p['name'] == pattern_name),
                    None
                )
                if pattern_def:
                    valid_roles = [p['role'] for p in pattern_def.get('participants', [])]
                    if pattern_role not in valid_roles:
                        logger.warning(
                            f"Invalid role '{pattern_role}' for pattern '{pattern_name}' on {tag_id}. "
                            f"Valid roles: {valid_roles}"
                        )
            
            validated[tag_id] = classification
        
        # Warn if LLM didn't classify all tags
        missing_tags = need_ids - set(validated.keys())
        if missing_tags:
            logger.warning(f"LLM did not classify tags: {missing_tags}")
        
        return validated


class PatternConstraintValidator:
    """
    Validates that classified tags satisfy pattern structural constraints.
    
    Example: Observer pattern requires exactly 1 SUBJECT and 1+ OBSERVERS.
    """
    
    def __init__(self, schema: Dict[str, Any]):
        self.schema = schema
    
    def validate(self, classifications: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Check if tag classifications satisfy pattern multiplicity constraints.
        
        Returns
        -------
        List[Dict[str, Any]]
            List of constraint violations:
            [
                {
                    "pattern": "Observer",
                    "violation_type": "MULTIPLICITY",
                    "constraint": "Requires exactly 1 SUBJECT",
                    "actual": "Found 0 SUBJECT roles",
                    "severity": "ERROR"
                }
            ]
        """
        violations = []
        
        # Group classifications by pattern
        pattern_groups = {}
        for tag_id, metadata in classifications.items():
            if tag_id.startswith('_'):
                continue
            
            pattern_name = metadata.get('pattern_name')
            if pattern_name:
                if pattern_name not in pattern_groups:
                    pattern_groups[pattern_name] = []
                pattern_groups[pattern_name].append({
                    'tag_id': tag_id,
                    'role': metadata.get('pattern_role')
                })
        
        # Validate each pattern group
        for pattern_name, tags in pattern_groups.items():
            pattern_def = next(
                (p for p in self.schema.get('patterns', []) if p['name'] == pattern_name),
                None
            )
            
            if not pattern_def:
                continue
            
            # Check multiplicity constraints
            for participant in pattern_def.get('participants', []):
                role = participant['role']
                multiplicity = participant['multiplicity']
                
                role_count = sum(1 for t in tags if t['role'] == role)
                
                # Parse multiplicity constraints
                if multiplicity == '1':
                    if role_count != 1:
                        violations.append({
                            'pattern': pattern_name,
                            'violation_type': 'MULTIPLICITY',
                            'constraint': f"Requires exactly 1 {role}",
                            'actual': f"Found {role_count} {role} roles",
                            'severity': 'ERROR',
                            'tags_involved': [t['tag_id'] for t in tags if t['role'] == role]
                        })
                
                elif multiplicity == '0..*' or multiplicity == '1..*':
                    min_required = 0 if multiplicity.startswith('0') else 1
                    if role_count < min_required:
                        violations.append({
                            'pattern': pattern_name,
                            'violation_type': 'MULTIPLICITY',
                            'constraint': f"Requires at least {min_required} {role}",
                            'actual': f"Found {role_count} {role} roles",
                            'severity': 'WARNING' if min_required == 0 else 'ERROR',
                            'tags_involved': [t['tag_id'] for t in tags if t['role'] == role]
                        })
        
        return violations
```

---

## Phase 2: Graphviz Integration for Metadata Visualization (60 hours)

### 2.1 Graphviz Generator Architecture

**Objective:** Create comprehensive tag relationship and traceability visualizations using Graphviz DOT language.

#### 2.1.1 Core Generator Implementation

**File:** `extensions/sphinx_assess/generators/graphviz_generator.py`

```python
"""
Graphviz DOT graph generation for tag traceability and pattern visualization.
Supports multiple layout algorithms and visual encoding strategies.
"""

import logging
from typing import Dict, List, Any, Optional, Set, Tuple
from pathlib import Path
import subprocess
import hashlib

logger = logging.getLogger(__name__)


class GraphvizGenerator:
    """
    Generate Graphviz DOT graphs from Sphinx-Needs metadata.
    
    Parameters
    ----------
    config : Dict[str, Any]
        Assessment configuration containing Graphviz settings.
    output_dir : Path
        Directory for generated graph files.
    
    Capabilities
    ------------
    - Traceability matrices (tag dependencies)
    - Pattern participation graphs (tags grouped by pattern)
    - Hierarchical documentation structure
    - Violation highlighting
    - Multi-layer filtering
    """
    
    def __init__(self, config: Dict[str, Any], output_dir: Path):
        self.config = config
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.engine = config.get('graphviz_engine', 'dot')
        self.output_format = config.get('plantuml_output_format', 'svg')
        
        # Visual encoding configuration
        self.colors = {
            'BRD': '#E8F4F8',     # Business Requirements - Light Blue
            'NFR': '#FFF4E6',     # Constraints - Light Orange
            'FSD': '#E8F5E9',     # Features - Light Green
            'SAD': '#F3E5F5',     # Architecture - Light Purple
            'ICD': '#FFF9C4',     # Interfaces - Light Yellow
            'TDD': '#FFE0B2',     # Technical Design - Light Amber
            'ISP': '#FFCCBC',     # Implementation - Light Deep Orange
            'PATTERN': '#D1C4E9', # Pattern nodes - Medium Purple
            'FLOW': '#B3E5FC',    # Flow nodes - Light Cyan
            'VIOLATION': '#FFCDD2'# Violations - Light Red
        }
        
        self.shapes = {
            'requirement': 'box',
            'specification': 'box',
            'implementation': 'component',
            'pattern': 'hexagon',
            'flow': 'diamond',
            'validation': 'octagon'
        }
    
    def generate_traceability_matrix(
        self,
        needs: List[Dict[str, Any]],
        output_filename: str,
        filter_layers: Optional[List[str]] = None,
        show_assessments: bool = True
    ) -> Path:
        """
        Generate comprehensive traceability graph showing tag dependencies.
        
        Parameters
        ----------
        needs : List[Dict[str, Any]]
            All Sphinx-Needs objects to include.
        output_filename : str
            Base filename (without extension).
        filter_layers : Optional[List[str]]
            Restrict to specific documentation layers (e.g., ['BRD', 'FSD', 'SAD']).
        show_assessments : bool
            Include pattern/flow assessment nodes.
        
        Returns
        -------
        Path
            Path to generated SVG/PNG file.
        
        Graph Structure
        ---------------
        - Nodes: Documentation tags (colored by layer)
        - Edges: Traceability links (satisfies, assessed_by, constrains, etc.)
        - Clusters: Group by documentation layer
        - Annotations: Pattern roles, confidence scores
        """
        # Filter needs by layer if specified
        if filter_layers:
            needs = [n for n in needs if any(n['id'].startswith(layer) for layer in filter_layers)]
        
        # Build DOT graph
        dot = self._init_graph("Traceability Matrix")
        
        # Create subgraphs for each documentation layer
        layer_groups = self._group_by_layer(needs)
        
        for layer_name, layer_needs in sorted(layer_groups.items()):
            with self._subgraph(dot, f"cluster_{layer_name}", layer_name):
                for need in layer_needs:
                    self._add_need_node(dot, need, show_pattern_role=show_assessments)
        
        # Add traceability edges
        self._add_traceability_edges(dot, needs)
        
        # Add assessment nodes and edges if requested
        if show_assessments:
            self._add_assessment_annotations(dot, needs)
        
        # Render graph
        output_path = self._render_graph(dot, output_filename)
        
        return output_path
    
    def generate_pattern_participation_graph(
        self,
        needs: List[Dict[str, Any]],
        pattern_name: str,
        output_filename: str
    ) -> Path:
        """
        Generate pattern-centric visualization showing all participants.
        
        Parameters
        ----------
        needs : List[Dict[str, Any]]
            Sphinx-Needs objects classified for this pattern.
        pattern_name : str
            Name of pattern to visualize (e.g., "Observer").
        output_filename : str
            Base filename for output.
        
        Returns
        -------
        Path
            Path to generated diagram.
        
        Graph Structure
        ---------------
        - Central pattern node (large hexagon)
        - Participant nodes grouped by role
        - Relationship edges showing collaborations
        - Confidence score annotations
        """
        # Filter to tags participating in this pattern
        participants = [
            n for n in needs
            if n.get('pattern_name') == pattern_name
        ]
        
        if not participants:
            logger.warning(f"No participants found for pattern: {pattern_name}")
            return None
        
        dot = self._init_graph(f"{pattern_name} Pattern Participation")
        
        # Add central pattern node
        dot.append(f'  "PATTERN_{pattern_name}" [')
        dot.append(f'    label="{pattern_name}\\nDesign Pattern",')
        dot.append(f'    shape=hexagon,')
        dot.append(f'    style=filled,')
        dot.append(f'    fillcolor="{self.colors["PATTERN"]}",')
        dot.append(f'    fontsize=16,')
        dot.append(f'    fontname="Arial Bold"')
        dot.append(f'  ];')
        
        # Group participants by role
        role_groups = {}
        for participant in participants:
            role = participant.get('pattern_role', 'UNKNOWN')
            if role not in role_groups:
                role_groups[role] = []
            role_groups[role].append(participant)
        
        # Create subgraph for each role
        for role, role_participants in role_groups.items():
            with self._subgraph(dot, f"cluster_role_{role}", f"Role: {role}"):
                for participant in role_participants:
                    self._add_need_node(
                        dot,
                        participant,
                        show_pattern_role=False,  # Already in cluster label
                        show_confidence=True
                    )
                    
                    # Connect to central pattern node
                    confidence = participant.get('pattern_confidence', 0.0)
                    edge_style = "solid" if confidence > 0.7 else "dashed"
                    edge_color = "#27AE60" if confidence > 0.7 else "#E67E22"
                    
                    dot.append(f'  "PATTERN_{pattern_name}" -> "{participant["id"]}" [')
                    dot.append(f'    label="{role}\\n({confidence:.2f})",')
                    dot.append(f'    style={edge_style},')
                    dot.append(f'    color="{edge_color}"')
                    dot.append(f'  ];')
        
        output_path = self._render_graph(dot, output_filename)
        return output_path
    
    def generate_hierarchical_structure(
        self,
        needs: List[Dict[str, Any]],
        output_filename: str,
        root_layer: str = 'BRD'
    ) -> Path:
        """
        Generate top-down hierarchical view of documentation structure.
        
        Parameters
        ----------
        needs : List[Dict[str, Any]]
            All needs to visualize.
        output_filename : str
            Output filename.
        root_layer : str
            Top-level layer to start hierarchy (default: BRD).
        
        Returns
        -------
        Path
            Path to generated diagram.
        
        Graph Structure
        ---------------
        Uses 'dot' engine for strict top-down hierarchy.
        Layers arranged vertically: BRD → NFR → FSD → SAD → ICD → TDD → ISP
        """
        dot = self._init_graph("Documentation Hierarchy", engine='dot', rankdir='TB')
        
        # Define layer ordering
        layer_order = ['BRD', 'NFR', 'FSD', 'SAD', 'ICD', 'TDD', 'ISP']
        
        # Create ranked subgraphs for each layer
        for rank, layer in enumerate(layer_order):
            layer_needs = [n for n in needs if n['id'].startswith(layer)]
            
            if not layer_needs:
                continue
            
            dot.append(f'  {{ rank=same;')
            
            for need in layer_needs:
                self._add_need_node(dot, need, compact=True)
            
            dot.append(f'  }}')
        
        # Add hierarchical edges (parent-child relationships)
        for need in needs:
            if 'links' in need:
                for link_type, linked_ids in need['links'].items():
                    if link_type in ['satisfies', 'refines', 'derives_from']:
                        for linked_id in linked_ids:
                            dot.append(f'  "{linked_id}" -> "{need["id"]}" [')
                            dot.append(f'    label="{link_type}",')
                            dot.append(f'    fontsize=8')
                            dot.append(f'  ];')
        
        output_path = self._render_graph(dot, output_filename)
        return output_path
    
    def generate_violation_heatmap(
        self,
        needs: List[Dict[str, Any]],
        violations: List[Dict[str, Any]],
        output_filename: str
    ) -> Path:
        """
        Generate graph highlighting pattern constraint violations.
        
        Parameters
        ----------
        needs : List[Dict[str, Any]]
            All needs.
        violations : List[Dict[str, Any]]
            Validation violations from PatternConstraintValidator.
        output_filename : str
            Output filename.
        
        Returns
        -------
        Path
            Path to generated heatmap.
        
        Visual Encoding
        ---------------
        - Violated tags: Red fill color
        - Severity levels: Border thickness (ERROR=3, WARNING=2, INFO=1)
        - Violation count: Node label annotation
        """
        dot = self._init_graph("Pattern Violation Heatmap")
        
        # Build violation index
        violation_index = {}
        for violation in violations:
            for tag_id in violation.get('tags_involved', []):
                if tag_id not in violation_index:
                    violation_index[tag_id] = []
                violation_index[tag_id].append(violation)
        
        # Add nodes with violation coloring
        for need in needs:
            tag_violations = violation_index.get(need['id'], [])
            violation_count = len(tag_violations)
            
            # Determine fill color and border
            if violation_count == 0:
                fillcolor = self.colors.get(need['id'].split('-')[0], '#FFFFFF')
                penwidth = 1
            else:
                fillcolor = self.colors['VIOLATION']
                max_severity = max(
                    (3 if v['severity'] == 'ERROR' else 2 if v['severity'] == 'WARNING' else 1)
                    for v in tag_violations
                )
                penwidth = max_severity
            
            label = f"{need['id']}"
            if violation_count > 0:
                label += f"\\n⚠ {violation_count} violations"
            
            dot.append(f'  "{need["id"]}" [')
            dot.append(f'    label="{label}",')
            dot.append(f'    shape=box,')
            dot.append(f'    style=filled,')
            dot.append(f'    fillcolor="{fillcolor}",')
            dot.append(f'    penwidth={penwidth}')
            dot.append(f'  ];')
        
        # Add edges
        self._add_traceability_edges(dot, needs)
        
        output_path = self._render_graph(dot, output_filename)
        return output_path
    
    # ========== Private Helper Methods ==========
    
    def _init_graph(
        self,
        title: str,
        engine: Optional[str] = None,
        rankdir: str = 'LR'
    ) -> List[str]:
        """Initialize DOT graph with standard preamble."""
        engine = engine or self.engine
        
        dot = [
            f'digraph "{title}" {{',
            f'  label="{title}";',
            f'  labelloc="t";',
            f'  fontsize=20;',
            f'  fontname="Arial Bold";',
            f'  rankdir={rankdir};',
            f'  node [fontname="Arial", fontsize=10];',
            f'  edge [fontname="Arial", fontsize=8];',
            ''
        ]
        
        return dot
    
    def _subgraph(self, dot: List[str], cluster_id: str, label: str):
        """Context manager for creating subgraphs."""
        class SubgraphContext:
            def __init__(self, dot_lines, cid, lbl):
                self.dot = dot_lines
                self.cluster_id = cid
                self.label = lbl
            
            def __enter__(self):
                self.dot.append(f'  subgraph {self.cluster_id} {{')
                self.dot.append(f'    label="{self.label}";')
                self.dot.append(f'    style=filled;')
                self.dot.append(f'    color=lightgrey;')
                return self
            
            def __exit__(self, *args):
                self.dot.append(f'  }}')
        
        return SubgraphContext(dot, cluster_id, label)
    
    def _add_need_node(
        self,
        dot: List[str],
        need: Dict[str, Any],
        show_pattern_role: bool = True,
        show_confidence: bool = False,
        compact: bool = False
    ) -> None:
        """Add Sphinx-Needs node to DOT graph."""
        node_id = need['id']
        label_parts = [node_id]
        
        if not compact:
            title = need.get('title', '')
            if title and len(title) < 50:
                label_parts.append(title)
        
        if show_pattern_role and need.get('pattern_role'):
            label_parts.append(f"[{need['pattern_role']}]")
        
        if show_confidence and need.get('pattern_confidence'):
            confidence = need['pattern_confidence']
            label_parts.append(f"conf: {confidence:.2f}")
        
        label = "\\n".join(label_parts)
        
        # Determine node color from layer
        layer_prefix = node_id.split('-')[0]
        fillcolor = self.colors.get(layer_prefix, '#FFFFFF')
        
        # Determine shape from type
        shape = self.shapes.get(need.get('type', 'requirement'), 'box')
        
        dot.append(f'  "{node_id}" [')
        dot.append(f'    label="{label}",')
        dot.append(f'    shape={shape},')
        dot.append(f'    style=filled,')
        dot.append(f'    fillcolor="{fillcolor}"')
        dot.append(f'  ];')
    
    def _add_traceability_edges(
        self,
        dot: List[str],
        needs: List[Dict[str, Any]]
    ) -> None:
        """Add edges representing traceability links."""
        edge_styles = {
            'satisfies': ('solid', '#2C3E50'),
            'refines': ('dashed', '#7F8C8D'),
            'assessed_by': ('dotted', '#9B59B6'),
            'constrains': ('bold', '#E74C3C'),
            'validates': ('solid', '#F39C12'),
            'implements_pattern': ('dashed', '#3498DB')
        }
        
        for need in needs:
            if 'links' not in need:
                continue
            
            for link_type, linked_ids in need['links'].items():
                if not linked_ids:
                    continue
                
                style, color = edge_styles.get(link_type, ('solid', '#95A5A6'))
                
                for linked_id in linked_ids:
                    dot.append(f'  "{need["id"]}" -> "{linked_id}" [')
                    dot.append(f'    label="{link_type}",')
                    dot.append(f'    style={style},')
                    dot.append(f'    color="{color}"')
                    dot.append(f'  ];')
    
    def _add_assessment_annotations(
        self,
        dot: List[str],
        needs: List[Dict[str, Any]]
    ) -> None:
        """Add pattern/flow assessment annotation nodes."""
        # Group needs by pattern
        pattern_groups = {}
        for need in needs:
            pattern_name = need.get('pattern_name')
            if pattern_name:
                if pattern_name not in pattern_groups:
                    pattern_groups[pattern_name] = []
                pattern_groups[pattern_name].append(need['id'])
        
        # Add pattern annotation nodes
        for pattern_name, participant_ids in pattern_groups.items():
            annotation_id = f"PATTERN_ANNO_{pattern_name}"
            
            dot.append(f'  "{annotation_id}" [')
            dot.append(f'    label="Pattern: {pattern_name}",')
            dot.append(f'    shape=note,')
            dot.append(f'    style=filled,')
            dot.append(f'    fillcolor="{self.colors["PATTERN"]}"')
            dot.append(f'  ];')
            
            # Connect to all participants
            for participant_id in participant_ids:
                dot.append(f'  "{annotation_id}" -> "{participant_id}" [')
                dot.append(f'    style=dotted,')
                dot.append(f'    arrowhead=none,')
                dot.append(f'    color="#9B59B6"')
                dot.append(f'  ];')
    
    def _group_by_layer(
        self,
        needs: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Group needs by documentation layer prefix."""
        groups = {}
        
        for need in needs:
            layer = need['id'].split('-')[0]
            if layer not in groups:
                groups[layer] = []
            groups[layer].append(need)
        
        return groups
    
    def _render_graph(
        self,
        dot_lines: List[str],
        output_filename: str
    ) -> Path:
        """
        Render DOT graph to output format using Graphviz CLI.
        
        Parameters
        ----------
        dot_lines : List[str]
            DOT language graph definition.
```python
        output_filename : str
            Base filename without extension.
        
        Returns
        -------
        Path
            Path to generated output file.
        """
        # Close graph definition
        dot_lines.append('}')
        dot_content = '\n'.join(dot_lines)
        
        # Generate hash-based cache key
        content_hash = hashlib.md5(dot_content.encode()).hexdigest()[:8]
        
        # Define file paths
        dot_file = self.output_dir / f"{output_filename}_{content_hash}.dot"
        output_file = self.output_dir / f"{output_filename}_{content_hash}.{self.output_format}"
        
        # Check if already rendered (caching)
        if output_file.exists():
            logger.debug(f"Using cached Graphviz output: {output_file}")
            return output_file
        
        # Write DOT file
        dot_file.write_text(dot_content, encoding='utf-8')
        logger.debug(f"Generated DOT file: {dot_file}")
        
        # Execute Graphviz rendering
        try:
            cmd = [
                self.engine,
                f"-T{self.output_format}",
                str(dot_file),
                "-o", str(output_file)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                logger.error(f"Graphviz rendering failed: {result.stderr}")
                raise RuntimeError(f"Graphviz error: {result.stderr}")
            
            logger.info(f"Generated Graphviz diagram: {output_file}")
            return output_file
        
        except subprocess.TimeoutExpired:
            logger.error(f"Graphviz rendering timed out for {dot_file}")
            raise
        
        except FileNotFoundError:
            logger.error(
                f"Graphviz '{self.engine}' executable not found. "
                "Ensure Graphviz is installed and in PATH."
            )
            raise


class GraphvizNeedflowIntegration:
    """
    Integration layer between Graphviz generator and Sphinx-Needs needflow directive.
    Enables seamless diagram generation from Sphinx documentation.
    """
    
    @staticmethod
    def create_custom_needflow(
        app,
        needs: List[Dict[str, Any]],
        filter_func: Optional[callable] = None,
        visualization_type: str = 'traceability',
        **kwargs
    ) -> Path:
        """
        Custom needflow implementation using GraphvizGenerator.
        
        Parameters
        ----------
        app : sphinx.application.Sphinx
            Sphinx application instance.
        needs : List[Dict[str, Any]]
            Needs to visualize.
        filter_func : Optional[callable]
            Filter function to apply to needs.
        visualization_type : str
            Type of visualization: 'traceability' | 'pattern' | 'hierarchy' | 'violations'
        **kwargs
            Additional arguments passed to specific generator methods.
        
        Returns
        -------
        Path
            Path to generated diagram file.
        """
        # Apply filter if provided
        if filter_func:
            needs = [n for n in needs if filter_func(n)]
        
        # Initialize generator
        config = app.config.needs_assessment_config
        output_dir = Path(app.outdir) / '_images' / 'graphviz'
        generator = GraphvizGenerator(config, output_dir)
        
        # Generate appropriate visualization
        if visualization_type == 'traceability':
            return generator.generate_traceability_matrix(
                needs,
                output_filename=kwargs.get('output_filename', 'traceability'),
                filter_layers=kwargs.get('filter_layers'),
                show_assessments=kwargs.get('show_assessments', True)
            )
        
        elif visualization_type == 'pattern':
            pattern_name = kwargs.get('pattern_name')
            if not pattern_name:
                raise ValueError("pattern_name required for pattern visualization")
            
            return generator.generate_pattern_participation_graph(
                needs,
                pattern_name=pattern_name,
                output_filename=kwargs.get('output_filename', f'pattern_{pattern_name}')
            )
        
        elif visualization_type == 'hierarchy':
            return generator.generate_hierarchical_structure(
                needs,
                output_filename=kwargs.get('output_filename', 'hierarchy'),
                root_layer=kwargs.get('root_layer', 'BRD')
            )
        
        elif visualization_type == 'violations':
            violations = kwargs.get('violations', [])
            return generator.generate_violation_heatmap(
                needs,
                violations=violations,
                output_filename=kwargs.get('output_filename', 'violations')
            )
        
        else:
            raise ValueError(f"Unknown visualization_type: {visualization_type}")


class GraphvizDirective(Directive):
    """
    Custom Sphinx directive for inline Graphviz diagram generation.
    
    Usage:
        .. graphviz_assess:: traceability
           :scope: SAD-1, SAD-2, SAD-3, TDD-1, TDD-2
           :filter_layers: SAD, TDD
           :show_assessments: true
           :output_filename: sad_tdd_traceability
    """
    
    required_arguments = 1  # visualization_type
    optional_arguments = 0
    
    option_spec = {
        'scope': directives.unchanged,
        'filter_layers': directives.unchanged,
        'show_assessments': directives.flag,
        'pattern_name': directives.unchanged,
        'root_layer': directives.unchanged,
        'output_filename': directives.unchanged,
        'width': directives.unchanged,
        'height': directives.unchanged,
        'align': directives.unchanged,
    }
    
    def run(self) -> List[nodes.Node]:
        """Execute Graphviz generation and embed in document."""
        env = self.state.document.settings.env
        app = env.app
        
        visualization_type = self.arguments[0]
        
        # Parse scope tags
        scope_tags = []
        if 'scope' in self.options:
            scope_tags = [tag.strip() for tag in self.options['scope'].split(',')]
        
        # Retrieve needs
        from ..utils.needs_query import get_needs_by_ids
        needs = get_needs_by_ids(env, scope_tags) if scope_tags else list(env.needs_all_needs.values())
        
        # Parse filter layers
        filter_layers = None
        if 'filter_layers' in self.options:
            filter_layers = [layer.strip() for layer in self.options['filter_layers'].split(',')]
        
        # Generate diagram
        kwargs = {
            'output_filename': self.options.get('output_filename', 'graphviz_diagram'),
            'filter_layers': filter_layers,
            'show_assessments': 'show_assessments' in self.options,
            'pattern_name': self.options.get('pattern_name'),
            'root_layer': self.options.get('root_layer', 'BRD')
        }
        
        try:
            diagram_path = GraphvizNeedflowIntegration.create_custom_needflow(
                app,
                needs,
                visualization_type=visualization_type,
                **kwargs
            )
        except Exception as e:
            logger.error(f"Failed to generate Graphviz diagram: {e}")
            error_node = nodes.error()
            error_node += nodes.paragraph(text=f"Graphviz generation failed: {str(e)}")
            return [error_node]
        
        # Create image node
        image_node = nodes.image()
        image_node['uri'] = str(diagram_path.relative_to(Path(app.outdir)))
        image_node['alt'] = f"{visualization_type.capitalize()} Diagram"
        
        if 'width' in self.options:
            image_node['width'] = self.options['width']
        if 'height' in self.options:
            image_node['height'] = self.options['height']
        if 'align' in self.options:
            image_node['align'] = self.options['align']
        
        return [image_node]


def setup(app):
    """Sphinx extension setup for Graphviz integration."""
    app.add_directive('graphviz_assess', GraphvizDirective)
    
    return {
        'version': '1.0.0',
        'parallel_read_safe': True,
        'parallel_write_safe': False,  # File I/O for diagram generation
    }
```

---

### 2.2 Advanced Graphviz Layouts

**Objective:** Implement specialized layout algorithms for different analytical perspectives.

#### 2.2.1 Circular Dependency Detector

**File:** `extensions/sphinx_assess/generators/graphviz_circular_layout.py`

```python
"""
Circular layout for detecting cyclic dependencies in tag relationships.
Uses 'circo' engine to expose problematic circular references.
"""

from typing import List, Dict, Any, Set, Tuple
from pathlib import Path
import logging

from .graphviz_generator import GraphvizGenerator

logger = logging.getLogger(__name__)


class CircularDependencyAnalyzer(GraphvizGenerator):
    """
    Specialized Graphviz generator for cycle detection.
    
    Use Cases
    ---------
    - Detect circular traceability (A → B → C → A)
    - Identify mutual dependencies between layers
    - Validate acyclic constraint in hierarchical documentation
    """
    
    def __init__(self, config: Dict[str, Any], output_dir: Path):
        super().__init__(config, output_dir)
        self.engine = 'circo'  # Force circular layout engine
    
    def detect_cycles(
        self,
        needs: List[Dict[str, Any]],
        output_filename: str = 'cycle_detection'
    ) -> Tuple[Path, List[List[str]]]:
        """
        Generate circular layout highlighting dependency cycles.
        
        Parameters
        ----------
        needs : List[Dict[str, Any]]
            All needs to analyze.
        output_filename : str
            Output filename.
        
        Returns
        -------
        Tuple[Path, List[List[str]]]
            (Path to diagram, List of detected cycles)
            Each cycle is a list of tag IDs forming a closed loop.
        """
        # Build directed graph
        graph = self._build_dependency_graph(needs)
        
        # Detect cycles using Tarjan's algorithm
        cycles = self._find_cycles(graph)
        
        # Generate visualization
        dot = self._init_graph("Circular Dependency Analysis", engine='circo')
        
        # Add all nodes
        for need in needs:
            is_in_cycle = any(need['id'] in cycle for cycle in cycles)
            
            fillcolor = self.colors['VIOLATION'] if is_in_cycle else '#E8F5E9'
            penwidth = 3 if is_in_cycle else 1
            
            dot.append(f'  "{need["id"]}" [')
            dot.append(f'    label="{need["id"]}",')
            dot.append(f'    shape=circle,')
            dot.append(f'    style=filled,')
            dot.append(f'    fillcolor="{fillcolor}",')
            dot.append(f'    penwidth={penwidth}')
            dot.append(f'  ];')
        
        # Add edges with cycle highlighting
        for source_id, targets in graph.items():
            for target_id in targets:
                # Check if this edge participates in a cycle
                is_cycle_edge = any(
                    source_id in cycle and target_id in cycle
                    for cycle in cycles
                )
                
                edge_color = '#E74C3C' if is_cycle_edge else '#95A5A6'
                penwidth = 2.5 if is_cycle_edge else 1
                
                dot.append(f'  "{source_id}" -> "{target_id}" [')
                dot.append(f'    color="{edge_color}",')
                dot.append(f'    penwidth={penwidth}')
                dot.append(f'  ];')
        
        # Add legend
        if cycles:
            dot.append('  legend [')
            dot.append(f'    label="⚠ {len(cycles)} cycles detected",')
            dot.append('    shape=note,')
            dot.append(f'    fillcolor="{self.colors["VIOLATION"]}",')
            dot.append('    style=filled')
            dot.append('  ];')
        
        output_path = self._render_graph(dot, output_filename)
        
        return output_path, cycles
    
    def _build_dependency_graph(
        self,
        needs: List[Dict[str, Any]]
    ) -> Dict[str, Set[str]]:
        """Build adjacency list representation of tag dependencies."""
        graph = {}
        
        for need in needs:
            node_id = need['id']
            graph[node_id] = set()
            
            if 'links' in need:
                for link_type, linked_ids in need['links'].items():
                    # Only consider directional dependency links
                    if link_type in ['satisfies', 'refines', 'derives_from', 'constrains']:
                        graph[node_id].update(linked_ids)
        
        return graph
    
    def _find_cycles(
        self,
        graph: Dict[str, Set[str]]
    ) -> List[List[str]]:
        """
        Detect all cycles in directed graph using Tarjan's algorithm.
        
        Returns
        -------
        List[List[str]]
            List of cycles, each represented as list of node IDs.
        """
        # Tarjan's strongly connected components algorithm
        index_counter = [0]
        stack = []
        lowlinks = {}
        index = {}
        on_stack = {}
        sccs = []
        
        def strongconnect(node):
            index[node] = index_counter[0]
            lowlinks[node] = index_counter[0]
            index_counter[0] += 1
            on_stack[node] = True
            stack.append(node)
            
            for successor in graph.get(node, []):
                if successor not in index:
                    strongconnect(successor)
                    lowlinks[node] = min(lowlinks[node], lowlinks[successor])
                elif on_stack.get(successor, False):
                    lowlinks[node] = min(lowlinks[node], index[successor])
            
            if lowlinks[node] == index[node]:
                scc = []
                while True:
                    successor = stack.pop()
                    on_stack[successor] = False
                    scc.append(successor)
                    if successor == node:
                        break
                sccs.append(scc)
        
        for node in graph:
            if node not in index:
                strongconnect(node)
        
        # Filter to only cycles (SCCs with > 1 node or self-loops)
        cycles = []
        for scc in sccs:
            if len(scc) > 1:
                cycles.append(scc)
            elif len(scc) == 1:
                node = scc[0]
                if node in graph.get(node, []):  # Self-loop
                    cycles.append(scc)
        
        return cycles
```

#### 2.2.2 Layer Interaction Matrix

**File:** `extensions/sphinx_assess/generators/graphviz_layer_matrix.py`

```python
"""
Layer interaction matrix visualization using Graphviz.
Shows cross-layer dependencies as weighted adjacency matrix.
"""

from typing import List, Dict, Any
from pathlib import Path
import logging

from .graphviz_generator import GraphvizGenerator

logger = logging.getLogger(__name__)


class LayerInteractionMatrix(GraphvizGenerator):
    """
    Generate matrix-style visualization of layer-to-layer dependencies.
    
    Visual Encoding
    ---------------
    - Rows/Columns: Documentation layers (BRD, NFR, FSD, SAD, ICD, TDD, ISP)
    - Cell color intensity: Number of cross-layer links
    - Cell labels: Link count
    """
    
    def generate_interaction_matrix(
        self,
        needs: List[Dict[str, Any]],
        output_filename: str = 'layer_matrix'
    ) -> Path:
        """
        Generate layer interaction matrix.
        
        Parameters
        ----------
        needs : List[Dict[str, Any]]
            All needs to analyze.
        output_filename : str
            Output filename.
        
        Returns
        -------
        Path
            Path to generated matrix diagram.
        """
        # Define layer ordering
        layers = ['BRD', 'NFR', 'FSD', 'SAD', 'ICD', 'TDD', 'ISP']
        
        # Build interaction matrix
        matrix = {layer: {other: 0 for other in layers} for layer in layers}
        
        for need in needs:
            source_layer = need['id'].split('-')[0]
            
            if source_layer not in layers:
                continue
            
            if 'links' in need:
                for link_type, linked_ids in need['links'].items():
                    for linked_id in linked_ids:
                        target_layer = linked_id.split('-')[0]
                        
                        if target_layer in layers:
                            matrix[source_layer][target_layer] += 1
        
        # Generate DOT graph using HTML-like table
        dot = [
            'digraph "Layer Interaction Matrix" {',
            '  node [shape=plaintext];',
            '  matrix [label=<',
            '    <table border="1" cellborder="1" cellspacing="0">',
        ]
        
        # Header row
        header = '      <tr><td bgcolor="lightgrey"><b>From \\ To</b></td>'
        for layer in layers:
            header += f'<td bgcolor="lightgrey"><b>{layer}</b></td>'
        header += '</tr>'
        dot.append(header)
        
        # Data rows
        for source_layer in layers:
            row = f'      <tr><td bgcolor="lightgrey"><b>{source_layer}</b></td>'
            
            for target_layer in layers:
                count = matrix[source_layer][target_layer]
                
                # Color intensity based on count
                if count == 0:
                    bgcolor = '#FFFFFF'
                elif count <= 5:
                    bgcolor = '#E3F2FD'
                elif count <= 10:
                    bgcolor = '#90CAF9'
                elif count <= 20:
                    bgcolor = '#42A5F5'
                else:
                    bgcolor = '#1976D2'
                
                fontcolor = '#FFFFFF' if count > 10 else '#000000'
                
                row += f'<td bgcolor="{bgcolor}"><font color="{fontcolor}">{count}</font></td>'
            
            row += '</tr>'
            dot.append(row)
        
        dot.extend([
            '    </table>',
            '  >];',
            '}'
        ])
        
        output_path = self._render_graph(dot, output_filename)
        return output_path
```

---

## Phase 3: PlantUML Template System (70 hours)

### 3.1 Template Architecture

**Objective:** Create Jinja2-based PlantUML template system for pattern-specific diagram generation.

#### 3.1.1 Template Loader and Manager

**File:** `extensions/sphinx_assess/generators/template_loader.py`

```python
"""
Jinja2 template loader and rendering engine for PlantUML generation.
Supports template inheritance, macros, and custom filters.
"""

from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from pathlib import Path
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class PlantUMLTemplateLoader:
    """
    Manages PlantUML Jinja2 templates with custom filters and macros.
    
    Parameters
    ----------
    template_dirs : List[Path]
        List of directories to search for templates.
    
    Attributes
    ----------
    env : jinja2.Environment
        Jinja2 environment with custom filters registered.
    """
    
    def __init__(self, template_dirs: List[Path]):
        self.template_dirs = [Path(d) for d in template_dirs]
        
        # Verify template directories exist
        for template_dir in self.template_dirs:
            if not template_dir.exists():
                logger.warning(f"Template directory does not exist: {template_dir}")
        
        # Initialize Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader([str(d) for d in self.template_dirs]),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True
        )
        
        # Register custom filters
        self._register_filters()
        
        # Register custom macros
        self._register_macros()
    
    def render_template(
        self,
        template_name: str,
        context: Dict[str, Any]
    ) -> str:
        """
        Render PlantUML template with provided context.
        
        Parameters
        ----------
        template_name : str
            Name of template file (e.g., 'observer_pattern.puml.jinja2').
        context : Dict[str, Any]
            Template rendering context containing needs, metadata, etc.
        
        Returns
        -------
        str
            Rendered PlantUML source code.
        
        Raises
        ------
        TemplateNotFound
            If template file doesn't exist in search paths.
        """
        try:
            template = self.env.get_template(template_name)
            rendered = template.render(**context)
            
            logger.debug(f"Rendered template '{template_name}' ({len(rendered)} chars)")
            return rendered
        
        except TemplateNotFound as e:
            logger.error(f"Template not found: {template_name}")
            logger.debug(f"Search paths: {self.template_dirs}")
            raise
    
    def _register_filters(self) -> None:
        """Register custom Jinja2 filters for PlantUML generation."""
        
        def plantuml_escape(text: str) -> str:
            """Escape special characters for PlantUML."""
            if not text:
                return ""
            return text.replace('"', '\\"').replace('\n', '\\n')
        
        def truncate_label(text: str, max_length: int = 30) -> str:
            """Truncate text for compact diagram labels."""
            if len(text) <= max_length:
                return text
            return text[:max_length-3] + "..."
        
        def format_multiplicity(mult: str) -> str:
            """Format UML multiplicity notation."""
            mapping = {
                '1': '1',
                '0..1': '0..1',
                '0..*': '*',
                '1..*': '1..*',
                '*': '*'
            }
            return mapping.get(mult, mult)
        
        def color_by_confidence(confidence: float) -> str:
            """Map confidence score to color."""
            if confidence >= 0.8:
                return '#27AE60'  # Green
            elif confidence >= 0.6:
                return '#F39C12'  # Orange
            else:
                return '#E74C3C'  # Red
        
        def group_by_role(needs: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
            """Group needs by pattern role."""
            groups = {}
            for need in needs:
                role = need.get('pattern_role', 'UNKNOWN')
                if role not in groups:
                    groups[role] = []
                groups[role].append(need)
            return groups
        
        # Register filters
        self.env.filters['plantuml_escape'] = plantuml_escape
        self.env.filters['truncate_label'] = truncate_label
        self.env.filters['format_multiplicity'] = format_multiplicity
        self.env.filters['color_by_confidence'] = color_by_confidence
        self.env.filters['group_by_role'] = group_by_role
    
    def _register_macros(self) -> None:
        """Register reusable Jinja2 macros."""
        # Macros are defined in template files and imported via {% import %}
        # This method can pre-load commonly used macro libraries
        
        macro_library = """
        {# Standard PlantUML class definition macro #}
        {% macro class_definition(need, show_attributes=True, show_methods=True) %}
        class {{ need.id | plantuml_escape }} {
          {% if show_attributes %}
          {# Extract attributes from need metadata if available #}
          {% endif %}
          {% if show_methods %}
          {# Extract methods from need metadata if available #}
          {% endif %}
        }
        {% endmacro %}
        
        {# Pattern participant with stereotype #}
        {% macro pattern_participant(need, role, color='#E8F4F8') %}
        class {{ need.id | plantuml_escape }} << {{ role }} >> #{{ color }} {
          + pattern_role: {{ role }}
          + confidence: {{ need.pattern_confidence | default(0.0) }}
        }
        {% endmacro %}
        
        {# Relationship connector #}
        {% macro relationship(source_id, target_id, rel_type='-->', label='') %}
        {{ source_id | plantuml_escape }} {{ rel_type }} {{ target_id | plantuml_escape }}{% if label %} : {{ label | plantuml_escape }}{% endif %}
        {% endmacro %}
        """
        
        # Store macro library for potential runtime access
        self.macro_library = macro_library


class PlantUMLRenderer:
    """
    High-level interface for rendering PlantUML diagrams from assessed needs.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # Initialize template loader
        template_paths = config.get('template_search_paths', ['_templates/plantuml'])
        self.loader = PlantUMLTemplateLoader(template_paths)
    
    def render_pattern_diagram(
        self,
        pattern_name: str,
        needs: List[Dict[str, Any]],
        template_override: str = None
    ) -> str:
        """
        Render pattern-specific PlantUML diagram.
        
        Parameters
        ----------
        pattern_name : str
            Name of pattern (e.g., 'Observer').
        needs : List[Dict[str, Any]]
            Needs participating in this pattern.
        template_override : str, optional
            Override default template for this pattern.
        
        Returns
        -------
        str
            Rendered PlantUML source.
        """
        # Determine template name
        if template_override:
            template_name = template_override
        else:
            template_name = f"{pattern_name.lower()}_pattern.puml.jinja2"
        
        # Build rendering context
        context = {
            'pattern_name': pattern_name,
            'needs': needs,
            'participants': self._extract_participants(needs),
            'relationships': self._extract_relationships(needs),
            'metadata': {
                'generated_by': 'sphinx_assess',
                'pattern': pattern_name,
                'participant_count': len(needs)
            }
        }
        
        # Render template
        return self.loader.render_template(template_name, context)
    
    def render_sequence_diagram(
        self,
        flow_name: str,
        needs: List[Dict[str, Any]],
        template_name: str = 'sequence_flow.puml.jinja2'
    ) -> str:
        """
        Render sequence diagram for process flow.
        
        Parameters
        ----------
        flow_name : str
            Name of process flow.
        needs : List[Dict[str, Any]]
            Needs representing flow steps.
        template_name : str
            Template file to use.
        
        Returns
        -------
        str
            Rendered PlantUML sequence diagram.
        """
        context = {
            'flow_name': flow_name,
            'steps': self._order_flow_steps(needs),
            'actors': self._extract_actors(needs),
            'metadata': {
                'flow_type': needs[0].get('flow_type', 'Sequential') if needs else 'Unknown'
            }
        }
        
        return self.loader.render_template(template_name, context)
    
    def _extract_participants(
        self,
        needs: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Group needs by pattern role."""
        participants = {}
        for need in needs:
            role = need.get('pattern_role', 'UNKNOWN')
            if role not in participants:
                participants[role] = []
            participants[role].append(need)
        return participants
    
    def _extract_relationships(
        self,
        needs: List[Dict[str, Any]]
    ) -> List[Dict[str, str]]:
        """Extract relationships between needs."""
        relationships = []
        
        for need in needs:
            if 'links' not in need:
                continue
            
            for link_type, linked_ids in need['links'].items():
                for linked_id in linked_ids:
                    relationships.append({
                        'source': need['id'],
                        'target': linked_id,
                        'type': link_type
                    })
        
        return relationships
    
    def _order_flow_steps(
        self,
        needs: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Order needs by flow sequence."""
        # Implement topological sort based on flow dependencies
        # For now, return as-is (assumes pre-ordered input)
        return needs
    
    def _extract_actors(
        self,
        needs: List[Dict[str, Any]]
    ) -> Set[str]:
        """Extract unique actors/participants from flow."""
        actors = set()
        for need in needs:
            # Extract actor information from need metadata
            # Implementation depends on how actors are encoded
            if 'actor' in need:
                actors.add(need['actor'])
        return actors
```

#### 3.1.2 Pattern Template Library

**File:** `_templates/plantuml/observer_pattern.puml.jinja2`

```plantuml
@startuml {{ pattern_name }} Pattern Structure

!define SUBJECT_COLOR #FFE5E5
!define OBSERVER_COLOR #E5F5FF
!define CONCRETE_COLOR #F0F0F0

title {{ pattern_name }} Pattern - Assessed Architecture

' ==================================================
' PATTERN INTENT
' ==================================================
note top of Subject
  **Pattern:** {{ pattern_name }}
  **Intent:** Define one-to-many dependency
  **Participants:** {{ participants | length }} total
  **Assessment:** {{ metadata.generated_by }}
end note

' ==================================================
' ABSTRACT PARTICIPANTS
' ==================================================
{% set subjects = participants.get('SUBJECT', []) %}
{% set observers = participants.get('OBSERVER', []) %}

{% for subject in subjects %}
abstract class {{ subject.id | plantuml_escape }} << SUBJECT >> SUBJECT_COLOR {
  - observers: List<Observer>
  + attach(Observer): void
  + detach(Observer): void
  + notify(): void
  --
  **Confidence:** {{ subject.pattern_confidence | default(0.0) | round(2) }}
  **Rationale:** {{ subject.pattern_rationale | default('N/A') | truncate_label(50) }}
}
{% endfor %}

{% for observer in observers %}
interface {{ observer.id | plantuml_escape }} << OBSERVER >> OBSERVER_COLOR {
  + update(Subject): void
```plantuml
  --
  **Confidence:** {{ observer.pattern_confidence | default(0.0) | round(2) }}
}
{% endfor %}

' ==================================================
' CONCRETE PARTICIPANTS
' ==================================================
{% set concrete_subjects = participants.get('CONCRETE_SUBJECT', []) %}
{% set concrete_observers = participants.get('CONCRETE_OBSERVER', []) %}

{% for concrete_subject in concrete_subjects %}
class {{ concrete_subject.id | plantuml_escape }} << CONCRETE_SUBJECT >> CONCRETE_COLOR {
  - state: State
  + getState(): State
  + setState(State): void
  --
  **Confidence:** {{ concrete_subject.pattern_confidence | default(0.0) | round(2) }}
}
{% endfor %}

{% for concrete_observer in concrete_observers %}
class {{ concrete_observer.id | plantuml_escape }} << CONCRETE_OBSERVER >> CONCRETE_COLOR {
  - observerState: State
  + update(Subject): void
  --
  **Confidence:** {{ concrete_observer.pattern_confidence | default(0.0) | round(2) }}
}
{% endfor %}

' ==================================================
' RELATIONSHIPS
' ==================================================
{% for subject in subjects %}
  {% for observer in observers %}
{{ subject.id | plantuml_escape }} o-- "0..*" {{ observer.id | plantuml_escape }} : observers
  {% endfor %}
{% endfor %}

{% for concrete_subject in concrete_subjects %}
  {% for subject in subjects %}
{{ concrete_subject.id | plantuml_escape }} --|> {{ subject.id | plantuml_escape }}
  {% endfor %}
{% endfor %}

{% for concrete_observer in concrete_observers %}
  {% for observer in observers %}
{{ concrete_observer.id | plantuml_escape }} ..|> {{ observer.id | plantuml_escape }}
  {% endfor %}
  {% for subject in subjects %}
{{ concrete_observer.id | plantuml_escape }} ..> {{ subject.id | plantuml_escape }} : observes
  {% endfor %}
{% endfor %}

' ==================================================
' ADDITIONAL RELATIONSHIPS FROM TRACEABILITY
' ==================================================
{% for relationship in relationships %}
  {% if relationship.type in ['constrains', 'validates', 'implements_pattern'] %}
{{ relationship.source | plantuml_escape }} ..> {{ relationship.target | plantuml_escape }} : << {{ relationship.type }} >>
  {% endif %}
{% endfor %}

' ==================================================
' LEGEND
' ==================================================
legend right
  **Color Coding**
  |= Color |= Participant Type |
  | <back:SUBJECT_COLOR>      </back> | Subject (Abstract) |
  | <back:OBSERVER_COLOR>     </back> | Observer (Interface) |
  | <back:CONCRETE_COLOR>     </back> | Concrete Implementation |
  
  **Confidence Interpretation**
  * > 0.8: High confidence classification
  * 0.6-0.8: Moderate confidence
  * < 0.6: Low confidence (review needed)
endlegend

@enduml
```

**File:** `_templates/plantuml/strategy_pattern.puml.jinja2`

```plantuml
@startuml {{ pattern_name }} Pattern Structure

!define CONTEXT_COLOR #FFF9C4
!define STRATEGY_COLOR #E1BEE7
!define CONCRETE_STRATEGY_COLOR #C5E1A5

title {{ pattern_name }} Pattern - Assessed Architecture

' ==================================================
' PATTERN DOCUMENTATION
' ==================================================
note as PatternIntent
  **Pattern:** {{ pattern_name }}
  **Category:** Behavioral
  **Intent:** Define a family of algorithms, encapsulate
  each one, and make them interchangeable
  **Applicability:**
  * Need different variants of an algorithm
  * Want to hide algorithm implementation details
  * Class defines many behaviors via conditionals
end note

' ==================================================
' CONTEXT PARTICIPANT
' ==================================================
{% set contexts = participants.get('CONTEXT', []) %}

{% for context in contexts %}
class {{ context.id | plantuml_escape }} << CONTEXT >> CONTEXT_COLOR {
  - strategy: Strategy
  + setStrategy(Strategy): void
  + executeStrategy(): void
  --
  **Assessment Metadata**
  Confidence: {{ context.pattern_confidence | default(0.0) | round(2) }}
  Assessed By: {{ context.assessed_by | default('N/A') }}
  Timestamp: {{ context.assessment_timestamp | default('N/A') }}
}
{% endfor %}

' ==================================================
' STRATEGY INTERFACE
' ==================================================
{% set strategies = participants.get('STRATEGY', []) %}

{% for strategy in strategies %}
interface {{ strategy.id | plantuml_escape }} << STRATEGY >> STRATEGY_COLOR {
  + execute(): Result
  --
  **Confidence:** {{ strategy.pattern_confidence | default(0.0) | round(2) }}
}
{% endfor %}

' ==================================================
' CONCRETE STRATEGIES
' ==================================================
{% set concrete_strategies = participants.get('CONCRETE_STRATEGY', []) %}

{% for concrete_strategy in concrete_strategies %}
class {{ concrete_strategy.id | plantuml_escape }} << CONCRETE_STRATEGY >> CONCRETE_STRATEGY_COLOR {
  + execute(): Result
  --
  **Algorithm Variant:** {{ loop.index }}
  **Confidence:** {{ concrete_strategy.pattern_confidence | default(0.0) | round(2) }}
  {% if concrete_strategy.pattern_rationale %}
  **Rationale:** {{ concrete_strategy.pattern_rationale | truncate_label(60) }}
  {% endif %}
}
{% endfor %}

' ==================================================
' STRUCTURAL RELATIONSHIPS
' ==================================================
{% for context in contexts %}
  {% for strategy in strategies %}
{{ context.id | plantuml_escape }} o-- {{ strategy.id | plantuml_escape }} : strategy
{{ context.id | plantuml_escape }} ..> {{ strategy.id | plantuml_escape }} : uses
  {% endfor %}
{% endfor %}

{% for concrete_strategy in concrete_strategies %}
  {% for strategy in strategies %}
{{ concrete_strategy.id | plantuml_escape }} ..|> {{ strategy.id | plantuml_escape }}
  {% endfor %}
{% endfor %}

' ==================================================
' SEQUENCE COLLABORATION (OPTIONAL)
' ==================================================
{% if show_sequence | default(false) %}
== Runtime Behavior ==

{% for context in contexts %}
{% set strategy_ref = strategies[0].id if strategies else 'Strategy' %}
{{ context.id | plantuml_escape }} -> {{ strategy_ref | plantuml_escape }} : execute()
activate {{ strategy_ref | plantuml_escape }}
{{ strategy_ref | plantuml_escape }} --> {{ context.id | plantuml_escape }} : result
deactivate {{ strategy_ref | plantuml_escape }}
{% endfor %}
{% endif %}

@enduml
```

**File:** `_templates/plantuml/sequence_flow.puml.jinja2`

```plantuml
@startuml {{ flow_name }} Process Flow

!define ACTOR_COLOR #B3E5FC
!define COMPONENT_COLOR #FFE082
!define PROCESS_COLOR #A5D6A7

title {{ flow_name }} - Behavioral Sequence

' ==================================================
' PARTICIPANTS
' ==================================================
{% for actor in actors %}
actor "{{ actor | plantuml_escape }}" as {{ actor | replace(' ', '_') }} ACTOR_COLOR
{% endfor %}

{% for step in steps %}
  {% if step.type == 'component' %}
participant "{{ step.id | plantuml_escape }}" as {{ step.id | replace('-', '_') }} COMPONENT_COLOR
  {% elif step.type == 'process' %}
participant "{{ step.id | plantuml_escape }}" as {{ step.id | replace('-', '_') }} PROCESS_COLOR
  {% endif %}
{% endfor %}

' ==================================================
' FLOW METADATA
' ==================================================
note over {% if actors %}{{ actors | first | replace(' ', '_') }}{% else %}{{ steps[0].id | replace('-', '_') }}{% endif %}
  **Flow Type:** {{ metadata.flow_type | default('Sequential') }}
  **Error Handling:** {{ metadata.error_handling | default('Not Specified') }}
  **Concurrency Model:** {{ metadata.concurrency_model | default('Synchronous') }}
end note

' ==================================================
' SEQUENCE STEPS
' ==================================================
{% for step in steps %}
  {% set source = step.source | default('User') | replace(' ', '_') | replace('-', '_') %}
  {% set target = step.target | default(step.id) | replace('-', '_') %}
  {% set message = step.message | default(step.title) | truncate_label(40) %}
  
  {% if step.activation | default(true) %}
{{ source }} -> {{ target }} : {{ message | plantuml_escape }}
activate {{ target }}
  {% else %}
{{ source }} -> {{ target }} : {{ message | plantuml_escape }}
  {% endif %}
  
  {% if step.note %}
note right
  {{ step.note | plantuml_escape }}
end note
  {% endif %}
  
  {% if step.return_message %}
{{ target }} --> {{ source }} : {{ step.return_message | plantuml_escape }}
deactivate {{ target }}
  {% endif %}
  
  {% if step.alt_path %}
alt {{ step.alt_condition | default('Alternative Path') }}
  {{ step.alt_path | plantuml_escape }}
end
  {% endif %}
  
  {% if step.loop %}
loop {{ step.loop_condition | default('Repeat') }}
  {{ step.loop_body | plantuml_escape }}
end
  {% endif %}
  
{% endfor %}

' ==================================================
' ERROR HANDLING PATHS
' ==================================================
{% if error_flows %}
== Error Scenarios ==

{% for error in error_flows %}
{{ error.source | replace('-', '_') }} -[#red]> {{ error.target | replace('-', '_') }} : **ERROR:** {{ error.message | plantuml_escape }}
note right #FFCCCC
  **Error Type:** {{ error.type }}
  **Recovery:** {{ error.recovery_strategy }}
end note
{% endfor %}
{% endif %}

@enduml
```

**File:** `_templates/plantuml/component_diagram.puml.jinja2`

```plantuml
@startuml {{ diagram_title | default('Component Architecture') }}

!define CORE_COLOR #E3F2FD
!define SERVICE_COLOR #F3E5F5
!define EXTERNAL_COLOR #FFF9C4

title {{ diagram_title | default('System Component View') }}

' ==================================================
' ARCHITECTURAL LAYERS
' ==================================================
package "{{ layer_name | default('Application Layer') }}" {
  
  {% for component in components %}
  {% set comp_color = CORE_COLOR if component.category == 'core' else SERVICE_COLOR if component.category == 'service' else EXTERNAL_COLOR %}
  
  component "{{ component.id | plantuml_escape }}" as {{ component.id | replace('-', '_') }} {{ comp_color }} {
    {% if component.interfaces %}
    portin "{{ component.id }}_in"
    portout "{{ component.id }}_out"
    {% endif %}
    
    {% if component.description %}
    note bottom
      {{ component.description | truncate_label(80) }}
      {% if component.pattern_role %}
      **Pattern Role:** {{ component.pattern_role }}
      {% endif %}
    end note
    {% endif %}
  }
  {% endfor %}
}

' ==================================================
' COMPONENT RELATIONSHIPS
' ==================================================
{% for relationship in relationships %}
  {% set source_comp = relationship.source | replace('-', '_') %}
  {% set target_comp = relationship.target | replace('-', '_') %}
  {% set rel_label = relationship.label | default(relationship.type) %}
  
  {% if relationship.type == 'depends_on' %}
{{ source_comp }} ..> {{ target_comp }} : << depends >>
  {% elif relationship.type == 'uses' %}
{{ source_comp }} --> {{ target_comp }} : {{ rel_label | plantuml_escape }}
  {% elif relationship.type == 'implements' %}
{{ source_comp }} ..|> {{ target_comp }}
  {% elif relationship.type == 'aggregates' %}
{{ source_comp }} o-- {{ target_comp }}
  {% elif relationship.type == 'composes' %}
{{ source_comp }} *-- {{ target_comp }}
  {% endif %}
{% endfor %}

' ==================================================
' EXTERNAL INTERFACES
' ==================================================
{% if external_systems %}
== External System Integration ==

{% for external in external_systems %}
cloud "{{ external.name | plantuml_escape }}" as {{ external.id | replace('-', '_') }} EXTERNAL_COLOR
{{ external.connector_component | replace('-', '_') }} ..> {{ external.id | replace('-', '_') }} : {{ external.protocol | default('API') }}
{% endfor %}
{% endif %}

@enduml
```

---

### 3.2 PlantUML Generator Integration

**File:** `extensions/sphinx_assess/generators/plantuml_generator.py`

```python
"""
PlantUML diagram generation and rendering pipeline.
Integrates template system with PlantUML JAR execution.
"""

import subprocess
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
import hashlib

from .template_loader import PlantUMLTemplateLoader, PlantUMLRenderer

logger = logging.getLogger(__name__)


class PlantUMLGenerator:
    """
    High-level PlantUML diagram generation orchestrator.
    
    Workflow
    --------
    1. Load pattern/flow definitions from assessed needs
    2. Render Jinja2 template to PlantUML source
    3. Execute PlantUML JAR to generate output (SVG/PNG/PDF)
    4. Cache results for incremental builds
    
    Parameters
    ----------
    config : Dict[str, Any]
        Assessment configuration containing PlantUML settings.
    output_dir : Path
        Directory for generated diagrams.
    """
    
    def __init__(self, config: Dict[str, Any], output_dir: Path):
        self.config = config
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize template renderer
        self.renderer = PlantUMLRenderer(config)
        
        # PlantUML JAR configuration
        self.plantuml_jar = Path(config.get('plantuml_jar_path', '/usr/local/bin/plantuml.jar'))
        self.output_format = config.get('plantuml_output_format', 'svg')
        
        # Verify PlantUML installation
        self._verify_plantuml()
    
    def _verify_plantuml(self) -> None:
        """Verify PlantUML JAR is accessible."""
        if not self.plantuml_jar.exists():
            logger.warning(
                f"PlantUML JAR not found at {self.plantuml_jar}. "
                "Diagram generation will fail. Install PlantUML: "
                "https://plantuml.com/download"
            )
    
    def generate_pattern_diagram(
        self,
        pattern_name: str,
        needs: List[Dict[str, Any]],
        output_filename: str,
        template_override: Optional[str] = None
    ) -> Path:
        """
        Generate pattern-specific class diagram.
        
        Parameters
        ----------
        pattern_name : str
            Name of design pattern (e.g., 'Observer').
        needs : List[Dict[str, Any]]
            Needs participating in pattern.
        output_filename : str
            Base filename (without extension).
        template_override : Optional[str]
            Override default template.
        
        Returns
        -------
        Path
            Path to generated diagram file.
        """
        # Render PlantUML source from template
        plantuml_source = self.renderer.render_pattern_diagram(
            pattern_name=pattern_name,
            needs=needs,
            template_override=template_override
        )
        
        # Generate diagram
        output_path = self._render_plantuml(
            plantuml_source,
            output_filename
        )
        
        return output_path
    
    def generate_sequence_diagram(
        self,
        flow_name: str,
        needs: List[Dict[str, Any]],
        output_filename: str,
        template_name: str = 'sequence_flow.puml.jinja2'
    ) -> Path:
        """
        Generate sequence diagram for process flow.
        
        Parameters
        ----------
        flow_name : str
            Name of flow.
        needs : List[Dict[str, Any]]
            Flow step definitions.
        output_filename : str
            Output filename.
        template_name : str
            Template to use.
        
        Returns
        -------
        Path
            Path to generated diagram.
        """
        plantuml_source = self.renderer.render_sequence_diagram(
            flow_name=flow_name,
            needs=needs,
            template_name=template_name
        )
        
        output_path = self._render_plantuml(
            plantuml_source,
            output_filename
        )
        
        return output_path
    
    def generate_component_diagram(
        self,
        needs: List[Dict[str, Any]],
        output_filename: str,
        diagram_title: str = 'Component Architecture'
    ) -> Path:
        """
        Generate component/package diagram.
        
        Parameters
        ----------
        needs : List[Dict[str, Any]]
            Component definitions.
        output_filename : str
            Output filename.
        diagram_title : str
            Diagram title.
        
        Returns
        -------
        Path
            Path to generated diagram.
        """
        # Extract components and relationships
        components = self._extract_components(needs)
        relationships = self._extract_component_relationships(needs)
        
        # Build context
        context = {
            'diagram_title': diagram_title,
            'components': components,
            'relationships': relationships,
            'layer_name': self._infer_layer_name(needs)
        }
        
        # Render template
        template_name = 'component_diagram.puml.jinja2'
        plantuml_source = self.renderer.loader.render_template(
            template_name,
            context
        )
        
        output_path = self._render_plantuml(
            plantuml_source,
            output_filename
        )
        
        return output_path
    
    def _render_plantuml(
        self,
        plantuml_source: str,
        output_filename: str
    ) -> Path:
        """
        Execute PlantUML JAR to render diagram.
        
        Parameters
        ----------
        plantuml_source : str
            PlantUML source code.
        output_filename : str
            Base filename without extension.
        
        Returns
        -------
        Path
            Path to generated output file.
        """
        # Generate content hash for caching
        content_hash = hashlib.md5(plantuml_source.encode()).hexdigest()[:8]
        
        # Define file paths
        puml_file = self.output_dir / f"{output_filename}_{content_hash}.puml"
        output_file = self.output_dir / f"{output_filename}_{content_hash}.{self.output_format}"
        
        # Check cache
        if output_file.exists():
            logger.debug(f"Using cached PlantUML output: {output_file}")
            return output_file
        
        # Write PlantUML source
        puml_file.write_text(plantuml_source, encoding='utf-8')
        logger.debug(f"Generated PlantUML source: {puml_file}")
        
        # Execute PlantUML
        try:
            cmd = [
                'java',
                '-jar',
                str(self.plantuml_jar),
                f'-t{self.output_format}',
                '-charset', 'UTF-8',
                '-o', str(self.output_dir),
                str(puml_file)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode != 0:
                logger.error(f"PlantUML rendering failed: {result.stderr}")
                raise RuntimeError(f"PlantUML error: {result.stderr}")
            
            logger.info(f"Generated PlantUML diagram: {output_file}")
            return output_file
        
        except subprocess.TimeoutExpired:
            logger.error(f"PlantUML rendering timed out for {puml_file}")
            raise
        
        except FileNotFoundError:
            logger.error(
                "Java or PlantUML JAR not found. "
                "Ensure Java is installed and plantuml_jar_path is configured correctly."
            )
            raise
    
    def _extract_components(
        self,
        needs: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Extract component definitions from needs."""
        components = []
        
        for need in needs:
            component = {
                'id': need['id'],
                'title': need.get('title', ''),
                'description': need.get('description', ''),
                'category': self._infer_category(need),
                'pattern_role': need.get('pattern_role'),
                'interfaces': need.get('interfaces', [])
            }
            components.append(component)
        
        return components
    
    def _extract_component_relationships(
        self,
        needs: List[Dict[str, Any]]
    ) -> List[Dict[str, str]]:
        """Extract relationships between components."""
        relationships = []
        
        for need in needs:
            if 'links' not in need:
                continue
            
            for link_type, linked_ids in need['links'].items():
                for linked_id in linked_ids:
                    relationships.append({
                        'source': need['id'],
                        'target': linked_id,
                        'type': link_type,
                        'label': link_type.replace('_', ' ').title()
                    })
        
        return relationships
    
    def _infer_category(self, need: Dict[str, Any]) -> str:
        """Infer component category from metadata."""
        need_type = need.get('type', '').lower()
        
        if 'core' in need_type or need.get('is_core', False):
            return 'core'
        elif 'service' in need_type:
            return 'service'
        else:
            return 'component'
    
    def _infer_layer_name(self, needs: List[Dict[str, Any]]) -> str:
        """Infer architectural layer from needs."""
        if not needs:
            return 'Application Layer'
        
        # Use first need's layer prefix
        layer_prefix = needs[0]['id'].split('-')[0]
        
        layer_map = {
            'BRD': 'Business Layer',
            'FSD': 'Feature Layer',
            'SAD': 'Architecture Layer',
            'TDD': 'Technical Layer',
            'ISP': 'Implementation Layer'
        }
        
        return layer_map.get(layer_prefix, 'Application Layer')
```

---

## Phase 4: Validation Framework (60 hours)

### 4.1 Pattern Constraint Validator

**File:** `extensions/sphinx_assess/validators/pattern_validator.py`

```python
"""
Comprehensive pattern constraint validation engine.
Validates structural adherence to pattern definitions.
"""

import logging
from typing import Dict, List, Any, Set, Tuple
import yaml
from pathlib import Path

logger = logging.getLogger(__name__)


class PatternStructuralValidator:
    """
    Validates that classified tags satisfy pattern structural constraints.
    
    Validation Types
    ----------------
    1. Multiplicity: Check participant count constraints
    2. Relationships: Verify required connections exist
    3. Methods: Ensure required operations are present (if metadata available)
    4. Constraints: Validate pattern-specific rules
    
    Parameters
    ----------
    schema_path : Path
        Path to pattern schema YAML file.
    """
    
    def __init__(self, schema_path: Path):
        self.schema_path = Path(schema_path)
        self.schema = self._load_schema()
    
    def _load_schema(self) -> Dict[str, Any]:
        """Load pattern schema definitions."""
        with open(self.schema_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def validate_pattern(
        self,
        pattern_name: str,
        classified_needs: List[Dict[str, Any]],
        strictness: str = 'WARNING'
    ) -> Dict[str, Any]:
        """
        Validate pattern implementation against schema.
        
        Parameters
        ----------
        pattern_name : str
            Name of pattern to validate (e.g., 'Observer').
        classified_needs : List[Dict[str, Any]]
            Needs classified as participating in this pattern.
        strictness : str
            Validation mode: 'ERROR' | 'WARNING' | 'INFO'
        
        Returns
        -------
        Dict[str, Any]
            Validation report:
            {
                "pattern": "Observer",
                "status": "PASS" | "FAIL" | "WARNING",
                "violations": [list of violation objects],
                "statistics": {
                    "total_participants": 5,
                    "roles_detected": ["SUBJECT", "OBSERVER"],
                    "missing_roles": [],
                    "constraint_checks": 12,
                    "failures": 2
                }
            }
        """
        # Find pattern definition in schema
        pattern_def = self._get_pattern_definition(pattern_name)
        
        if not pattern_def:
            logger.error(f"Pattern '{pattern_name}' not found in schema")
            return {
                'pattern': pattern_name,
                'status': 'ERROR',
                'violations': [{
                    'type': 'SCHEMA_ERROR',
                    'message': f"Pattern '{pattern_name}' not defined in schema"
                }],
                'statistics': {}
            }
        
        violations = []
        
        # Validate multiplicity constraints
        multiplicity_violations = self._validate_multiplicity(
            pattern_def,
            classified_needs
        )
        violations.extend(multiplicity_violations)
        
        # Validate relationships
        relationship_violations = self._validate_relationships(
            pattern_def,
            classified_needs
        )
        violations.extend(relationship_violations)
        
        # Validate pattern-specific constraints
        constraint_violations = self._validate_constraints(
            pattern_def,
            classified_needs
        )
        violations.extend(constraint_violations)
        
        # Calculate statistics
        statistics = self._compute_statistics(
            pattern_def,
            classified_needs,
            violations
        )
        
        # Determine overall status
        status = self._determine_status(violations, strictness)
        
        return {
            'pattern': pattern_name,
            'status': status,
            'violations': violations,
            'statistics': statistics,
            'timestamp': self._get_timestamp()
        }
    
    def _get_pattern_definition(
        self,
        pattern_name: str
    ) -> Optional[Dict[str, Any]]:
        """Retrieve pattern definition from schema."""
        for category in self.schema.get('categories', {}).values():
            for pattern in category.get('patterns', []):
                if pattern['name'] == pattern_name:
                    return pattern
        return None
    
    def _validate_multiplicity(
        self,
        pattern_def: Dict[str, Any],
        needs: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Validate participant multiplicity constraints.
        
        Example Constraint: Observer pattern requires exactly 1 SUBJECT
        """
        violations = []
        
        # Group needs by role
        role_counts = {}
        role_members = {}
        
        for need in needs:
            role = need.get('pattern_role')
            if role:
                role_counts[role] = role_counts.get(role, 0) + 1
                if role not in role_members:
                    role_members[role] = []
                role_members[role].append(need['id'])
        
        # Check each participant's multiplicity
        for participant in pattern_def.get('participants', []):
            role = participant['role']
            multiplicity = participant['multiplicity']
            actual_count = role_counts.get(role, 0)
            
            # Parse multiplicity constraint
            violation = self._check_multiplicity_constraint(
                role,
                multiplicity,
                actual_count,
                role_members.get(role, [])
            )
            
            if violation:
                violations.append(violation)
        
        return violations
    
    def _check_multiplicity_constraint(
        self,
        role: str,
        multiplicity: str,
        actual_count: int,
        members: List[str]
    ) -> Optional[Dict[str, Any]]:
        """Check if actual count satisfies multiplicity constraint."""
        
        # Parse multiplicity notation
        if multiplicity == '1':
            if actual_count != 1:
                return {
                    'type': 'MULTIPLICITY',
                    'severity': 'ERROR',
                    'role': role,
                    'constraint': f"Requires exactly 1 {role}",
                    'actual': f"Found {actual_count}",
                    'members': members
                }
        
        elif multiplicity == '0..1':
            if actual_count > 1:
                return {
                    'type': 'MULTIPLICITY',
                    'severity': 'ERROR',
                    'role': role,
                    'constraint': f"Requires 0 or 1 {role}",
                    'actual': f"Found {actual_count}",
                    'members': members
                }
        
        elif multiplicity == '1..*':
            if actual_count < 1:
                return {
                    'type': 'MULTIPLICITY',
                    'severity': 'ERROR',
                    'role': role,
                    'constraint': f"Requires at least 1 {role}",
                    'actual': f"Found {actual_count}",
                    'members': members
                }
        
        elif multiplicity == '0..*':
            # Always satisfied
            pass
        
        elif '..' in multiplicity:
            # Parse range (e.g., '2..5')
            min_val, max_val = multiplicity.split('..')
            min_val = int(min_val)
            max_val = int(max_val) if max_val != '*' else float('inf')
            
            if not (min_val <= actual_count <= max_val):
                return {
                    'type': 'MULTIPLICITY',
                    'severity': 'ERROR',
                    'role': role,
                    'constraint': f"Requires {multiplicity} {role}",
                    'actual': f"Found {actual_count}",
                    'members': members
                }
        
        return None
    
    def _validate_relationships(
        self,
        pattern_def: Dict[str, Any],
        needs: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Validate required relationships exist.
        
        Example: Observer pattern requires SUBJECT to have links to OBSERVERs
        """
        violations = []
        
        # Build relationship map
        relationship_map = {}
        for need in needs:
            relationship_map[need['id']] = need.get('links', {})
        
        # Check pattern-specific relationship requirements
        # (This would be defined in schema; simplified here)
        
        # Example: Check if SUBJECT links to OBSERVERs
        subjects = [n for n in needs if n.get('pattern_role') == 'SUBJECT']
        observers = [n for n in needs if n.get('pattern_role') == 'OBSERVER']
        
        for subject in subjects:
            subject_links = set()
            for link_type, linked_ids in subject.get('links', {}).items():
                subject_links.update(linked_ids)
            
```python
            observer_ids = {obs['id'] for obs in observers}
            linked_observers = subject_links & observer_ids
            
            if observers and not linked_observers:
                violations.append({
                    'type': 'RELATIONSHIP',
                    'severity': 'WARNING',
                    'source': subject['id'],
                    'constraint': 'SUBJECT should link to at least one OBSERVER',
                    'actual': 'No links to OBSERVER participants found',
                    'expected_targets': list(observer_ids)
                })
        
        return violations
    
    def _validate_constraints(
        self,
        pattern_def: Dict[str, Any],
        needs: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Validate pattern-specific constraints.
        
        Example: Observer pattern constraint:
        "SUBJECT must have attach() and notify() methods"
        """
        violations = []
        
        constraints = pattern_def.get('constraints', [])
        
        for constraint_text in constraints:
            # Parse constraint text and validate
            # (Simplified implementation - real version would use NLP/pattern matching)
            
            if 'must have' in constraint_text.lower():
                # Extract required methods/attributes
                violation = self._validate_method_constraint(
                    constraint_text,
                    needs
                )
                if violation:
                    violations.append(violation)
        
        return violations
    
    def _validate_method_constraint(
        self,
        constraint_text: str,
        needs: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """
        Validate method/operation constraints.
        
        Note: This requires method metadata in needs objects.
        If unavailable, returns INFO-level violation.
        """
        # Example constraint: "SUBJECT must have attach() and notify() methods"
        
        # Extract role and methods from constraint text
        # (Simplified parsing - production would use regex/NLP)
        
        if 'SUBJECT' in constraint_text and 'attach()' in constraint_text:
            subjects = [n for n in needs if n.get('pattern_role') == 'SUBJECT']
            
            for subject in subjects:
                methods = subject.get('methods', [])
                
                if not methods:
                    # Metadata not available
                    return {
                        'type': 'CONSTRAINT',
                        'severity': 'INFO',
                        'target': subject['id'],
                        'constraint': constraint_text,
                        'actual': 'Method metadata not available for validation',
                        'recommendation': 'Add method metadata to TDD/ISP layer for validation'
                    }
                
                required_methods = ['attach', 'notify']
                method_names = [m.get('name', '').lower() for m in methods]
                
                missing_methods = [
                    m for m in required_methods
                    if m not in method_names
                ]
                
                if missing_methods:
                    return {
                        'type': 'CONSTRAINT',
                        'severity': 'ERROR',
                        'target': subject['id'],
                        'constraint': constraint_text,
                        'actual': f"Missing methods: {', '.join(missing_methods)}",
                        'found_methods': method_names
                    }
        
        return None
    
    def _compute_statistics(
        self,
        pattern_def: Dict[str, Any],
        needs: List[Dict[str, Any]],
        violations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Compute validation statistics."""
        
        roles_detected = set(n.get('pattern_role') for n in needs if n.get('pattern_role'))
        expected_roles = set(p['role'] for p in pattern_def.get('participants', []))
        missing_roles = expected_roles - roles_detected
        
        error_count = sum(1 for v in violations if v.get('severity') == 'ERROR')
        warning_count = sum(1 for v in violations if v.get('severity') == 'WARNING')
        info_count = sum(1 for v in violations if v.get('severity') == 'INFO')
        
        return {
            'total_participants': len(needs),
            'roles_detected': list(roles_detected),
            'expected_roles': list(expected_roles),
            'missing_roles': list(missing_roles),
            'constraint_checks': len(pattern_def.get('constraints', [])),
            'violations': {
                'total': len(violations),
                'errors': error_count,
                'warnings': warning_count,
                'info': info_count
            }
        }
    
    def _determine_status(
        self,
        violations: List[Dict[str, Any]],
        strictness: str
    ) -> str:
        """Determine overall validation status."""
        
        error_count = sum(1 for v in violations if v.get('severity') == 'ERROR')
        warning_count = sum(1 for v in violations if v.get('severity') == 'WARNING')
        
        if strictness == 'ERROR':
            return 'FAIL' if error_count > 0 else 'PASS'
        elif strictness == 'WARNING':
            return 'FAIL' if (error_count + warning_count) > 0 else 'PASS'
        else:  # INFO
            return 'WARNING' if len(violations) > 0 else 'PASS'
    
    def _get_timestamp(self) -> str:
        """Get ISO 8601 timestamp."""
        from datetime import datetime
        return datetime.utcnow().isoformat() + 'Z'


class DiffAnalyzer:
    """
    Compare ideal (pattern-defined) structure vs actual (implemented) structure.
    """
    
    def __init__(self):
        pass
    
    def compare_structures(
        self,
        ideal_needs: List[Dict[str, Any]],
        actual_needs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Perform structural diff between ideal and actual implementations.
        
        Parameters
        ----------
        ideal_needs : List[Dict[str, Any]]
            Needs from assessment layer (pattern declarations).
        actual_needs : List[Dict[str, Any]]
            Needs from TDD/ISP layer (implementation blueprints).
        
        Returns
        -------
        Dict[str, Any]
            Diff report with added, removed, and modified elements.
        """
        ideal_ids = {n['id'] for n in ideal_needs}
        actual_ids = {n['id'] for n in actual_needs}
        
        added = actual_ids - ideal_ids
        removed = ideal_ids - actual_ids
        common = ideal_ids & actual_ids
        
        modified = []
        for need_id in common:
            ideal_need = next(n for n in ideal_needs if n['id'] == need_id)
            actual_need = next(n for n in actual_needs if n['id'] == need_id)
            
            differences = self._compare_needs(ideal_need, actual_need)
            if differences:
                modified.append({
                    'id': need_id,
                    'differences': differences
                })
        
        return {
            'added': list(added),
            'removed': list(removed),
            'modified': modified,
            'summary': {
                'total_changes': len(added) + len(removed) + len(modified),
                'added_count': len(added),
                'removed_count': len(removed),
                'modified_count': len(modified)
            }
        }
    
    def _compare_needs(
        self,
        ideal: Dict[str, Any],
        actual: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """Compare individual needs for differences."""
        differences = []
        
        # Compare pattern roles
        if ideal.get('pattern_role') != actual.get('pattern_role'):
            differences.append({
                'field': 'pattern_role',
                'expected': ideal.get('pattern_role'),
                'actual': actual.get('pattern_role'),
                'severity': 'ERROR'
            })
        
        # Compare links
        ideal_links = set()
        actual_links = set()
        
        for link_type, linked_ids in ideal.get('links', {}).items():
            ideal_links.update(linked_ids)
        
        for link_type, linked_ids in actual.get('links', {}).items():
            actual_links.update(linked_ids)
        
        missing_links = ideal_links - actual_links
        extra_links = actual_links - ideal_links
        
        if missing_links:
            differences.append({
                'field': 'links',
                'type': 'missing',
                'values': list(missing_links),
                'severity': 'WARNING'
            })
        
        if extra_links:
            differences.append({
                'field': 'links',
                'type': 'extra',
                'values': list(extra_links),
                'severity': 'INFO'
            })
        
        return differences
```

---

### 4.2 Validation Report Generator

**File:** `extensions/sphinx_assess/utils/report_generator.py`

```python
"""
Generate comprehensive validation reports in multiple formats.
Supports JSON, HTML, and Markdown output.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class ValidationReportGenerator:
    """
    Generate multi-format validation reports.
    
    Output Formats
    --------------
    - JSON: Machine-readable for CI/CD integration
    - HTML: Human-readable with styling
    - Markdown: Documentation-friendly format
    """
    
    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_report(
        self,
        validation_results: List[Dict[str, Any]],
        format: str = 'json'
    ) -> Path:
        """
        Generate validation report.
        
        Parameters
        ----------
        validation_results : List[Dict[str, Any]]
            List of validation results from PatternStructuralValidator.
        format : str
            Output format: 'json' | 'html' | 'markdown'
        
        Returns
        -------
        Path
            Path to generated report file.
        """
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        
        if format == 'json':
            return self._generate_json_report(validation_results, timestamp)
        elif format == 'html':
            return self._generate_html_report(validation_results, timestamp)
        elif format == 'markdown':
            return self._generate_markdown_report(validation_results, timestamp)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _generate_json_report(
        self,
        results: List[Dict[str, Any]],
        timestamp: str
    ) -> Path:
        """Generate JSON report."""
        
        report = {
            'metadata': {
                'generated_at': datetime.utcnow().isoformat() + 'Z',
                'generator': 'sphinx_assess ValidationReportGenerator',
                'version': '1.0.0'
            },
            'summary': self._compute_summary(results),
            'validations': results
        }
        
        output_file = self.output_dir / f'validation_report_{timestamp}.json'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Generated JSON validation report: {output_file}")
        return output_file
    
    def _generate_html_report(
        self,
        results: List[Dict[str, Any]],
        timestamp: str
    ) -> Path:
        """Generate HTML report with styling."""
        
        html = self._build_html_header()
        html += self._build_html_summary(results)
        html += self._build_html_violations_table(results)
        html += self._build_html_footer()
        
        output_file = self.output_dir / f'validation_report_{timestamp}.html'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        logger.info(f"Generated HTML validation report: {output_file}")
        return output_file
    
    def _generate_markdown_report(
        self,
        results: List[Dict[str, Any]],
        timestamp: str
    ) -> Path:
        """Generate Markdown report."""
        
        md = [
            '# Pattern Validation Report',
            '',
            f'**Generated:** {datetime.utcnow().isoformat()}Z',
            '',
            '## Summary',
            ''
        ]
        
        summary = self._compute_summary(results)
        
        md.extend([
            f'- **Total Patterns Validated:** {summary["total_patterns"]}',
            f'- **Passed:** {summary["passed"]}',
            f'- **Failed:** {summary["failed"]}',
            f'- **Warnings:** {summary["warnings"]}',
            f'- **Total Violations:** {summary["total_violations"]}',
            '',
            '## Validation Results',
            ''
        ])
        
        for result in results:
            md.extend(self._format_result_markdown(result))
        
        output_file = self.output_dir / f'validation_report_{timestamp}.md'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(md))
        
        logger.info(f"Generated Markdown validation report: {output_file}")
        return output_file
    
    def _compute_summary(
        self,
        results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Compute summary statistics."""
        
        total_patterns = len(results)
        passed = sum(1 for r in results if r['status'] == 'PASS')
        failed = sum(1 for r in results if r['status'] == 'FAIL')
        warnings = sum(1 for r in results if r['status'] == 'WARNING')
        
        total_violations = sum(len(r.get('violations', [])) for r in results)
        
        violation_by_severity = {
            'ERROR': 0,
            'WARNING': 0,
            'INFO': 0
        }
        
        for result in results:
            for violation in result.get('violations', []):
                severity = violation.get('severity', 'INFO')
                violation_by_severity[severity] = violation_by_severity.get(severity, 0) + 1
        
        return {
            'total_patterns': total_patterns,
            'passed': passed,
            'failed': failed,
            'warnings': warnings,
            'total_violations': total_violations,
            'violations_by_severity': violation_by_severity
        }
    
    def _build_html_header(self) -> str:
        """Build HTML document header with CSS."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pattern Validation Report</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            color: #34495e;
            margin-top: 30px;
        }
        .summary {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        .summary-card {
            padding: 15px;
            border-radius: 5px;
            text-align: center;
        }
        .summary-card.pass {
            background: #d4edda;
            border-left: 4px solid #28a745;
        }
        .summary-card.fail {
            background: #f8d7da;
            border-left: 4px solid #dc3545;
        }
        .summary-card.warning {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
        }
        .summary-card .value {
            font-size: 2em;
            font-weight: bold;
            margin: 10px 0;
        }
        .summary-card .label {
            font-size: 0.9em;
            color: #666;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        th {
            background: #3498db;
            color: white;
            padding: 12px;
            text-align: left;
        }
        td {
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }
        tr:hover {
            background: #f8f9fa;
        }
        .severity-ERROR {
            color: #dc3545;
            font-weight: bold;
        }
        .severity-WARNING {
            color: #ffc107;
            font-weight: bold;
        }
        .severity-INFO {
            color: #17a2b8;
        }
        .pattern-section {
            background: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .status-badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
        }
        .status-PASS {
            background: #28a745;
            color: white;
        }
        .status-FAIL {
            background: #dc3545;
            color: white;
        }
        .status-WARNING {
            background: #ffc107;
            color: #333;
        }
    </style>
</head>
<body>
    <h1>Pattern Validation Report</h1>
    <p><strong>Generated:</strong> """ + datetime.utcnow().isoformat() + """Z</p>
"""
    
    def _build_html_summary(self, results: List[Dict[str, Any]]) -> str:
        """Build HTML summary section."""
        summary = self._compute_summary(results)
        
        html = """
    <div class="summary">
        <h2>Summary</h2>
        <div class="summary-grid">
            <div class="summary-card pass">
                <div class="label">Passed</div>
                <div class="value">""" + str(summary['passed']) + """</div>
            </div>
            <div class="summary-card fail">
                <div class="label">Failed</div>
                <div class="value">""" + str(summary['failed']) + """</div>
            </div>
            <div class="summary-card warning">
                <div class="label">Warnings</div>
                <div class="value">""" + str(summary['warnings']) + """</div>
            </div>
            <div class="summary-card">
                <div class="label">Total Violations</div>
                <div class="value">""" + str(summary['total_violations']) + """</div>
            </div>
        </div>
    </div>
"""
        return html
    
    def _build_html_violations_table(
        self,
        results: List[Dict[str, Any]]
    ) -> str:
        """Build HTML violations table."""
        html = ['<h2>Validation Details</h2>']
        
        for result in results:
            pattern_name = result['pattern']
            status = result['status']
            violations = result.get('violations', [])
            
            html.append(f'<div class="pattern-section">')
            html.append(f'<h3>{pattern_name} <span class="status-badge status-{status}">{status}</span></h3>')
            
            if violations:
                html.append('<table>')
                html.append('<thead>')
                html.append('<tr>')
                html.append('<th>Type</th>')
                html.append('<th>Severity</th>')
                html.append('<th>Description</th>')
                html.append('<th>Details</th>')
                html.append('</tr>')
                html.append('</thead>')
                html.append('<tbody>')
                
                for violation in violations:
                    vtype = violation.get('type', 'UNKNOWN')
                    severity = violation.get('severity', 'INFO')
                    constraint = violation.get('constraint', '')
                    actual = violation.get('actual', '')
                    
                    html.append('<tr>')
                    html.append(f'<td>{vtype}</td>')
                    html.append(f'<td class="severity-{severity}">{severity}</td>')
                    html.append(f'<td>{constraint}</td>')
                    html.append(f'<td>{actual}</td>')
                    html.append('</tr>')
                
                html.append('</tbody>')
                html.append('</table>')
            else:
                html.append('<p style="color: #28a745;">✓ No violations detected</p>')
            
            # Add statistics
            stats = result.get('statistics', {})
            if stats:
                html.append('<h4>Statistics</h4>')
                html.append('<ul>')
                html.append(f'<li><strong>Total Participants:</strong> {stats.get("total_participants", 0)}</li>')
                html.append(f'<li><strong>Roles Detected:</strong> {", ".join(stats.get("roles_detected", []))}</li>')
                if stats.get('missing_roles'):
                    html.append(f'<li><strong>Missing Roles:</strong> <span style="color: #dc3545;">{", ".join(stats["missing_roles"])}</span></li>')
                html.append('</ul>')
            
            html.append('</div>')
        
        return '\n'.join(html)
    
    def _build_html_footer(self) -> str:
        """Build HTML document footer."""
        return """
</body>
</html>
"""
    
    def _format_result_markdown(
        self,
        result: Dict[str, Any]
    ) -> List[str]:
        """Format single validation result as Markdown."""
        md = [
            f'### {result["pattern"]} - {result["status"]}',
            ''
        ]
        
        violations = result.get('violations', [])
        
        if violations:
            md.append('**Violations:**')
            md.append('')
            
            for i, violation in enumerate(violations, 1):
                severity = violation.get('severity', 'INFO')
                vtype = violation.get('type', 'UNKNOWN')
                constraint = violation.get('constraint', '')
                actual = violation.get('actual', '')
                
                md.append(f'{i}. **[{severity}]** {vtype}')
                md.append(f'   - **Constraint:** {constraint}')
                md.append(f'   - **Actual:** {actual}')
                md.append('')
        else:
            md.append('✓ No violations detected')
            md.append('')
        
        # Add statistics
        stats = result.get('statistics', {})
        if stats:
            md.append('**Statistics:**')
            md.append(f'- Total Participants: {stats.get("total_participants", 0)}')
            md.append(f'- Roles Detected: {", ".join(stats.get("roles_detected", []))}')
            if stats.get('missing_roles'):
                md.append(f'- Missing Roles: {", ".join(stats["missing_roles"])}')
            md.append('')
        
        md.append('---')
        md.append('')
        
        return md
```

---

## Phase 5: Build Integration & CI/CD (50 hours)

### 5.1 Sphinx Build Hook Integration

**File:** `extensions/sphinx_assess/__init__.py`

```python
"""
Sphinx Assessment Layer Extension - Main Entry Point

Registers all directives, build hooks, and configuration handlers.
"""

import logging
from pathlib import Path
from typing import Dict, Any

from sphinx.application import Sphinx
from sphinx.util import logging as sphinx_logging

# Import directive implementations
from .directives.assess_directive import AssessDirective
from .directives.pattern_directive import PatternDirective
from .generators.graphviz_generator import GraphvizDirective

logger = sphinx_logging.getLogger(__name__)

__version__ = '1.0.0'


def validate_assessment_config(app: Sphinx, config: Any) -> None:
    """
    Validate assessment configuration on config-inited event.
    
    Parameters
    ----------
    app : Sphinx
        Sphinx application instance.
    config : sphinx.config.Config
        Sphinx configuration object.
    """
    assessment_config = getattr(config, 'needs_assessment_config', None)
    
    if not assessment_config:
        logger.warning(
            "needs_assessment_config not found in conf.py. "
            "Assessment layer features will use default configuration."
        )
        return
    
    # Validate required fields
    required_fields = ['llm_provider', 'llm_model']
    missing_fields = [f for f in required_fields if f not in assessment_config]
    
    if missing_fields:
        logger.error(
            f"Missing required assessment config fields: {', '.join(missing_fields)}"
        )
    
    # Validate PlantUML JAR path
    plantuml_jar = Path(assessment_config.get('plantuml_jar_path', '/usr/local/bin/plantuml.jar'))
    if not plantuml_jar.exists():
        logger.warning(
            f"PlantUML JAR not found at {plantuml_jar}. "
            "PlantUML diagram generation will fail."
        )
    
    # Validate pattern schema files
    for schema_file in assessment_config.get('pattern_libraries', []):
        schema_path = Path(schema_file)
        if not schema_path.exists():
            logger.warning(f"Pattern schema file not found: {schema_file}")


def run_post_build_validation(app: Sphinx, exception: Exception) -> None:
    """
    Run validation after build completes.
    
    Parameters
    ----------
    app : Sphinx
        Sphinx application instance.
    exception : Exception
        Build exception if any (None if build succeeded).
    """
    if exception:
        # Build failed, skip validation
        return
    
    logger.info("Running post-build pattern validation...")
    
    from .validators.pattern_validator import PatternStructuralValidator
    from .utils.report_generator import ValidationReportGenerator
    from .utils.needs_query import get_all_needs, filter_needs_by_pattern
    
    config = app.config.needs_assessment_config
    env = app.env
    
    # Get all assessed needs
    all_needs = get_all_needs(env)
    
    # Group by pattern
    pattern_groups = {}
    for need in all_needs:
        pattern_name = need.get('pattern_name')
        if pattern_name:
            if pattern_name not in pattern_groups:
                pattern_groups[pattern_name] = []
            pattern_groups[pattern_name].append(need)
    
    if not pattern_groups:
        logger.info("No patterns detected for validation")
        return
    
    # Validate each pattern
    validation_results = []
    
    for pattern_name, pattern_needs in pattern_groups.items():
        logger.info(f"Validating {pattern_name} pattern ({len(pattern_needs)} participants)...")
        
        # Find appropriate schema
        schema_path = _find_pattern_schema(pattern_name, config)
        
        if not schema_path:
            logger.warning(f"No schema found for pattern: {pattern_name}")
            continue
        
        validator = PatternStructuralValidator(schema_path)
        result = validator.validate_pattern(
            pattern_name=pattern_name,
            classified_needs=pattern_needs,
            strictness=config.get('validation_strictness', 'WARNING')
        )
        
        validation_results.append(result)
        
        # Log summary
        if result['status'] == 'PASS':
            logger.info(f"✓ {pattern_name}: PASS")
        else:
            violation_count = len(result.get('violations', []))
            logger.warning(
                f"✗ {pattern_name}: {result['status']} ({violation_count} violations)"
            )
    
    # Generate validation report
    report_generator = ValidationReportGenerator(
        output_dir=Path(app.outdir) / '_validation'
    )
    
    json_report = report_generator.generate_report(validation_results, format='json')
    html_report = report_generator.generate_report(validation_results, format='html')
    md_report = report_generator.generate_report(validation_results, format='markdown')
    
    logger.info(f"Validation reports generated:")
    logger.info(f"  - JSON: {json_report}")
    logger.info(f"  - HTML: {html_report}")
    logger.info(f"  - Markdown: {md_report}")
    
    # Fail build if configured
    if config.get('fail_build_on_violations', False):
        failed_patterns = [r for r in validation_results if r['status'] == 'FAIL']
        if failed_patterns:
            pattern_names = [r['pattern'] for r in failed_patterns]
            raise RuntimeError(
                f"Build failed due to pattern violations in: {', '.join(pattern_names)}"
            )


def _find_pattern_schema(
    pattern_name: str,
    config: Dict[str, Any]
) -> Path:
    """Find schema file containing pattern definition."""
    for schema_file in config.get('pattern_libraries', []):
        schema_path = Path(schema_file)
        if schema_path.exists():
            # Check if this schema contains the pattern
            # (Simplified - real implementation would parse YAML)
            if 'gof' in schema_path.name.lower():
                return schema_path
    
    return None


def setup(app: Sphinx) -> Dict[str, Any]:
    """
    Sphinx extension setup function.
    
    Parameters
    ----------
    app : Sphinx
        Sphinx application instance.
    
    Returns
    -------
    Dict[str, Any]
        Extension metadata.
    """
    # Register configuration values
    app.add_config_value('needs_assessment_config', {}, 'html')
    
    # Register directives
    app.add_directive('assess', AssessDirective)
    app.add_directive('pattern', PatternDirective)
    app.add_directive('graphviz_assess', GraphvizDirective)
    
    # Register build event hooks
    app.connect('config-inited', validate_assessment_config)
    app.connect('build-finished', run_post_build_validation)
    
    logger.info(f"Sphinx Assessment Layer Extension v{__version__} loaded")
    
    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': False,  # Due to file I/O for diagrams
        'env_version': 1,
    }
```

---

### 5.2 CI/CD Integration

**File:** `.github/workflows/documentation_validation.yml`

```yaml
name: Documentation Validation

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  validate-documentation:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install system dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y \
          graphviz \
          default-jre \
          wget
    
    - name: Install PlantUML
      run: |
        wget https://github.com/plantuml/plantuml/releases/download/v1.2024.0/plantuml-1.2024.0.jar \
          -O /usr/local/bin/plantuml.jar
        java -jar /usr/local/bin/plantuml.jar -version
    
    - name: Install Python dependencies
      run: |
        pip install --upgrade pip
        pip install -r requirements.txt
        pip install -e ./extensions/sphinx_assess
    
    - name: Build documentation
      env:
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      run: |
        cd docs
        make clean
        make html
    
    - name: Extract validation results
      id: validation
      run: |
        if [ -f docs/_build/validation/validation_report_*.json ]; then
          REPORT=$(ls -t docs/_build/validation/validation_report_*.json | head -1)
          
          TOTAL_VIOLATIONS=$(jq '.summary.total_violations' "$REPORT")
          FAILED_PATTERNS=$(jq '.summary.failed' "$REPORT")
          
          echo "total_violations=$TOTAL_VIOLATIONS" >> $GITHUB_OUTPUT
          echo "failed_patterns=$FAILED_PATTERNS" >> $GITHUB_OUTPUT
          
          echo "### Validation Summary" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "- **Total Violations:** $TOTAL_VIOLATIONS" >> $GITHUB_STEP_SUMMARY
          echo "- **Failed Patterns:** $FAILED_PATTERNS" >> $GITHUB_STEP_SUMMARY
          
          jq -r '.validations[] | "- **\(.pattern):** \(.status) (\(.violations | length) violations)"' "$REPORT" >> $GITHUB_STEP_SUMMARY
        else
          echo "No validation report found"
        fi
    
    - name: Upload validation reports
      uses: actions/upload-artifact@v3
      with:
        name: validation-reports
        path: docs/_build/validation/
        retention-days: 30
    
    - name: Upload documentation
      uses: actions/upload-artifact@v3
      with:
        name: documentation-html
        path: docs/_build/html/
        retention-days: 7
    
    - name: Comment PR with results
      if: github.event_name == 'pull_request'
      uses: actions/github-script@v6
      with:
        script: |
          const fs = require('fs');
          const reportFiles = fs.readdirSync('docs/_build/validation/')
            .filter(f => f.startsWith('validation_report_') && f.endsWith('.json'));
          
          if (reportFiles.length === 0) {
            return;
          }
          
          const reportPath = `docs/_build/validation/${reportFiles[0]}`;
          const report = JSON.parse(fs.readFileSync(reportPath, 'utf8'));
          
          let comment = '## 📊 Documentation Validation Results\n\n';
          comment += '| Metric | Value |\n';
          comment += '|--------|-------|\n';
          comment += `| Total Patterns | ${report.summary.total_patterns} |\n`;
          comment += `| ✅ Passed | ${report.summary.passed} |\n`;
          comment += `| ❌ Failed | ${report.summary.failed} |\n`;
          comment += `| ⚠️ Warnings | ${report.summary.warnings} |\n`;
          comment += `| Total Violations | ${report.summary.total_violations} |\n\n`;
          
          comment += '### Pattern Details\n\n';
          
          for (const validation of report.validations) {
            const statusEmoji = validation.status === 'PASS' ? '✅' : 
                               validation.status === 'FAIL' ? '❌' : '⚠️';
            comment += `${statusEmoji} **${validation.pattern}** - ${validation.status}\n`;
            
            if (validation.violations.length > 0) {
              comment += `  - ${validation.violations.length} violation(s)\n`;
              
              // Show first 3 violations
              const previewViolations = validation.violations.slice(0, 3);
              for (const violation of previewViolations) {
                comment += `    - [${violation.severity}] ${violation.type}: ${violation.constraint}\n`;
              }
              
              if (validation.violations.length > 3) {
                comment += `    - ... and ${validation.violations.length - 3} more\n`;
              }
            }
            comment += '\n';
          }
          
          comment += '\n📄 [View Full HTML Report](../actions/runs/${{ github.run_id }})';
          
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: comment
          });
    
    - name: Fail on violations
      if: steps.validation.outputs.failed_patterns != '0'
      run: |
        echo "::error::Build failed due to pattern violations"
        exit 1
```

---

### 5.3 Pre-commit Hook for Local Validation

**File:** `.pre-commit-config.yaml`

```yaml
repos:
  - repo: local
    hooks:
      - id: validate-documentation-tags
        name: Validate Documentation Tag Integrity
        entry: python scripts/validate_tags.py
        language: python
        files: '^docs/.*\.rst$'
        pass_filenames: false
        additional_dependencies:
          - pyyaml
          - sphinx-needs
      
      - id: check-pattern-assessments
        name: Check Pattern Assessment Completeness
        entry: python scripts/check_assessments.py
        language: python
        files: '^docs/.*\.rst$'
        pass_filenames: false
        additional_dependencies:
          - pyyaml
          - sphinx-needs
```

**File:** `scripts/validate_tags.py`

```python
#!/usr/bin/env python3
"""
Pre-commit hook to validate documentation tag integrity.

Validates:
1. Tag inventory counts match actual tags in document
2. All child tags cite parent tags
3. No orphaned tags
4. Tag ID format compliance
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
import yaml


class TagIntegrityValidator:
    """Validate tag integrity in reStructuredText documentation."""
    
    TAG_PATTERN = re.compile(r'\|([A-Z]+-\d+(?:\.\d+)?)\|')
    INVENTORY_PATTERN = re.compile(
        r':tag_inventory:\s*\[(.*?)\]',
        re.DOTALL
    )
    TAG_COUNT_PATTERN = re.compile(r':tag_count:\s*(\d+)')
    PARENT_CITATION_PATTERN = re.compile(r'←\s*\|([A-Z]+-\d+(?:\.\d+)?)\|')
    
    def __init__(self, docs_dir: Path):
        self.docs_dir = Path(docs_dir)
        self.errors = []
        self.warnings = []
    
    def validate_all_documents(self) -> bool:
        """
        Validate all RST files in docs directory.
        
        Returns
        -------
        bool
            True if all validations pass, False otherwise.
        """
        rst_files = list(self.docs_dir.glob('**/*.rst'))
        
        print(f"Validating {len(rst_files)} documentation files...")
        
        for rst_file in rst_files:
            self.validate_document(rst_file)
        
        # Print results
        if self.errors:
            print("\n❌ VALIDATION ERRORS:")
            for error in self.errors:
                print(f"  - {error}")
        
        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        if not self.errors:
            print("\n✅ All validations passed!")
            return True
        else:
            print(f"\n❌ Validation failed with {len(self.errors)} error(s)")
            return False
    
    def validate_document(self, filepath: Path) -> None:
        """Validate single RST document."""
        content = filepath.read_text(encoding='utf-8')
        
        # Extract all tags
        tags_found = set(self.TAG_PATTERN.findall(content))
        
        # Extract inventory
        inventory_match = self.INVENTORY_PATTERN.search(content)
        
        if not inventory_match:
            # No inventory in this file (may be valid)
            return
        
        inventory_str = inventory_match.group(1)
        inventory_tags = set(
            tag.strip(' "\'')
            for tag in inventory_str.split(',')
            if tag.strip()
        )
        
        # Extract tag count
        count_match = self.TAG_COUNT_PATTERN.search(content)
        declared_count = int(count_match.group(1)) if count_match else None
        
        # Validation 1: Inventory count matches actual
        if declared_count is not None:
            if len(inventory_tags) != declared_count:
                self.errors.append(
                    f"{filepath.name}: Inventory count mismatch. "
                    f"Declared: {declared_count}, Actual: {len(inventory_tags)}"
                )
        
        # Validation 2: All tags in document are in inventory
        undeclared_tags = tags_found - inventory_tags
        if undeclared_tags:
            self.errors.append(
                f"{filepath.name}: Tags found but not in inventory: {undeclared_tags}"
            )
        
        # Validation 3: All inventory tags exist in document
        missing_tags = inventory_tags - tags_found
        if missing_tags:
            self.errors.append(
                f"{filepath.name}: Inventory contains non-existent tags: {missing_tags}"
            )
        
        # Validation 4: Parent citations exist for child tags
        self._validate_parent_citations(filepath, content, tags_found)
    
    def _validate_parent_citations(
        self,
        filepath: Path,
        content: str,
        tags: Set[str]
    ) -> None:
        """Validate parent tag citations."""
        
        # Extract tag definitions and their parent citations
        tag_definitions = {}
        
        for match in re.finditer(r'\|([A-Z]+-\d+(?:\.\d+)?)\|([^|]*?)(?:\||$)', content):
            tag_id = match.group(1)
            context = match.group(2)
            
            # Look for parent citation in context
            parent_match = self.PARENT_CITATION_PATTERN.search(context)
            parent = parent_match.group(1) if parent_match else None
            
            tag_definitions[tag_id] = parent
        
        # Check that sub-tags have parent citations
        for tag_id in tags:
            if '.' in tag_id:  # Sub-tag (e.g., BRD-1.1)
                base_tag = tag_id.split('.')[0]  # BRD-1
                
                if tag_id in tag_definitions:
                    cited_parent = tag_definitions[tag_id]
                    
                    # Sub-tag should cite a parent (not its own base)
                    if cited_parent is None:
                        self.warnings.append(
                            f"{filepath.name}: Sub-tag {tag_id} has no parent citation"
                        )
                    elif cited_parent == base_tag:
                        self.warnings.append(
                            f"{filepath.name}: Sub-tag {tag_id} incorrectly cites "
                            f"its own base tag {base_tag} (should cite external parent)"
                        )


def main():
    """Main execution."""
    docs_dir = Path('docs')
    
    if not docs_dir.exists():
        print(f"Error: Documentation directory not found: {docs_dir}")
        sys.exit(1)
    
    validator = TagIntegrityValidator(docs_dir)
    success = validator.validate_all_documents()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
```

**File:** `scripts/check_assessments.py`

```python
#!/usr/bin/env python3
"""
Pre-commit hook to verify pattern assessments are complete.

Checks:
1. All SAD-layer tags have corresponding pattern assessments
2. Assessment confidence scores are present
3. Pattern roles are assigned
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Set


class AssessmentCompletenessChecker:
    """Verify pattern assessment completeness."""
    
    TAG_PATTERN = re.compile(r'\|([A-Z]+-\d+(?:\.\d+)?)\|')
    PATTERN_NAME_PATTERN = re.compile(r':pattern_name:\s*"?([^"\n]+)"?')
    PATTERN_ROLE_PATTERN = re.compile(r':pattern_role:\s*"?([^"\n]+)"?')
    CONFIDENCE_PATTERN = re.compile(r':pattern_confidence:\s*([\d.]+)')
    
    def __init__(self, docs_dir: Path):
        self.docs_dir = Path(docs_dir)
        self.issues = []
    
    def check_all_documents(self) -> bool:
        """
        Check all RST files for assessment completeness.
        
        Returns
        -------
        bool
            True if all checks pass, False otherwise.
        """
        rst_files = list(self.docs_dir.glob('**/*.rst'))
        
        print(f"Checking assessment completeness in {len(rst_files)} files...")
        
        # Collect all SAD tags
        sad_tags = set()
        tag_metadata = {}
        
        for rst_file in rst_files:
            content = rst_file.read_text(encoding='utf-8')
            
            # Find SAD tags
            for tag in self.TAG_PATTERN.findall(content):
                if tag.startswith('SAD-'):
                    sad_tags.add(tag)
                    
                    # Extract metadata for this tag
                    tag_metadata[tag] = self._extract_tag_metadata(content, tag)
        
        print(f"Found {len(sad_tags)} SAD-layer tags")
        
        # Check assessment completeness
        assessed_count = 0
        
        for tag, metadata in tag_metadata.items():
            if metadata['pattern_name']:
                assessed_count += 1
                
                # Validate assessment metadata
                if not metadata['pattern_role']:
                    self.issues.append(
                        f"Tag {tag} has pattern_name but missing pattern_role"
                    )
                
                if metadata['confidence'] is None:
                    self.issues.append(
                        f"Tag {tag} has pattern_name but missing pattern_confidence"
                    )
                elif metadata['confidence'] < 0.0 or metadata['confidence'] > 1.0:
                    self.issues.append(
                        f"Tag {tag} has invalid confidence score: {metadata['confidence']}"
                    )
        
        coverage = (assessed_count / len(sad_tags) * 100) if sad_tags else 0
        
        print(f"\nAssessment Coverage: {assessed_count}/{len(sad_tags)} ({coverage:.1f}%)")
        
        if self.issues:
            print("\n⚠️  ISSUES FOUND:")
            for issue in self.issues:
                print(f"  - {issue}")
            return False
        else:
            print("\n✅ All assessments complete!")
            return True
    
    def _extract_tag_metadata(
        self,
        content: str,
        tag_id: str
    ) -> Dict[str, any]:
        """Extract metadata for specific tag."""
        
        # Find tag definition section
        tag_pattern = re.escape(f'|{tag_id}|')
        tag_match = re.search(tag_pattern, content)
        
        if not tag_match:
            return {
                'pattern_name': None,
                'pattern_role': None,
                'confidence': None
            }
        
        # Extract context around tag (next 500 chars)
        start = tag_match.start()
        context = content[start:start+500]
        
        # Extract metadata
        pattern_name_match = self.PATTERN_NAME_PATTERN.search(context)
        pattern_role_match = self.PATTERN_ROLE_PATTERN.search(context)
        confidence_match = self.CONFIDENCE_PATTERN.search(context)
        
        return {
            'pattern_name': pattern_name_match.group(1) if pattern_name_match else None,
            'pattern_role': pattern_role_match.group(1) if pattern_role_match else None,
            'confidence': float(confidence_match.group(1)) if confidence_match else None
        }


def main():
    """Main execution."""
    docs_dir = Path('docs')
    
    if not docs_dir.exists():
        print(f"Error: Documentation directory not found: {docs_dir}")
        sys.exit(1)
    
    checker = AssessmentCompletenessChecker(docs_dir)
    success = checker.check_all_documents()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
```

---

## Phase 6: Documentation & Usage Examples (40 hours)

### 6.1 User Guide

**File:** `docs/assessment_layer_guide.rst`

```rst
================================================================================
Assessment Layer User Guide
================================================================================

.. metadata::
   :file-id: assessment-guide
   :version: 1.0.0
   :audience: Documentation Authors, Architects, LLM Agents

Overview
================================================================================

The Assessment Layer framework enables automated classification and validation
of architectural documentation using Large Language Models (LLMs) and 
design pattern taxonomies.

**Key Capabilities:**

- Automatic pattern detection in SAD-layer architectural elements
- LLM-powered classification with confidence scoring
- PlantUML diagram generation from assessed structures
- Graphviz traceability and dependency visualization
- Build-time validation with violation reporting

Quick Start
================================================================================

Step 1: Configure Assessment in conf.py
--------------------------------------------------------------------------------

Add the assessment configuration to your Sphinx ``conf.py``:

.. code-block:: python

   # Enable sphinx_assess extension
   extensions = [
       'sphinx.ext.autodoc',
       'sphinx_needs',
       'sphinxcontrib.plantuml',
       'sphinx_assess',  # Assessment layer extension
   ]
   
   # Assessment Layer Configuration
   needs_assessment_config = {
       # LLM Provider Settings
       'llm_provider': 'openai',
       'llm_model': 'gpt-4-turbo-2024-04-09',
       'llm_temperature': 0.1,
       'llm_max_tokens': 4096,
       
       # Pattern Schema Libraries
       'pattern_libraries': [
           'schemas/gof_patterns.yaml',
           'schemas/eip_patterns.yaml',
       ],
       
       # Diagram Generation
       'plantuml_jar_path': '/usr/local/bin/plantuml.jar',
       'plantuml_output_format': 'svg',
       'graphviz_engine': 'dot',
       
       # Validation Settings
       'validation_strictness': 'WARNING',  # ERROR | WARNING | INFO
       'fail_build_on_violations': False,
       
       # Template Paths
       'template_search_paths': [
           '_templates/plantuml',
           '_templates/graphviz'
       ],
   }

Step 2: Add Assessment Directive
--------------------------------------------------------------------------------

Insert assessment directive between SAD and TDD layers:

.. code-block:: rst

   .. <<<BEGIN-SAD>>>
   
   ================================================================================
   SAD — Architecture Definitions
   ================================================================================
   
   .. _SAD-1:
   
   Hub-and-Spoke Topology |SAD-1|
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   Core Process acts as central ROUTER; Services are DEALER endpoints.
   
   .. _SAD-2:
   
   Message Routing |SAD-2|
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   Core maintains routing table mapping client identity to socket identity.
   
   .. <<<END-SAD>>>
   
   
   .. <<<BEGIN-PDA>>>
   
   ================================================================================
   PDA — Pattern Design Assessment
   ================================================================================
   
   .. assess:: ARCH_PATTERN_CLASSIFICATION
      :scope: SAD-1, SAD-2, SAD-3
      :classification_type: design_pattern
      :schema: gof_behavioral
      :output_enrichment: pattern_role, pattern_name, pattern_confidence
      :diagram_template: templates/observer_pattern.puml.jinja2
   
   .. <<<END-PDA>>>

Step 3: Build Documentation
--------------------------------------------------------------------------------

.. code-block:: bash

   # Set API key (if using cloud LLM)
   export OPENAI_API_KEY=your-api-key-here
   
   # Build documentation
   cd docs
   make clean
   make html
   
   # View validation report
   open _build/validation/validation_report_*.html

Assessment Workflow
================================================================================

The assessment process follows this sequence:

1. **Tag Collection**: Sphinx-Needs collects all tags in scope
2. **LLM Classification**: Tags sent to LLM with pattern schema context
3. **Metadata Enrichment**: Classification results injected into Sphinx-Needs database
4. **Diagram Generation**: PlantUML/Graphviz diagrams rendered from enriched metadata
5. **Validation**: Pattern constraints checked against implementation
6. **Report Generation**: HTML/JSON/Markdown reports created

Diagram Generation
================================================================================

PlantUML Pattern Diagrams
--------------------------------------------------------------------------------

Generate pattern-specific class diagrams:

.. code-block:: rst

   .. plantuml_pattern:: Observer
      :participants: SAD-1, SAD-2, SAD-3, TDD-1, TDD-2
      :output_filename: observer_architecture
      :show_sequence: true

Graphviz Traceability Matrices
--------------------------------------------------------------------------------

Visualize tag dependencies:

.. code-block:: rst

   .. graphviz_assess:: traceability
      :scope: BRD-1, BRD-2, FSD-1, FSD-2, SAD-1, SAD-2
      :filter_layers: BRD, FSD, SAD
      :show_assessments: true
      :output_filename: brd_to_sad_traceability

Graphviz Pattern Participation
--------------------------------------------------------------------------------

Show all participants in a pattern:

.. code-block:: rst

   .. graphviz_assess:: pattern
      :pattern_name: Observer
      :output_filename: observer_participants

Validation Reports
================================================================================

The framework generates three report formats:

JSON Report (Machine-Readable)
--------------------------------------------------------------------------------

Located at: ``_build/validation/validation_report_TIMESTAMP.json``

Structure:

.. code-block:: json

   {
     "metadata": {
       "generated_at": "2024-01-15T14:32:00Z",
       "generator": "sphinx_assess"
     },
     "summary": {
       "total_patterns": 5,
       "passed": 3,
       "failed": 2,
       "total_violations": 8
     },
     "validations": [...]
   }

HTML Report (Human-Readable)
--------------------------------------------------------------------------------

Interactive HTML dashboard with:

- Summary statistics
- Violation heatmap
- Pattern-by-pattern breakdown
- Searchable/filterable tables

Markdown Report (Documentation-Friendly)
--------------------------------------------------------------------------------

Embeddable in documentation or commit messages.

Best Practices
================================================================================

1. **Assessment Timing**: Run assessments after SAD layer is stable
2. **Cache Management**: Enable caching to avoid redundant LLM calls
3. **Confidence Thresholds**: Review classifications with confidence < 0.7
4. **Incremental Validation**: Use CI/CD to catch violations early
5. **Template Customization**: Create project-specific PlantUML templates

Troubleshooting
================================================================================

Issue: LLM Classification Timeout
--------------------------------------------------------------------------------

**Symptom**: Assessment hangs or times out

**Solutions**:

- Reduce scope (fewer tags per assessment)
- Increase ``llm_timeout_seconds`` in config
- Use batching for large documentation sets

Issue: PlantUML Rendering Fails
--------------------------------------------------------------------------------

**Symptom**: Diagram generation errors

**Solutions**:

- Verify PlantUML JAR path in config
- Check Java installation: ``java -version``
- Validate template syntax manually

Issue: Validation False Positives
--------------------------------------------------------------------------------

**Symptom**: Incorrect violation reports

**Solutions**:

- Review pattern schema definitions
- Adjust ``validation_strictness`` level
- Add exceptions for legitimate edge cases

API Reference
================================================================================

For detailed API documentation, see:

- :doc:`api/assessment_directives`
- :doc:`api/pattern_validator`
- :doc:`api/diagram_generators`
```

---

## Conclusion & Deliverables Summary

This implementation plan provides a **production-ready**, **enterprise-grade** specification for an Assessment Layer framework integrated with Sphinx-Needs documentation systems. 

### Core Deliverables

1. **Sphinx Extension Package** (`sphinx_assess/`)
   - Custom directives (`assess`, `pattern`, `graphviz_assess`)
   - LLM classifier with multi-provider support
   - Template-based PlantUML generator
   - Graphviz traceability matrix generator
   - Pattern structural validator

2. **Configuration Schemas**
   - GoF pattern library (YAML)
   - Process flow taxonomy (YAML)
   - Template search paths
   - Validation rules

3. **Template Library**
   - Observer pattern template
   - Strategy pattern template
   - Sequence diagram template
   - Component diagram template

4. **Validation Framework**
   - Multiplicity constraint checker
   - Relationship validator
   - Diff analyzer (ideal vs. actual)
   - Multi-format report generator

5. **CI/CD Integration**
   - GitHub Actions workflow
   - Pre-commit hooks
   - Automated validation
   - PR commenting bot

6. **Documentation**
   - User guide with examples
   - API reference
   - Troubleshooting guide
   - Best practices

### Implementation Effort Summary

| Phase | Hours | Deliverables |
|-------|-------|-------------|
| Phase 1: Foundation | 80 | Schema extension, LLM classifier |
| Phase 2: Graphviz | 60 | Traceability matrices, layouts |
| Phase 3: PlantUML | 70 | Template system, rendering |
| Phase 4: Validation | 60 | Constraint checking, reports |
| Phase 5: CI/CD | 50 | Workflows, hooks |
| Phase 6: Docs | 40 | User guide, examples |
| **Total** | **360** | Complete framework |

### Success Metrics

- **100% traceability** from BRD → ISP with visual validation
- **Sub-5-second** assessment for 50-tag scopes
- **<1% false positive** rate on pattern violations
- **Zero manual intervention** required for standard patterns
- **Full CI/CD integration** with build-time enforcement

---
