#!/usr/bin/env python3
"""Fix: Replace Wikipedia search with FISH_IMG-based loading."""
with open('/opt/data/fishing-hk/index.html') as f:
    c = f.read()

# Find the loadFishImages function
start = c.find('async function loadFishImages()')
end = c.find('}\n\n// Render fish cards', start)
if end < 0:
    end = c.find('}\n\n// Page switching', start)

old_func = c[start:end+1]

new_func = """// Load fish images from curated FISH_IMG map
async function loadFishImages() {
  var g = document.getElementById('fishGrid');
  if (!g) return;
  var cards = g.querySelectorAll('.fi');
  for (var i = 0; i < FISH.length && i < cards.length; i++) {
    var chName = FISH[i][0];
    var existing = cards[i].querySelector('.fi-img-wrap');
    if (!existing) continue;
    var imgUrl = FISH_IMG[chName];
    if (imgUrl) {
      existing.innerHTML = '<img src="'+imgUrl+'" style="width:100%;height:100%;object-fit:contain" alt="'+chName+'">';
    } else {
      existing.innerHTML = '';
    }
  }
}"""

c = c.replace(old_func, new_func)
with open('/opt/data/fishing-hk/index.html', 'w') as f2:
    f2.write(c)

print("✅ Replaced Wikipedia search with FISH_IMG loading")
print(f"Old func: {len(old_func)} chars -> New func: {len(new_func)} chars")
