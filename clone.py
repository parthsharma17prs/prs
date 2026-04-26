import re

def clone_website():
    with open('raw_index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Ensure absolute URLs for ALL assets (CSS, JS, Images)
    original_domain = "https://chkstepan.com"
    
    # Prefix root-relative paths
    html = re.sub(r'(src|href|srcset)="\/', r'\1="' + original_domain + '/', html)
    
    # 2. Inject Dynamic Branding & Animation Fixes
    # We don't replace strings in the HTML directly to avoid breaking Next.js/Framer hydration.
    # Instead, we do it in the browser AFTER the page loads.
    
    injection_script = """
    <script>
        // 1. DYNAMIC REBRANDING (Text only, to avoid breaking scripts)
        function applyBranding() {
            const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
            let node;
            while (node = walk.nextNode()) {
                const text = node.nodeValue;
                const newText = text
                    .replace(/chkstepan/gi, 'FinSaathi')
                    .replace(/Stepan Chokobok/gi, 'FinSaathi Team')
                    .replace(/Stepan/gi, 'FinSaathi')
                    .replace(/Romania/gi, 'India');
                if (text !== newText) node.nodeValue = newText;
            }
            
            // Rebrand meta/title
            document.title = document.title.replace(/chkstepan/gi, 'FinSaathi');
        }

        // 2. ANIMATION & LOADER FIX
        // Force hide the original loader if it gets stuck
        function killLoader() {
            const loaders = document.querySelectorAll('[class*="Tuk-dW__wrapper"], [class*="Tuk-dW__grayBg"]');
            if (loaders.length > 0) {
                console.log("Removing stuck loader...");
                loaders.forEach(el => {
                    el.style.transition = 'opacity 1s ease';
                    el.style.opacity = '0';
                    setTimeout(() => el.remove(), 1000);
                });
                document.body.style.overflow = 'auto';
            }
        }

        // 3. INJECT SHOWCASE BUTTON
        function injectShowcase() {
            if (document.querySelector('.showcase-link')) return;
            const link = document.createElement('a');
            link.className = 'showcase-link';
            link.href = 'projects.html';
            link.innerHTML = '<span>Explore Projects</span> <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>';
            document.body.appendChild(link);
        }

        // Run logic
        window.addEventListener('DOMContentLoaded', () => {
            applyBranding();
            injectShowcase();
            // Wait for Framer to hopefully finish, then kill loader if it didn't
            setTimeout(killLoader, 2500);
        });

        // Continuous observer for dynamic content
        const observer = new MutationObserver((mutations) => {
            applyBranding();
            // Hunt watermarks
            mutations.forEach(m => {
                m.addedNodes.forEach(node => {
                    if (node.nodeType === 1) {
                        if (node.innerText && node.innerText.includes("Made in Framer")) node.remove();
                        if (node.id === "awwwards") node.remove();
                    }
                });
            });
        });
        observer.observe(document.body, { childList: true, subtree: true });
    </script>
    <style>
        /* Premium Showcase Link */
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
        /* Hide watermarks via CSS as fallback */
        #awwwards, [class*="badge"], [class*="watermark"] {
            display: none !important;
        }
    </style>
    """
    
    # 3. Clean up the HTML from previous hard-coded replacements
    # (Just in case raw_index.html was already modified, though it should be raw)
    
    # Find head and inject
    if '</head>' in html:
        html = html.replace('</head>', injection_script + '</head>')
    else:
        html = html + injection_script

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    clone_website()
