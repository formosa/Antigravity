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
