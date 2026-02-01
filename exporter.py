import json
import os
from datetime import datetime

class RecipeExporter:
    def __init__(self, output_dir="/home/udon/liasfile/openclaw-hub/recipes"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def create_recipe(self, title, description, steps, dependencies=None):
        recipe = {
            "version": "1.0",
            "recipe_id": f"recipe_{int(datetime.now().timestamp())}",
            "title": title,
            "description": description,
            "author": "Ria & Udon",
            "compatibility": {
                "os": ["linux"],
                "wsl": True,
                "min_vram_gb": 6
            },
            "dependencies": dependencies or {"apt": [], "pip": [], "openclaw_plugins": []},
            "steps": steps,
            "verification": "Check logs for success message."
        }
        
        filename = f"{recipe['recipe_id']}.json"
        path = os.path.join(self.output_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(recipe, f, ensure_ascii=False, indent=2)
        
        return path

if __name__ == "__main__":
    # サンプル：セキュリティ強化レシピの作成
    exporter = RecipeExporter()
    steps = [
        {"order": 1, "type": "command", "content": "chmod 700 ~/.openclaw", "explanation": "Configフォルダの権限を所有者のみに制限"},
        {"order": 2, "type": "config_patch", "content": '{"logging": {"redactSensitive": "tools"}}', "explanation": "ログの機密情報を自動マスク"}
    ]
    path = exporter.create_recipe("Basic Security Hardening", "OpenClawの基本セキュリティを強化するレシピ", steps)
    print(f"Recipe exported to: {path}")
