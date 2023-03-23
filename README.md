<div align="center">
    <img src="https://cdn3.iconfinder.com/data/icons/covid-19-coronavirus-protection-or-prevention-fill/64/HospitalCovid-19-512.png" alt="logo" height="128">
</div>

# ab-physicians

![coding_style](https://img.shields.io/badge/code%20style-black-000000.svg)

A Streamlit app to visualize listings of Alberta physicians

## Getting Started

> Install Ghostscript, which is a [dependency](https://camelot-py.readthedocs.io/en/master/user/install-deps.html#install-deps) for `camelot-py`

    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements-dev.txt
    python fetch_physicians.py
    python fetch_population.py
    python fetch_ratemds.py
    streamlit run streamlit_app.py

## Credits

- [Logo][1] by [KP Arts][2]
- [Medical Directory Listings][3]
- [Population and dwelling counts: Canada and census subdivisions (municipalities)][4]
- Ratings from [RateMDs][5]

[1]: https://www.iconfinder.com/icons/5946958/clinic_doctor_healthcare_hospital_medical_treatment_icon
[2]: https://www.iconfinder.com/katsana24
[3]: https://cpsa.ca/medical-directory-listings/
[4]: https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=9810000201
[5]: https://www.ratemds.com/
