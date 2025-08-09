#!/usr/bin/env python3
"""
Demo script to test the AI Code Review Bot locally
"""

import asyncio
import json
from reviewer import review_changed_files, render_markdown

# Mock changed files data (similar to what GitHub sends)
MOCK_CHANGED_FILES = [
    {
        "filename": "src/example.py",
        "status": "modified",
        "patch": """@@ -1,5 +1,8 @@
 def calculate_total(items):
-    total = 0
-    for item in items:
-        total += item['price']
-    return total
+    # This is a security issue - using eval
+    result = eval(f"sum([{','.join([str(item['price']) for item in items])}])")
+    return result
+
+def unsafe_function(user_input):
+    return eval(user_input)  # Very dangerous!
"""
    },
    {
        "filename": "src/frontend.js", 
        "status": "added",
        "patch": """@@ -0,0 +1,10 @@
+function processData(data) {
+    var results = [];
+    for (var i = 0; i < data.length; i++) {
+        results.push(data[i] * 2);
+    }
+    return results;
+}
+
+// Performance issue - this creates many DOM elements
+for (let i = 0; i < 1000; i++) {
+    document.body.appendChild(document.createElement('div'));
+}
"""
    }
]

MOCK_REPO_RULES = {
    "severity_threshold": "info",
    "max_findings_per_file": 3,
    "focus": ["correctness", "security", "performance", "readability"]
}

async def test_review():
    """Test the review functionality"""
    print("🤖 Testing AI Code Review Bot...")
    print("=" * 50)
    
    try:
        # Run the review
        result = await review_changed_files(
            owner="test-owner",
            repo="test-repo", 
            pr_number=1,
            changed=MOCK_CHANGED_FILES,
            repo_rules=MOCK_REPO_RULES
        )
        
        # Generate markdown output
        markdown = render_markdown(result, "ai-review-bot")
        
        print("Review Result:")
        print("-" * 30)
        print(markdown)
        print("\n" + "=" * 50)
        print("✅ Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        print("Make sure you have set OPENAI_API_KEY in your .env file")

if __name__ == "__main__":
    asyncio.run(test_review())
