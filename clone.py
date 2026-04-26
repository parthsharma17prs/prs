import re

def clone_website():
    with open('raw_index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Absolute URLs for ALL assets
    original_domain = "https://chkstepan.com"
    html = re.sub(r'(src|href|srcset)="\/', r'\1="' + original_domain + '/', html)
    
    # 2. Premium Studio Injection (Noise, Cursor, Branding)
    injection_script = """
    <script>
        // Dynamic Branding
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
            document.title = document.title.replace(/chkstepan/gi, 'FinSaathi');
        }

        // Custom Cursor
        function initCursor() {
            const cursor = document.createElement('div');
            cursor.className = 'custom-cursor';
            document.body.appendChild(cursor);
            
            document.addEventListener('mousemove', (e) => {
                cursor.style.left = e.clientX + 'px';
                cursor.style.top = e.clientY + 'px';
            });
        }

        // Kill Loader
        function killLoader() {
            const loaders = document.querySelectorAll('[class*="Tuk-dW__wrapper"], [class*="Tuk-dW__grayBg"]');
            loaders.forEach(el => {
                el.style.transition = 'opacity 1s ease';
                el.style.opacity = '0';
                setTimeout(() => el.remove(), 1000);
            });
            document.body.style.overflow = 'auto';
        }

        window.addEventListener('DOMContentLoaded', () => {
            applyBranding();
            initCursor();
            setTimeout(killLoader, 2000);
            
            // Inject Showcase link
            const link = document.createElement('a');
            link.className = 'showcase-link';
            link.href = 'projects.html';
            link.innerHTML = '<span>Explore Projects</span> <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>';
            document.body.appendChild(link);
        });

        const observer = new MutationObserver(() => applyBranding());
        observer.observe(document.body, { childList: true, subtree: true });
    </script>
    <style>
        /* Exact Same 2 Same Premium Overlays */
        body::after {
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: url('https://grainy-gradients.vercel.app/noise.svg');
            opacity: 0.05;
            pointer-events: none;
            z-index: 999999;
        }

        .custom-cursor {
            position: fixed;
            width: 8px;
            height: 8px;
            background: #729e84;
            border-radius: 50%;
            pointer-events: none;
            z-index: 1000000;
            transform: translate(-50%, -50%);
            transition: width 0.3s, height 0.3s, background 0.3s;
        }

        a:hover ~ .custom-cursor, 
        button:hover ~ .custom-cursor {
            width: 40px;
            height: 40px;
            background: rgba(114, 158, 132, 0.2);
            backdrop-filter: blur(4px);
        }

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
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            box-shadow: 0 10px 20px rgba(0,0,0,0.4);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .showcase-link:hover {
            transform: translateY(-5px) scale(1.05);
            background: #84b096;
        }

        #awwwards, [class*="badge"], [class*="watermark"] {
            display: none !important;
        }
    </style>
    """
    
    html = html.replace('</head>', injection_script + '</head>')

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    clone_website()
