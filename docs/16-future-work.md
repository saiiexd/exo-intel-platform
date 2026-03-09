# Future Work

## Expanding the ExoIntel Platform
The ExoIntel architecture is established as a foundational framework intended to scale alongside advancements in exoplanetary observation and machine learning methodology. The platform provides numerous vectors for significant expansion.

## Additional Astrophysical Features
Future iterations aim to natively integrate increasingly complex spectrographic data arrays. As next-generation instruments provide detailed atmospheric composition data—such as detecting biosignatures like ozone, methane, or complex carbon structures—the feature engineering pipeline must be expanded to parse these metrics. Processing direct atmospheric observations will drastically enhance the reliability of the habitability indices compared to current reliance on orbital dimension scaling.

## Improved Machine Learning Models
While the current ensemble decision tree methods provide robustness and necessary explainability, exploring advanced architectures represents a clear path forward. Implementing specifically directed deep neural networks or Graph Neural Networks (GNN) could uncover non-linear astrophysical relationships currently missed. This integration requires bridging advanced predictive capabilities with the existing SHAP explainability layer to avoid compromising system transparency.

## Expanded Datasets
Currently focused heavily upon the NASA Exoplanet Archive, integrating cross-referenced telemetry from independent European Space Agency (ESA) databases or specific transit survey independent logs (e.g., specific TESS or James Webb Space Telescope data dumps) will enrich the training data environment and correct potential underlying biases isolated to singular data providers.

## Collaborative Research Opportunities
The platform must increasingly support decentralized scientific operation. The goal is providing cloud orchestration features to permit multiple international research institutions to dynamically train models against proprietary restricted data subsets securely within the ExoIntel environment prior to publishing finalized candidate probabilities.
