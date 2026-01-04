"""
Sphinx Configuration for Maggie Documentation System.

This module configures the Sphinx documentation builder for the Maggie AI
assistant project. It defines traceability types, custom options, and build
settings for the Sphinx-Needs requirements management extension.

Purpose
-------
Provides centralized documentation build configuration including:

- Project metadata (name, version, author)
- Extension loading (sphinx_needs, sphinxcontrib.mermaid)
- Custom Sphinx-Needs type definitions for hierarchical traceability
- JSON output configuration for LLM context generation
- HTML theme and styling options

Dependencies
------------
- sphinx : Core documentation generator
- sphinx_needs : Requirements traceability extension
- sphinxcontrib.mermaid : Diagram rendering extension
- sphinx_rtd_theme : Read the Docs HTML theme

Traceability Schema (needs_types)
---------------------------------
The following directive types are configured for hierarchical documentation:

====== =========== ======= ============================================
Prefix Directive   Color   Purpose
====== =========== ======= ============================================
BRD    req         #BFDADC Business Requirements (root level)
NFR    constraint  #DF7E35 Non-Functional Requirements/Constraints
FSD    spec        #F0D27F Functional Specifications
SAD    arch        #A1D391 System Architecture Definitions
ICD    schema      #D3A191 Interface/Data Contracts
TDD    impl        #A191D3 Technical Design Blueprints
ISP    test        #D391A1 Integration/System Prompts (tests)
TERM   term        #E8E8E8 Glossary Terms
====== =========== ======= ============================================

Usage
-----
This file is automatically read by Sphinx when building documentation::

    sphinx-build -b html docs docs/_build

To generate JSON output for LLM context::

    sphinx-build -b needs docs docs/_build

Notes
-----
- `needs_build_json = True` enables JSON export of all needs items
- `suppress_warnings` silences false-positive cross-file link warnings
- Custom CSS is loaded from `docs/_static/custom.css`

See Also
--------
- Sphinx-Needs documentation: https://sphinx-needs.readthedocs.io/
- Project workflow: `.agent/workflows/update_documentation_spec.md`
"""
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Maggie'
copyright = '2025, Antigravity'
author = 'Antigravity'

version = '0.1'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx_needs', 'sphinxcontrib.mermaid']

# -- Sphinx-Needs Configuration ----------------------------------------------
needs_types = [
    dict(directive="req", title="Requirement", prefix="", color="#BFDADC", style="node"),
    dict(directive="constraint", title="Constraint", prefix="", color="#DF7E35", style="node"),
    dict(directive="spec", title="Specification", prefix="", color="#F0D27F", style="node"),
    dict(directive="arch", title="Architecture", prefix="", color="#A1D391", style="node"),
    dict(directive="schema", title="Contract", prefix="", color="#D3A191", style="node"),
    dict(directive="impl", title="Blueprint", prefix="", color="#A191D3", style="node"),
    dict(directive="test", title="Prompt", prefix="", color="#D391A1", style="node"),
    dict(directive="term", title="Term", prefix="", color="#E8E8E8", style="node"),
]

needs_extra_options = [
    "priority",
    "version",
    "layer",
    "latency"
]

needs_id_regex = r"^[A-Z0-9\-\.]+$"

# Strict Mode: Treat warnings as errors
# Strict Mode: Treat warnings as errors
# needs_warnings = {
#    'orphaned_need': True,
#    'unknown_link': True,
# }

# JSON Output for LLM Context
needs_build_json = True
needs_reproducible_json = True

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Suppress false-positive warnings (cross-file link validation timing issue)
suppress_warnings = [
    "needs.link_outgoing"
]



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = ["custom.css"]
