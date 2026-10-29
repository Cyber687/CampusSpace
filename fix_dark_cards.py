with open('frontend/css/style.css', 'r') as f: css = f.read()

css += """
/* Fix for Block Cards and Floor Pills in Dark Mode */
[data-theme="dark"] .block-card, [data-theme="dark"] .canteen-card {
  background: var(--panel) !important;
  border-color: var(--line) !important;
  color: var(--ink) !important;
}
[data-theme="dark"] .floor-pills span {
  background: #1e293b !important;
  color: #94a3b8 !important;
  border: 1px solid #334155;
}
"""
with open('frontend/css/style.css', 'w') as f: f.write(css)
print("✅ Fixed block cards and floor pills for Dark Mode!")
