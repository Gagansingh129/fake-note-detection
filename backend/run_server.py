import os
import sys
import tempfile
from pathlib import Path

# Set cache directories to writable temp folder before importing matplotlib/tensorflow
mpl_dir = os.path.join(tempfile.gettempdir(), "matplotlib_noteguard")
os.makedirs(mpl_dir, exist_ok=True)
os.environ["MPLCONFIGDIR"] = mpl_dir
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Ensure backend root is on sys.path
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)
