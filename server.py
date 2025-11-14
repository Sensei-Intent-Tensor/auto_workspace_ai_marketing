#!/usr/bin/env python3
"""
Auto_Workspace-AI Marketing Server
Generates time-aware marketing GIFs with count-based control
"""

from flask import Flask, Response, request
from flask_cors import CORS
import os
from io import BytesIO

try:
    import cairosvg
    HAS_CAIRO = True
except ImportError:
    HAS_CAIRO = False

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

from generate_marketing import generate_marketing_svg

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    """Marketing info page"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Auto_Workspace-AI Marketing Generator</title>
        <style>
            body {
                font-family: 'Segoe UI', Arial, sans-serif;
                max-width: 900px;
                margin: 50px auto;
                padding: 20px;
                background: linear-gradient(135deg, #0a0520 0%, #1a4d7a 100%);
                color: #ffffff;
            }
            .container {
                background: rgba(255, 255, 255, 0.05);
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 8px 32px rgba(0, 255, 255, 0.1);
                border: 1px solid rgba(0, 255, 255, 0.2);
            }
            h1 { 
                color: #00ffff;
                text-shadow: 0 0 20px #00ffff;
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            h2 {
                color: #ff00ff;
                border-bottom: 2px solid #ff00ff;
                padding-bottom: 10px;
                margin-top: 30px;
            }
            code {
                background: rgba(0, 0, 0, 0.5);
                padding: 4px 12px;
                border-radius: 4px;
                font-family: 'Courier New', monospace;
                color: #00ff00;
                border: 1px solid #00ff00;
            }
            .example {
                margin: 20px 0;
                padding: 20px;
                background: rgba(0, 100, 200, 0.1);
                border-left: 4px solid #00ffff;
                border-radius: 4px;
            }
            .gif-demo {
                text-align: center;
                margin: 30px 0;
                padding: 20px;
                background: rgba(0, 0, 0, 0.3);
                border-radius: 8px;
            }
            img {
                border: 3px solid #00ffff;
                margin: 15px;
                box-shadow: 0 0 30px rgba(0, 255, 255, 0.3);
            }
            .feature {
                background: rgba(255, 0, 255, 0.1);
                padding: 15px;
                margin: 10px 0;
                border-radius: 6px;
                border-left: 3px solid #ff00ff;
            }
            a {
                color: #00ffff;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>⚡ Auto_Workspace-AI Marketing</h1>
            <p style="font-size: 1.2em; color: #ffaa00;">Dynamic marketing GIF generator with time-aware aesthetics</p>
            
            <h2>🎯 Quick Start</h2>
            <div class="example">
                <code>/marketing.gif?count=N</code>
                <p style="margin-top: 10px;">Where <strong>N</strong> is the number of frames you want</p>
            </div>
            
            <h2>🎬 Live Examples</h2>
            
            <div class="gif-demo">
                <h3>Static (1 frame)</h3>
                <img src="/marketing.gif?count=1" width="200">
                <p><code>/marketing.gif?count=1</code></p>
            </div>
            
            <div class="gif-demo">
                <h3>Quick Loop (3 frames)</h3>
                <img src="/marketing.gif?count=3" width="200">
                <p><code>/marketing.gif?count=3</code></p>
            </div>
            
            <div class="gif-demo">
                <h3>Full Day Cycle (24 frames)</h3>
                <img src="/marketing.gif?count=24" width="200">
                <p><code>/marketing.gif?count=24</code></p>
            </div>
            
            <h2>📋 API</h2>
            <p><strong>GET /marketing.gif</strong></p>
            <ul style="line-height: 1.8;">
                <li><strong>Parameter:</strong> <code>count</code> (integer, required) - Number of frames to generate</li>
                <li><strong>Parameter:</strong> <code>duration</code> (integer, optional) - Milliseconds per frame (default: 1000)</li>
                <li><strong>Returns:</strong> Animated GIF (image/gif)</li>
            </ul>
            
            <h2>✨ Features</h2>
            
            <div class="feature">
                <strong>🌅 Time-of-Day Aesthetics</strong>
                <p>Colors automatically adjust based on time representation (dark at midnight, bright at noon)</p>
            </div>
            
            <div class="feature">
                <strong>🔄 Service Rotation</strong>
                <p>Cycles through: Expert Consulting → AI Automations → Live Workshops</p>
            </div>
            
            <div class="feature">
                <strong>⚡ Electric Effects</strong>
                <p>Futuristic tracer patterns, glowing text, and dynamic accents</p>
            </div>
            
            <div class="feature">
                <strong>🎨 Solar Dampener</strong>
                <p>Brightness automatically scales with time representation for realistic day/night cycles</p>
            </div>
            
            <h2>💡 Usage Examples</h2>
            <div class="example">
                <p><code>/marketing.gif?count=1</code></p>
                <p>→ Single static marketing image (perfect for ads)</p>
            </div>
            
            <div class="example">
                <p><code>/marketing.gif?count=6</code></p>
                <p>→ 6 frames showing variety (12-hour span)</p>
            </div>
            
            <div class="example">
                <p><code>/marketing.gif?count=12&duration=500</code></p>
                <p>→ 12 frames, faster playback (0.5 sec per frame)</p>
            </div>
            
            <div class="example">
                <p><code>/marketing.gif?count=24</code></p>
                <p>→ Complete 24-hour day cycle (ultimate variety)</p>
            </div>
            
            <h2>🚀 Workflow</h2>
            <ol style="line-height: 2;">
                <li>Choose your frame count (1-24 recommended)</li>
                <li>Generate URL: <code>/marketing.gif?count=N</code></li>
                <li>Open in browser to preview</li>
                <li>Right-click → Save As → Download GIF</li>
                <li>Use anywhere (social media, emails, websites)</li>
            </ol>
            
            <h2>🎯 Why This Works</h2>
            <p>One URL generates infinite marketing variations. Instead of manually creating each image, 
            you specify how many frames you want and download a professional animated GIF in seconds.</p>
            
            <p style="margin-top: 30px; text-align: center; color: #00ffff;">
                <strong>Auto_Workspace-AI</strong> | Automating Your Marketing ⚡
            </p>
        </div>
    </body>
    </html>
    '''

@app.route('/marketing.gif')
def serve_marketing_gif():
    """Generate and serve marketing GIF based on count parameter"""
    count_param = request.args.get('count', '3')
    duration = int(request.args.get('duration', 1000))
    
    if not HAS_CAIRO:
        return Response(
            "GIF generation requires cairosvg. Install: pip install cairosvg",
            status=500,
            mimetype='text/plain'
        )
    
    if not HAS_PIL:
        return Response(
            "GIF generation requires Pillow. Install: pip install pillow",
            status=500,
            mimetype='text/plain'
        )
    
    try:
        # Parse count
        if not count_param.isdigit():
            return Response(
                "Error: 'count' parameter must be a positive integer",
                status=400,
                mimetype='text/plain'
            )
        
        count = int(count_param)
        
        if count < 1:
            return Response(
                "Error: 'count' must be at least 1",
                status=400,
                mimetype='text/plain'
            )
        
        if count > 100:
            return Response(
                "Error: 'count' maximum is 100 frames (file size limits)",
                status=400,
                mimetype='text/plain'
            )
        
        # Generate frames
        frames = []
        for i in range(count):
            svg_content = generate_marketing_svg(i, count)
            png_data = cairosvg.svg2png(
                bytestring=svg_content.encode('utf-8'),
                output_width=400,
                output_height=480
            )
            img = Image.open(BytesIO(png_data))
            frames.append(img)
        
        # Create animated GIF
        output = BytesIO()
        frames[0].save(
            output,
            format='GIF',
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=0,
            optimize=True
        )
        output.seek(0)
        
        return Response(output.read(), mimetype='image/gif')
        
    except Exception as e:
        return Response(
            f"Error generating GIF: {str(e)}",
            status=500,
            mimetype='text/plain'
        )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("⚡ Auto_Workspace-AI Marketing Generator Starting...")
    print(f"📍 Server running on port: {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
