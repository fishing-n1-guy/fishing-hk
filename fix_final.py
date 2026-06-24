#!/usr/bin/env python3
"""Final fix: keep iNaturalist images but remove known wrong ones + switch back to iNaturalist loading."""
with open('/opt/data/fishing-hk/index.html') as f:
    c = f.read()

# Replace the Wikipedia search function with the simpler iNaturalist one
old_func = """// Load fish images from Wikipedia (client-side)
async function loadFishImages() {
  var g = document.getElementById('fishGrid');
  if (!g) return;
  var cards = g.querySelectorAll('.fi');
  for (var i = 0; i < FISH.length && i < cards.length; i++) {
    var enName = FISH[i][1]; // English name
    var chName = FISH[i][0];
    var existing = cards[i].querySelector('.fi-img-wrap');
    if (!existing) continue;
    
    try {
      // Search English Wikipedia by English name
      var r = await fetch('https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch='+encodeURIComponent(enName+' fish')+'&format=json&origin=*&srlimit=2');
      var data = await r.json();
      var results = data.query && data.query.search;
      var imgUrl = null;
      
      if (results && results.length > 0) {
        var title = results[0].title;
        var r2 = await fetch('https://en.wikipedia.org/w/api.php?action=query&titles='+encodeURIComponent(title)+'&prop=pageimages&format=json&origin=*&pithumbsize=300');
        var data2 = await r2.json();
        var pages = data2.query && data2.query.pages;
        if (pages) {
          for (var pid in pages) {
            if (pages[pid].thumbnail) { imgUrl = pages[pid].thumbnail.source; break; }
          }
        }
      }
      
      if (imgUrl) {
        existing.innerHTML = '<img src="'+imgUrl+'" style="width:100%;height:100%;object-fit:contain" alt="'+chName+'">';
      } else {
        existing.innerHTML = '';
      }
    } catch(e) {
      existing.innerHTML = '';
    }
  }
}"""

new_func = """// Load fish images from curated source
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
      existing.innerHTML = '<img src="'+imgUrl+'" style="width:100%;height:100%;object-fit:contain" alt="'+chName+'" onerror="this.parentNode.innerHTML=\'\'">';
    } else {
      existing.innerHTML = '';
    }
  }
}"""

if old_func in c:
    c = c.replace(old_func, new_func)
    print("✅ Replaced Wikipedia search with iNaturalist loading")
else:
    print("❌ Could not find Wikipedia function")
    # Find what we have
    idx = c.find('async function loadFishImages')
    if idx >= 0:
        print(f"Found at position {idx}")
        print(c[idx:idx+200])

with open('/opt/data/fishing-hk/index.html', 'w') as f2:
    f2.write(c)

print("Done")
