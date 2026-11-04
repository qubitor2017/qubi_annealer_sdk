import json
from pathlib import Path
def save_result(result,path):
    Path(path).write_text(json.dumps(result.as_dict(),indent=2,default=str),encoding='utf-8')
