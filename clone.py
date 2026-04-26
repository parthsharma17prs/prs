import re

def clone_website():
    with open('raw_index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add <base href="...">
    base_tag = '<base href="https://chkstepan.com/">'
    html = html.replace('<head>', '<head>' + base_tag)

    # 2. Inject MutationObserver and custom styles
    script_to_inject = """
    <script>
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === 1) {
                        const watermarkTexts = ["Framer", "Awwwards", "Made in Framer"];
                        if (node.id === "awwwards" || (node.innerText && watermarkTexts.some(text => node.innerText.includes(text)))) {
                            node.remove();
                        }
                        const watermarks = node.querySelectorAll('[id*="awwwards"], [class*="badge"], [class*="watermark"]');
                        watermarks.forEach(el => el.style.display = 'none');
                    }
                });
            });
        });
        observer.observe(document.body || document.documentElement, { childList: true, subtree: true });
        window.addEventListener('DOMContentLoaded', () => {
            document.querySelectorAll('#awwwards').forEach(el => el.remove());
        });
    </script>
    <style>
        .showcase-link {
            position: fixed;
            bottom: 30px;
            right: 30px;
            z-index: 10000;
            background: #729e84;
            color: white !important;
            padding: 12px 24px;
            border-radius: 50px;
            text-decoration: none !important;
            font-family: sans-serif;
            font-weight: 600;
            box-shadow: 0 10px 20px rgba(0,0,0,0.4);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            gap: 8px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .showcase-link:hover {
            transform: translateY(-5px) scale(1.05);
            background: #84b096;
            box-shadow: 0 15px 30px rgba(0,0,0,0.5);
        }
    </style>
    """
    html = html.replace('</head>', script_to_inject + '</head>')

    # 3. Inject Project Showcase Link
    showcase_html = '<a href="projects.html" class="showcase-link"><span>Explore Projects</span> <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg></a>'
    html = html.replace('</body>', showcase_html + '</body>')

    # 4. Branded Replacements
    replacements = {
        'chkstepan': 'FinSaathi',
        'Stepan Chokobok': 'FinSaathi Team',
        'Stepan': 'FinSaathi',
        'chkstepan11@gmail.com': 'contact@finsaathi.com',
        'Romania': 'India',
        'Europe, Romania': 'New Delhi, India',
        'chkstepan.dev': 'finsaathi.com',
        '©2026': '©2026 FinSaathi'
    }

    for old, new in replacements.items():
        html = html.replace(old, new)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    clone_website()
