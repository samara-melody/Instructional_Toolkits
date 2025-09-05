This is a working repository for executing TDBayes Inversion using BayesBay

- **BayesBay_BluePrint** Spreadsheet- high level summary of BayesBay framework. For details, see Magrini, Fabrizio, Jiawen He, and Malcolm Sambridge. "BayesBay: a versatile Bayesian inversion framework written in Python." Seismological Research Letters 96.3 (2025): 2052-2064.
- **TDBayesInversion** Slide Deck - Overview of TD Bayes including nuances of BayesBay implementation and a general scope of the area of research

- **"Tutorial" notebook** - generates synthetic Rayleigh wave dispersion data (using **disba**) and performs a transdimensional (TD) Bayesian inversion (using **BayesBay** and **disba**) to solve for a 1-D shear-wave velocity profile.
- **"Working" notebook**  - performs TDBayes on synthetic Frequency Gradiometry Data (from Daniel). Right now, data forward modeled as Rayleigh using **disba**
- **`smo_plotting_swd.py`** — Plotting functions for models, data, and solutions (some call BayesBay utilities). May need to modify for user/project preferences.
- **`smo_models.py`** — Example Earth models and functions which format them for input into **disba**.

The notebooks follow a more linear, step-by-step structure than the standard BayesBay tutorials, with all key user-defined variables grouped in one cell, followed by sequential implementation steps:
1. **Import packages**  
2. **Create synthetic data** (and optionally explore sensitivities)  
3. **Set user-defined variables** and prepare frameworks for TD Bayes implementation  
4. **Run inversion**  
5. **Plot results**
