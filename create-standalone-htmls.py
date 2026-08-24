#!/usr/bin/env python3
"""
Creates 6 self-contained HTML files with all images and videos embedded as base64
"""

import base64
import os

blog_dir = "/Users/london.summers@outsystems.com/Documents/blog"
asset_dir = blog_dir  # Files are directly in blog directory

# Read HTML files
html_files = {
    '01-dark-factory-full.html': 'Part 1 - Full',
    '01-dark-factory-medium.html': 'Part 1 - Medium',
    '02-alignment-crisis-full.html': 'Part 2 - Full',
    '02-alignment-crisis-medium.html': 'Part 2 - Medium',
    '03-collaborative-sessions-full.html': 'Part 3 - Full',
    '03-collaborative-sessions-medium.html': 'Part 3 - Medium',
}

# Read and encode media files to base64
print("Reading and encoding media files...")

def encode_file(filepath):
    with open(filepath, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

profile_b64 = encode_file(f"{asset_dir}/profile.jpg")
diagram1_b64 = encode_file(f"{asset_dir}/diagram-part1.png")
diagram2_b64 = encode_file(f"{asset_dir}/diagram-part2.png")
diagram3_b64 = encode_file(f"{asset_dir}/diagram-part3.png")
video1_b64 = encode_file(f"{asset_dir}/diagram-part1.mp4")
video2_b64 = encode_file(f"{asset_dir}/diagram-part2.mp4")
video3_b64 = encode_file(f"{asset_dir}/diagram-part3.mp4")

print("Media files encoded. Creating standalone HTML files...")

for html_file, title in html_files.items():
    source_path = f"{blog_dir}/{html_file}"

    # Determine which media to use
    if 'dark-factory' in html_file:
        video_b64 = video1_b64
        diagram_b64 = diagram1_b64
        part_num = 1
    elif 'alignment' in html_file:
        video_b64 = video2_b64
        diagram_b64 = diagram2_b64
        part_num = 2
    else:  # collaborative
        video_b64 = video3_b64
        diagram_b64 = diagram3_b64
        part_num = 3

    # Read original HTML
    with open(source_path, 'r') as f:
        html_content = f.read()

    # Replace media file references with base64 data URIs

    # For full versions - replace video references
    if 'full' in html_file:
        # Replace video src
        html_content = html_content.replace(
            f'<source src="diagram-part{part_num}.mp4"',
            f'<source src="data:video/mp4;base64,{video_b64}"'
        )
    else:
        # For medium versions - replace image references
        html_content = html_content.replace(
            f'src="diagram-part{part_num}.png"',
            f'src="data:image/png;base64,{diagram_b64}"'
        )

    # Replace profile image in all versions
    html_content = html_content.replace(
        'src="profile.jpg"',
        f'src="data:image/jpeg;base64,{profile_b64}"'
    )

    # Create output filename
    output_file = html_file.replace('.html', '-Standalone.html')
    output_path = f"{blog_dir}/{output_file}"

    # Write standalone HTML
    with open(output_path, 'w') as f:
        f.write(html_content)

    file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"✅ Created: {output_file} ({file_size_mb:.1f} MB)")

print("\n" + "="*60)
print("All standalone HTML files created successfully!")
print("="*60)
print("\nFiles created:")
for html_file in html_files.keys():
    output_file = html_file.replace('.html', '-Standalone.html')
    print(f"  - {output_file}")

print("\nYou can now send any of these files directly to team members.")
print("Each file is completely self-contained with all media embedded.")
