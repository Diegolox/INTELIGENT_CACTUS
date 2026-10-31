import json
from pathlib import Path
THEME=json.loads(Path(__file__).with_name('theme.json').read_text(encoding='utf-8'))
def font(size=14, weight="normal"):
    return (THEME['font'],size,weight)
