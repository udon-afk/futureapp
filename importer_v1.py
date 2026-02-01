import json
import os
import subprocess

class RecipeImporter:
    """
    全世界のレシピを解析し、ユーザーの環境に合わせて
    『安全に』導入を代行する汎用エンジン。
    """
    def __init__(self, recipe_path):
        with open(recipe_path, 'r') as f:
            self.recipe = json.load(f)

    def analyze(self):
        print(f"\n===== 📦 Recipe Analysis: {self.recipe['title']} =====")
        print(f"Description: {self.recipe['description']}")
        print(f"Author: {self.recipe['author']}")
        
        # 依存関係のチェック
        deps = self.recipe.get('dependencies', {})
        if deps.get('apt'):
            print(f"⚠️  System Requirements: {', '.join(deps['apt'])}")
        if deps.get('pip'):
            print(f"🐍 Python Requirements: {', '.join(deps['pip'])}")

    def execute(self, dry_run=True):
        print(f"\n===== 🚀 Execution Plan {'(DRY RUN)' if dry_run else ''} =====")
        for step in self.recipe['steps']:
            print(f"[{step['order']}] {step['explanation']}")
            print(f"    Action ({step['type']}): {step['content']}")

            if not dry_run:
                # 実際の実行ロジック
                if step['type'] == 'command':
                    confirm = input("    これを実行してもいい？ (y/n): ")
                    if confirm.lower() == 'y':
                        os.system(step['content'])
                elif step['type'] == 'write_file':
                    print("    (ファイルの書き込みは手動、または将来のアップデートで対応)")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("使い方: python importer_v1.py <recipe.json>")
    else:
        importer = RecipeImporter(sys.argv[1])
        importer.analyze()
        importer.execute(dry_run=True)
        
        confirm = input("\n実際に実行を開始する？ (yes/no): ")
        if confirm.lower() == 'yes':
            importer.execute(dry_run=False)
