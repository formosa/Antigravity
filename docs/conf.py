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
    dict(directive="brd", title="Business Requirements Document", prefix="BRD_", color="#BFDADC", style="artifact"),
    dict(directive="nfr", title="Non-Functional Requirements", prefix="NFR_", color="#DF7E35", style="artifact"),
    dict(directive="fsd", title="Functional Specification Document", prefix="FSD_", color="#F0D27F", style="artifact"),
    dict(directive="sad", title="System Architecture Document", prefix="SAD_", color="#A1D391", style="artifact"),
    dict(directive="icd", title="Interface Control Document", prefix="ICD_", color="#D3A191", style="artifact"),
    dict(directive="tdd", title="Technical Design Document", prefix="TDD_", color="#A191D3", style="artifact"),
    dict(directive="isp", title="Integration System Prompts", prefix="ISP_", color="#D391A1", style="artifact"),
    dict(directive="term", title="Glossary Term", prefix="TERM_", color="#E8E8E8", style="artifact"),
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
