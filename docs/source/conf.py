# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'STARWARS Model Tool'
copyright = '2025, Kennedy Kandia'
author = 'Kennedy Kandia'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',       # For parsing docstrings
    'sphinx.ext.napoleon',      # For Google/NumPy style docstrings
    'sphinx.ext.viewcode',      # To include source code in the docs
    'sphinx.ext.todo',          # If you want to include TODOs in your docs
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
