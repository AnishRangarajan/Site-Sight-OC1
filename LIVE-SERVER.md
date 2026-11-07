# Preview with VS Code Live Server

1. Open this folder in VS Code and install the recommended **Live Server** extension if prompted.
2. Right-click `dist/index.html` and choose **Open with Live Server** (or click **Go Live**).
3. The static preview loads the saved Orange County snapshot from `dist/data`.

The preview supports browsing, filters, shortlists, comparisons, and print view. API-backed actions such as CSV downloads, generated briefs, and reference map layers require the full app server: run `npm install` once, then `npm run dev` and open `http://127.0.0.1:5173`.

To rebuild the preview after changing the source code, run `npm install` if needed and then `npm run build`. The VS Code Live Server root is configured to serve `dist`.
