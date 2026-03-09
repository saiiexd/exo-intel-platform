import os

docs_dir = 'docs'
out_file = 'docs/ExoIntel_Technical_Documentation.md'

sections = [
    ("Introduction", "01-introduction.md"),
    ("System Overview", "02-system-overview.md"),
    ("Platform Architecture", "03-architecture.md"),
    ("Data Ingestion and Processing Pipeline", "04-data-pipeline.md"),
    ("Machine Learning Methodology", "05-machine-learning.md"),
    ("Planet Discovery and Ranking Engine", "06-discovery-engine.md"),
    ("Explainable AI Analysis", "07-explainable-ai.md"),
    ("Scientific Insight Generation", "08-scientific-insights.md"),
    ("Interactive Interfaces", "09-frontend-interface.md"),
    ("Installation and Environment Setup", "10-installation.md"),
    ("Running the Platform", "11-running-the-platform.md"),
    ("Demonstration Guide", "12-demo-guide.md"),
    ("Development and Contribution Guide", "13-development-guide.md"),
    ("Reproducibility and Research Integrity", "14-reproducibility.md"),
    ("Repository Structure", "15-project-structure.md"),
    ("Future Research Directions", "16-future-work.md")
]

with open(out_file, 'w', encoding='utf-8') as outfile:
    outfile.write("---\n")
    outfile.write("title: ExoIntel Technical Documentation\n")
    outfile.write("author: Sai Venkat\n")
    outfile.write("date: March 2026\n")
    outfile.write("---\n\n")

    outfile.write("# Title Page\n\n")
    outfile.write("**ExoIntel Technical Documentation**\n\n")
    outfile.write("**Author:** Sai Venkat  \n")
    outfile.write("**Date:** March 2026  \n")
    outfile.write("**Version:** 2.0.0\n\n")
    
    outfile.write("<div style='page-break-after: always;'></div>\n\n")

    outfile.write("# Abstract\n\n")
    outfile.write("The ExoIntel AI Exoplanet Discovery Platform is an autonomous, scalable, and reproducible system designed to ingest, process, and analyze exoplanetary data. This document provides a comprehensive technical overview of the platform's architecture, data engineering pipelines, machine learning methodologies, and explainable AI integrations. It serves as a definitive guide for both researchers interpreting the platform's findings and software engineers contributing to its ongoing development.\n\n")
    
    outfile.write("<div style='page-break-after: always;'></div>\n\n")
    
    outfile.write("# Table of Contents\n\n")
    outfile.write("<!-- toc -->\n\n")
    
    outfile.write("<div style='page-break-after: always;'></div>\n\n")
    
    for section_title, filename in sections:
        filepath = os.path.join(docs_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as infile:
                content = infile.read()
                # remove the first line if it's a heading 1.
                lines = content.split('\n')
                if lines[0].startswith('# '):
                    lines = lines[1:]
                content = '\n'.join(lines).strip()
                outfile.write(f"# {section_title}\n\n")
                outfile.write(content + "\n\n")

print("Created consolidated MD")
