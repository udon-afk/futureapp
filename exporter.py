import json
import os
import argparse
from datetime import datetime

class RecipeFactory:
    """
    全世界のOpenClawユーザーが、自分の成功体験をどんな環境でも
    規格化されたJSONに変換できるようにするための汎用ツール。
    """
    def __init__(self, output_dir="recipes"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate(self, data):
        # 必須項目のバリデーション
        required = ["title", "description", "steps"]
        for field in required:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        recipe = {
            "version": "1.0",
            "recipe_id": f"recipe_{int(datetime.now().timestamp())}",
            "title": data["title"],
            "description": data["description"],
            "author": data.get("author", "Anonymous"),
            "compatibility": data.get("compatibility", {
                "os": ["linux"],
                "wsl": True,
                "required_privileges": "user"
            }),
            "dependencies": data.get("dependencies", {
                "apt": [],
                "pip": [],
                "openclaw_plugins": []
            }),
            "steps": data["steps"],
            "verification": data.get("verification", ""),
            "tags": data.get("tags", [])
        }

        filename = f"{recipe['recipe_id']}.json"
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(recipe, f, ensure_ascii=False, indent=2)
        
        return filepath

def interactive_mode():
    print("--- 🎀 Ria's Success Recipe Wizard ---")
    factory = RecipeFactory()
    data = {}
    data["title"] = input("タイトル (例: Unity Build Automation): ")
    data["description"] = input("説明 (何ができるようになる?): ")
    
    print("\n[手順の入力] 'exit' と入力して終了")
    steps = []
    order = 1
    while True:
        content = input(f"手順 {order} の内容 (コマンドや設定): ")
        if content.lower() == 'exit': break
        explanation = input(f"手順 {order} の解説: ")
        steps.append({
            "order": order,
            "type": "command", # デフォルト。必要に応じて後で拡張
            "content": content,
            "explanation": explanation
        })
        order += 1
    data["steps"] = steps
    
    path = factory.generate(data)
    print(f"\n✅ レシピが生成されたよ！: {path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--interactive", action="store_true", help="対話モードでレシピを作成")
    parser.add_argument("--json-file", help="既存のJSONやログからレシピを生成 (将来用)")
    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
    else:
        print("使い方: python exporter.py --interactive")
