with open('frontend/index.html', 'r') as f: html = f.read()

# Insert Floor 9 right after Floor 8
old_select = '<option value="8">Floor 8</option>'
new_select = '<option value="8">Floor 8</option>\n    <option value="9">Floor 9</option>'

html = html.replace(old_select, new_select)

with open('frontend/index.html', 'w') as f: f.write(html)
print("✅ Added Floor 9 to the dropdown!")
