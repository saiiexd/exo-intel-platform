# Development Guide

## Extending the Platform
The ExoIntel platform is designed as an iterative, open, and extensible architecture. Developers contributing to the core repository must strictly adhere to the established project structure and formal coding standards to guarantee long-term maintainability.

## Core Project Structure
The repository strictly divides backend computational operations from frontend presentation layers. All core ingestion, data engineering, machine learning, and database interactions reside within the `src/` directory. Standalone analytical outputs from these scripts are directed to the `analysis_outputs/` folder, while all React-based user interface components operate entirely within the `frontend/` directory. Explicit structural documentation is situated in the repository `README.md` and related structural guides.

## Coding Standards
*   **Python (Backend):** Adhere strictly to PEP 8 guidelines. Type hinting is highly recommended for all complex function signatures to simplify downstream integration and debugging. Code must be fully modularized to permit precise unit testing.
*   **TypeScript/React (Frontend):** Utilize strict TypeScript to enforce interface contracts between React components and potential backend API payloads. Functional components employing standard React Hooks are required to maintain state consistency without utilizing legacy class objects.

## Recommended Implementation Workflow
When addressing feature requests or implementing architectural improvements:
1.  **Branch Creation:** Isolate work on a dedicated feature branch stemming from `main`.
2.  **Modular Development:** Design features as independent modules, particularly when modifying data pipelines or integrating new ML evaluation metrics.
3.  **Local Validation:** Completely execute the `run_exointel_pipeline.py` script to ensure new modifications do not corrupt data integrity or cause regression in existing model performance. Verify the React interface compiles and renders error-free via `npm run dev`.
4.  **Pull Request Submission:** Submit a granular pull request requiring review, ensuring the commit history is clean, logically segmented, and accompanied by updated technical documentation covering newly introduced systems.
