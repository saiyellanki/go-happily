# Go Happily

This repository contains a friendly motivational chatbot. There are two ways to use it:

- Run the original Streamlit app locally (`streamlit_app.py`).
- A static client-side version is provided in the `docs/` folder so it can be deployed to GitHub Pages.

## GitHub Pages (static)

The static single-page app is in the `docs/` folder and can be served directly by GitHub Pages from the `main` branch.

1. Commit and push changes to `main`.
2. In your repository Settings → Pages, set the source to `main` branch and `/docs` folder.
3. After a minute the site will be available at: `https://<your-github-username>.github.io/go-happily/`

The static app offers supportive messages, short grounding exercises, motivational quotes (public-domain), and simple CBT-style reframes — implemented client-side with no server required.

## Run the Streamlit app locally

1. Install the requirements

```bash
pip install -r requirements.txt
```

2. Run the app

```bash
streamlit run streamlit_app.py
```

