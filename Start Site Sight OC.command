#!/bin/zsh
cd "${0:A:h}"
if [[ -x "$PWD/.runtime/node/bin/node" ]]; then
  export PATH="$PWD/.runtime/node/bin:$PATH"
fi
if ! command -v node >/dev/null; then
  echo 'Install Node.js 22 or newer, then launch again.'
  read -k 1
  exit 1
fi
if [[ ! -f .env ]]; then cp .env.example .env; fi
if [[ ! -d node_modules ]]; then npm install || exit 1; fi
echo 'Site Sight OC: open http://127.0.0.1:5173'
echo 'Paste API keys into .env and restart this launcher to connect services.'
npm run dev
