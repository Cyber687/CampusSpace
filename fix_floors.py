with open('frontend/index.html', 'r') as f: html = f.read()

# Replace the empty floor select with one that has options 1 to 8
old_select = '<label>Floor<select id="filter-floor"><option value="">All floors</option></select></label>'
new_select = '''<label>Floor<select id="filter-floor">
    <option value="">All floors</option>
    <option value="1">Floor 1</option>
    <option value="2">Floor 2</option>
    <option value="3">Floor 3</option>
    <option value="4">Floor 4</option>
    <option value="5">Floor 5</option>
    <option value="6">Floor 6</option>
    <option value="7">Floor 7</option>
    <option value="8">Floor 8</option>
    <option value="8">Floor 8</option>
</select></label>'''

html = html.replace(old_select, new_select)

with open('frontend/index.html', 'w') as f: f.write(html)
print("✅ Added Floors 1 through 9 to the dropdown!")
