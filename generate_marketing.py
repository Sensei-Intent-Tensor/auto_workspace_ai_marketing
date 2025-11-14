#!/usr/bin/env python3
"""
Auto_Workspace-AI Marketing Generator
Creates futuristic marketing frames with time-of-day aesthetics
"""

import hashlib
import math

# Services rotation
SERVICES = [
    "Expert Consulting",
    "AI Automations", 
    "Live Workshops"
]

def calculate_solar_dampener(hour):
    """Calculate brightness multiplier based on hour (0-23)"""
    # Peak brightness at noon (12), darkest at midnight (0/24)
    # Using sine wave for smooth transition
    normalized = (hour - 6) / 12  # Shift so peak is at hour 12
    brightness = (math.sin(normalized * math.pi) + 1) / 2  # 0 to 1
    return max(0.2, min(1.0, brightness))  # Clamp between 0.2 and 1.0

def get_time_colors(hour):
    """Get color palette based on time of day"""
    brightness = calculate_solar_dampener(hour)
    
    if 0 <= hour < 6:  # Midnight to 6 AM - Deep night
        return {
            'bg_start': '#0a0520',
            'bg_end': '#1a0f3d',
            'text': '#00ffff',
            'accent': '#8b00ff',
            'tracer': '#4b0082',
            'glow': '#9d00ff',
            'brightness': brightness
        }
    elif 6 <= hour < 12:  # 6 AM to Noon - Morning to day
        return {
            'bg_start': '#1a4d7a',
            'bg_end': '#2d6ba3',
            'text': '#ffaa00',
            'accent': '#ff6b35',
            'tracer': '#00bfff',
            'glow': '#ffd700',
            'brightness': brightness
        }
    elif 12 <= hour < 18:  # Noon to 6 PM - Peak day
        return {
            'bg_start': '#00d4ff',
            'bg_end': '#ffffff',
            'text': '#ffff00',
            'accent': '#ff8c00',
            'tracer': '#ffffff',
            'glow': '#ffeb3b',
            'brightness': brightness
        }
    else:  # 6 PM to Midnight - Evening
        return {
            'bg_start': '#2d1b4e',
            'bg_end': '#612d7a',
            'text': '#ff00ff',
            'accent': '#ff1493',
            'tracer': '#9d4edd',
            'glow': '#ff69b4',
            'brightness': brightness
        }

def create_tracer_pattern(colors, index):
    """Create animated tracer line effects"""
    tracer_color = colors['tracer']
    accent_color = colors['accent']
    
    # Vary pattern based on index for uniqueness
    pattern_type = index % 4
    
    if pattern_type == 0:
        # Diagonal lines
        return f'''
        <g opacity="0.6">
            <line x1="0" y1="0" x2="400" y2="200" stroke="{tracer_color}" stroke-width="2"/>
            <line x1="0" y1="100" x2="400" y2="300" stroke="{tracer_color}" stroke-width="2"/>
            <line x1="0" y1="200" x2="400" y2="400" stroke="{accent_color}" stroke-width="3"/>
        </g>
        '''
    elif pattern_type == 1:
        # Circuit board style
        return f'''
        <g opacity="0.5">
            <path d="M 50 100 L 150 100 L 150 200 L 250 200" stroke="{tracer_color}" stroke-width="2" fill="none"/>
            <path d="M 100 50 L 100 150 L 200 150 L 200 250" stroke="{accent_color}" stroke-width="2" fill="none"/>
            <circle cx="150" cy="100" r="4" fill="{tracer_color}"/>
            <circle cx="150" cy="200" r="4" fill="{tracer_color}"/>
            <circle cx="100" cy="150" r="4" fill="{accent_color}"/>
        </g>
        '''
    elif pattern_type == 2:
        # Concentric arcs
        return f'''
        <g opacity="0.6">
            <path d="M 50 240 Q 200 100 350 240" stroke="{tracer_color}" stroke-width="2" fill="none"/>
            <path d="M 75 240 Q 200 130 325 240" stroke="{accent_color}" stroke-width="2" fill="none"/>
            <path d="M 100 240 Q 200 160 300 240" stroke="{tracer_color}" stroke-width="3" fill="none"/>
        </g>
        '''
    else:
        # Grid pattern
        return f'''
        <g opacity="0.4">
            <line x1="100" y1="0" x2="100" y2="480" stroke="{tracer_color}" stroke-width="1"/>
            <line x1="200" y1="0" x2="200" y2="480" stroke="{tracer_color}" stroke-width="1"/>
            <line x1="300" y1="0" x2="300" y2="480" stroke="{tracer_color}" stroke-width="1"/>
            <line x1="0" y1="160" x2="400" y2="160" stroke="{accent_color}" stroke-width="1"/>
            <line x1="0" y1="320" x2="400" y2="320" stroke="{accent_color}" stroke-width="1"/>
        </g>
        '''

def generate_marketing_svg(index, total_frames):
    """Generate one marketing frame"""
    
    # Calculate which hour this frame represents
    if total_frames == 24:
        hour = index
    elif total_frames == 1:
        hour = 12  # Static image at noon (brightest)
    else:
        # Distribute frames across 24 hours
        hour = int((index / total_frames) * 24)
    
    # Get service for this frame (rotate through 3 services)
    service = SERVICES[index % len(SERVICES)]
    
    # Get colors for this time of day
    colors = get_time_colors(hour)
    
    # Create tracer pattern
    tracers = create_tracer_pattern(colors, index)
    
    # Apply brightness dampener to glow
    glow_opacity = colors['brightness']
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 480">
    <defs>
        <linearGradient id="bg-gradient-{index}" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="{colors['bg_start']}" />
            <stop offset="100%" stop-color="{colors['bg_end']}" />
        </linearGradient>
        
        <filter id="glow-{index}">
            <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
            <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
        
        <filter id="strong-glow-{index}">
            <feGaussianBlur stdDeviation="8" result="coloredBlur"/>
            <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
    </defs>
    
    <style>
        .brand-text {{
            font-family: 'Arial Black', sans-serif;
            font-weight: bold;
            letter-spacing: 2px;
        }}
        .service-text {{
            font-family: 'Arial', sans-serif;
            font-weight: normal;
            letter-spacing: 1px;
        }}
    </style>
    
    <!-- Background -->
    <rect width="400" height="480" fill="url(#bg-gradient-{index})"/>
    
    <!-- Tracer effects -->
    {tracers}
    
    <!-- Main brand text -->
    <text x="200" y="200" text-anchor="middle" class="brand-text" 
          font-size="36" fill="{colors['text']}" 
          filter="url(#strong-glow-{index})">
        Auto_Workspace-AI
    </text>
    
    <!-- Accent line -->
    <line x1="50" y1="220" x2="350" y2="220" 
          stroke="{colors['accent']}" stroke-width="3" 
          opacity="{glow_opacity}"/>
    
    <!-- Service text -->
    <text x="200" y="280" text-anchor="middle" class="service-text" 
          font-size="28" fill="{colors['glow']}" 
          filter="url(#glow-{index})">
        {service}
    </text>
    
    <!-- Tech accent corners -->
    <g stroke="{colors['accent']}" stroke-width="2" fill="none" opacity="0.8">
        <path d="M 20 20 L 60 20 L 60 60"/>
        <path d="M 380 20 L 340 20 L 340 60"/>
        <path d="M 20 460 L 60 460 L 60 420"/>
        <path d="M 380 460 L 340 460 L 340 420"/>
    </g>
    
    <!-- Time indicator dots -->
    <g fill="{colors['glow']}" opacity="{glow_opacity}">
        <circle cx="200" cy="320" r="3"/>
        <circle cx="180" cy="320" r="2"/>
        <circle cx="220" cy="320" r="2"/>
    </g>
    
    <!-- Energy pulse effect -->
    <circle cx="200" cy="240" r="80" fill="none" 
            stroke="{colors['glow']}" stroke-width="1" 
            opacity="{glow_opacity * 0.3}"/>
    <circle cx="200" cy="240" r="100" fill="none" 
            stroke="{colors['glow']}" stroke-width="1" 
            opacity="{glow_opacity * 0.2}"/>
</svg>'''

def generate_svg(seed="default"):
    """Compatibility function for existing server code"""
    # Parse seed if it's in format "auto-X"
    if seed.startswith("auto-"):
        try:
            index = int(seed.split("-")[1])
        except:
            index = 0
    else:
        # Hash seed to get index
        hash_val = int(hashlib.sha256(seed.encode()).hexdigest(), 16)
        index = hash_val % 24
    
    return generate_marketing_svg(index, 24)
